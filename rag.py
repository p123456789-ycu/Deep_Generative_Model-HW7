import faiss
import pickle

from sentence_transformers import SentenceTransformer


class WorldCupRAG:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            "data/worldcup.index"
        )

        print("Loading documents...")

        with open(
            "data/worldcup.pkl",
            "rb"
        ) as f:

            self.documents = pickle.load(f)

        print(
            f"Loaded {len(self.documents)} documents."
        )

    # =====================================
    # Debug Search
    # Shows source + content
    # =====================================

    def search(
        self,
        query,
        top_k=3
    ):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(
            embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx >= len(self.documents):
                continue

            doc = self.documents[idx]

            source = doc.get(
                "source",
                "Unknown"
            )

            content = doc.get(
                "content",
                ""
            )

            results.append(
                f"""
SOURCE:
{source}

CONTENT:
{content}
"""
            )

        return "\n".join(results)

    # =====================================
    # Retrieval for LLM
    # Returns only content
    # =====================================

    def retrieve(
        self,
        query,
        top_k=3
    ):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(
            embedding,
            top_k
        )

        contexts = []

        for idx in indices[0]:

            if idx >= len(self.documents):
                continue

            doc = self.documents[idx]

            contexts.append(
                doc.get(
                    "content",
                    ""
                )
            )

        return "\n\n".join(contexts)

    # =====================================
    # Return raw documents
    # Useful for future agent expansion
    # =====================================

    def retrieve_docs(
        self,
        query,
        top_k=3
    ):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(
            embedding,
            top_k
        )

        docs = []

        for idx in indices[0]:

            if idx >= len(self.documents):
                continue

            docs.append(
                self.documents[idx]
            )

        return docs


if __name__ == "__main__":

    rag = WorldCupRAG()

    print("\n")
    print("=" * 60)
    print("TEST QUERY")
    print("=" * 60)

    result = rag.search(
        "World Cup Final"
    )

    print(result)
