def chunk_text(text, chunk_size=350, overlap=50):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    sample_text = " ".join(["AI"] * 1000)

    chunks = chunk_text(sample_text)

    print("Chunks Created:", len(chunks))