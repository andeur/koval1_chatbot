import chromadb
from sentence_transformers import SentenceTransformer

from main import charger_cours
from chunking import creer_chunks

MODELE = "intfloat/multilingual-e5-small"
model = SentenceTransformer(MODELE)


def indexer():
    chunks = creer_chunks(charger_cours())
    chunks = [c for c in chunks if len(c["texte"].split()) >= 30]
    print(f"{len(chunks)} chunks à indexer")

    textes = ["passage: " + c["texte"] for c in chunks]
    embeddings = model.encode(
        textes, batch_size=32, show_progress_bar=True, normalize_embeddings=True
    )

    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection("cours")
    except Exception:
        pass
    collection = client.create_collection("cours", metadata={"hnsw:space": "cosine"})

    for i in range(0, len(chunks), 500):
        lot = chunks[i:i + 500]
        collection.add(
            ids=[c["id"] for c in lot],
            embeddings=embeddings[i:i + 500].tolist(),
            documents=[c["texte"] for c in lot],
            metadatas=[{"source": c["source"], "page": c["page"]} for c in lot],
        )
    print("Indexation terminée")


def rechercher(question, n=4):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("cours")
    vecteur = model.encode(["query: " + question], normalize_embeddings=True)
    res = collection.query(query_embeddings=vecteur.tolist(), n_results=n)
    return list(zip(res["documents"][0], res["metadatas"][0], res["distances"][0]))


if __name__ == "__main__":
    indexer()
    for texte, meta, dist in rechercher("Qu'est-ce que la reconnaissance des formes ?"):
        print(f"\n[{meta['source']} - page {meta['page']}] (distance {dist:.3f})")
        print(texte[:300])