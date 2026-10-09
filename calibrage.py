import json
from indexation import rechercher

with open("tests.json", encoding="utf-8") as f:
    TESTS = json.load(f)


def meilleure_distance(question):
    return rechercher(question, 1)[0][2]


print("Questions de cours :")
for t in TESTS:
    print(f"  {meilleure_distance(t['question']):.3f}  {t['question'][:70]}")

print("\nHors sujet :")
for q in ["Quelle est la capitale de la France ?",
          "Comment préparer une pizza margherita ?",
          "Qui a gagné la Coupe du monde 2018 ?"]:
    print(f"  {meilleure_distance(q):.3f}  {q}")


print("\nMes reformulations :")
for q in [
    "C'est quoi un classifieur bayésien ?",
    "À quoi sert RDF ?",
    "Comment un agent BDI choisit-il ses actions ?",
    "Quelle différence entre apprentissage supervisé et non supervisé ?",
    "Comment on représente des connaissances dans un ordinateur ?",
]:
    print(f"  {meilleure_distance(q):.3f}  {q}")