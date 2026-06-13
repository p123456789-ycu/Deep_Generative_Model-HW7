import os
import faiss
import pickle

from sentence_transformers import (
    SentenceTransformer
)

os.makedirs(
    "data",
    exist_ok=True
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

documents = []

for root, dirs, files in os.walk("kb"):

    for file in files:

        if file.endswith(".txt"):

            path = os.path.join(
                root,
                file
            )

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                documents.append({
                    "source": path,
                    "content": f.read()
                })
texts = [
    doc["content"]
    for doc in documents
]

embeddings = model.encode(
    texts,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(embeddings)

faiss.write_index(
    index,
    "data/worldcup.index"
)

with open(
    "data/worldcup.pkl",
    "wb"
) as f:

    pickle.dump(
        documents,
        f
    )

print("FAISS built")