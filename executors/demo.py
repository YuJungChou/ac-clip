import asyncio

import numpy as np
from docarray import DocumentArray, Document
from jina import Executor, requests


class RequestExecutor(Executor):
    @requests(
        on=['/index', '/search']
    )  # foo will be bound to `/index` and `/search` endpoints
    def foo(self, **kwargs):
        print(f'Calling foo')

    @requests(on='/other')  # bar will be bound to `/other` endpoint
    async def bar(self, **kwargs):
        await asyncio.sleep(1.0)
        print(f'Calling bar')


class PrintDocuments(Executor):
    @requests
    def foo(self, docs, **kwargs):
        for doc in docs:
            print(f' PrintExecutor: received document with text: "{doc.text}"')


class ProcessDocuments(Executor):
    @requests(on='/change_in_place')
    def in_place(self, docs, **kwargs):
        # This executor will only work on `docs` and will not consider any other arguments
        for doc in docs:
            print(f' ProcessDocuments: received document with text "{doc.text}"')
            doc.text = 'I changed the executor in place'

    @requests(on='/return_different_docarray')
    def ret_docs(self, docs, **kwargs):
        # This executor will only work on `docs` and will not consider any other arguments
        ret = DocumentArray()
        for doc in docs:
            print(f' ProcessDocuments: received document with text: "{doc.text}"')
            ret.append(Document(text='I returned a different Document'))
        return ret


class DemoEncoder(Executor):
    @requests
    def encode(self, docs: 'DocumentArray', **kwargs):
        print(f"Got task with document number '{len(docs)}'.")
        for doc in docs:
            print(f"Embedding text '{doc.text}' ...")
            doc.embedding = np.random.random(5)
        return docs


if __name__ == '__main__':

    from jina import Flow

    f = Flow().add(uses=RequestExecutor)

    with f:
        f.post(on='/index', inputs=[])
        f.post(on='/other', inputs=[])
        f.post(on='/search', inputs=[])

    f = Flow().add(uses=ProcessDocuments).add(uses=PrintDocuments)

    with f:
        f.post(on='/change_in_place', inputs=DocumentArray(Document(text='request')))
        f.post(
            on='/return_different_docarray', inputs=DocumentArray(Document(text='request'))
        )
