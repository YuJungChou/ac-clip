from typing import Optional, Text, Tuple

import torch
from transformers import (
    AutoModel,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerFast,
)

from config import settings

logger = settings.logger


def load_transformers_model(
    model_name: Text,
    tokenizer_name: Optional[Text] = None,
    device: Optional[Text] = None
) -> Tuple['PreTrainedModel', 'PreTrainedTokenizerFast']:
    """Load transformers model then return them."""

    tokenizer_name = model_name if tokenizer_name is None else tokenizer_name
    device = ('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device

    model: 'PreTrainedModel' = AutoModel.from_pretrained(model_name)
    model.to(device=device)
    if str(device).lower() == 'cpu':
        model.float()

    tokenizer: 'PreTrainedTokenizerFast' = AutoTokenizer.from_pretrained(tokenizer_name)

    return (model, tokenizer)
