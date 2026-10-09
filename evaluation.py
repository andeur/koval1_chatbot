from indexation import rechercher
from chatbot import repondre

import json

with open("tests.json", encoding="utf-8") as f:
    TESTS = json.load(f)

TESTS += [
    {"question": "Quelle est la capitale de la France ?", "source": None, "pages": None},
    {"question": "Comment préparer une pizza margherita ?", "source": None, "pages": None},
]


def retrouve(question, source, pages, n=4):
    for _, meta, _ in rechercher(question, n):
        if meta["source"] == source and pages[0] <= meta["page"] <= pages[1]:
            return True
    return False


if __name__ == "__main__":
    contenu = [t for t in TESTS if t["source"]]
    hors_sujet = [t for t in TESTS if not t["source"]]

    ok = 0
    for t in contenu:
        trouve = retrouve(t["question"], t["source"], t["pages"])
        ok += trouve
        print("OK  " if trouve else "RATE", t["question"])
    print(f"\nRecherche : {ok}/{len(contenu)}")

    for t in hors_sujet + contenu[:5]:
        texte, sources = repondre(t["question"])
        print("\n" + "=" * 60)
        print("Q :", t["question"])
        print(texte)
        print("Sources :", sources)
