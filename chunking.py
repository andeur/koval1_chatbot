
from main import charger_cours


def decouper(texte, taille=200, chevauchement=40):
    mots = texte.split()
    pas = taille - chevauchement
    chunks = []
    for debut in range(0, len(mots), pas):
        morceau = mots[debut:debut + taille]
        chunks.append(" ".join(morceau))
        if debut + taille >= len(mots):
            break
    return chunks


def creer_chunks(documents, taille=200, chevauchement=40):
    resultat = []
    for doc in documents:
        for i, morceau in enumerate(decouper(doc["texte"], taille, chevauchement)):
            resultat.append({
                "id": f"{doc['source']}_p{doc['page']}_c{i}",
                "source": doc["source"],
                "page": doc["page"],
                "texte": morceau,
            })
    return resultat


if __name__ == "__main__":
    docs = charger_cours()
    chunks = creer_chunks(docs)
    print(f"{len(docs)} pages -> {len(chunks)} chunks")
    print(chunks[0]["id"])
    print(chunks[0]["texte"][:300])

    from collections import Counter
    from main import charger_cours
    from chunking import creer_chunks

    docs = charger_cours()
    chunks = creer_chunks(docs)

    pages = Counter(d["source"] for d in docs)
    nb_chunks = Counter(c["source"] for c in chunks)

    for source in pages:
        print(f"{source}: {pages[source]} pages, {nb_chunks[source]} chunks")