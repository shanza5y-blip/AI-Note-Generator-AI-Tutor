from chunker import chunk_text

def test_chunk_creation():

    text = " ".join(["AI"] * 1000)

    chunks = chunk_text(
        text,
        chunk_size=350,
        overlap=50
    )

    assert len(chunks) > 0


def test_chunk_size():

    text = " ".join(["AI"] * 1000)

    chunks = chunk_text(text)

    for chunk in chunks[:-1]:
        assert len(chunk.split()) <= 350
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from chunker import chunk_text