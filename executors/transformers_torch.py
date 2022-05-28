from multiprocessing.pool import ThreadPool
from typing import Optional, Text

import numpy as np
import torch
from jina import Executor, requests, DocumentArray, monitor
from transformers import AutoTokenizer, AutoModel, BertTokenizerFast, BertModel
from transformers.modeling_outputs import ModelOutput


class TransformersEncoder(Executor):
    def __init__(
        self,
        model_name: Text = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        device: Optional[Text] = None,
        num_worker_preprocess: int = 1,
        batch_size: int = 16,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if not device:
            self._device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self._device = device

        self._batch_size = batch_size

        self._tokenizer: 'BertModel' = AutoTokenizer.from_pretrained(model_name)
        self._model: 'BertTokenizerFast' = AutoModel.from_pretrained(model_name)

        self._pool = ThreadPool(processes=num_worker_preprocess)

    def mean_pooling(
        self, model_output: 'ModelOutput', attention_mask: 'torch.Tensor'
    ):
        """Mean Pooling - Take attention mask into account for correct averaging."""

        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = (
            attention_mask
            .unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )
        return (
            torch.sum(
                token_embeddings * input_mask_expanded, 1
            )
            / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        )

    def embedding(
        self, docs: 'DocumentArray'
    ) -> 'torch.Tensor':
        """"""

        encoded_input = self._tokenizer(
            docs.texts, padding=True, truncation=True, return_tensors='pt'
        )
        with torch.inference_mode():
            model_output = self._model(**encoded_input)

        # Perform pooling. In this case, max pooling.
        texts_embeddings = self.mean_pooling(
            model_output=model_output, attention_mask=encoded_input['attention_mask']
        )
        return texts_embeddings

    @monitor()
    def _preprocess_texts(self, docs: 'DocumentArray'):
        return docs

    @requests
    async def encode(self, docs: 'DocumentArray', **kwargs):
        """"""

        with torch.inference_mode():

            for docs_batch in docs.map_batch(
                self._preprocess_texts,
                batch_size=self._batch_size,
                pool=self._pool,
            ):
                docs_batch.embeddings = (
                    self.embedding(docs_batch)
                    .cpu()
                    .numpy()
                    .astype(np.float32)
                )

        return docs
