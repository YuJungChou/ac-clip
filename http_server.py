import time
from typing import List, Text

import numpy as np
from fastapi import Body, FastAPI
from clip_client import Client

from config import settings

logger = settings.logger


app = FastAPI()

clip_client = Client('grpc://0.0.0.0:51000')


@app.post("/")
async def encode(
    texts: List[Text] = Body(
        ...,
        example=['I Am Iron Man.', 'I can do this all day.', 'I am Groot.'],
    )
) -> List[List[float]]:
    """Request clip service."""

    if len(texts) == 0:
        return []

    time_start = time.time()
    text_embeddings: np.ndarray = await clip_client.aencode(texts)
    time_cost = time.time() - time_start
    logger.info(f"Processed {len(texts)} texts with timecost {time_cost * 1000:0.3f} ms.")

    return text_embeddings.tolist()
