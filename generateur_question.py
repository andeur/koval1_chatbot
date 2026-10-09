import json
import random
from itertools import cycle

import ollama

from main import charger_cours
from chunking import creer_chunks
from chatbot import MODELE_LLM

NB_QUESTIONS = 20
random.seed(42)

PROMPT = (
    "Voici un extrait de cours. Écris UNE seule question en français, claire et "
    "compréhensible sans l'extrait, dont la réponse se trouve dans cet extrait. "
    "Ne mentionne pas « l'extrait » ni « le texte ». "
    "Réponds uniquement par la question.\n\nExtrait :\n{texte}"
)

# Chunks assez longs, regroupés par PDF, puis tirage à tour de rôle entre les PDF
chunks = [c for c in creer_chunks(charger_cours()) if len(c["texte"].split()) >= 80]
par_source = {}
for c in chunks:
    par_source.setdefault(c["source"], []).append(c)
for liste in par_source.values():
    random.shuffle(liste)

choisis = []
for source in cycle(list(par_source)):
    if len(choisis) >= NB_QUESTIONS or not any(par_source.values()):
        break
    if par_source[source]:
        choisis.append(par_source[source].pop())

tests = []
for c in choisis:
    rep = ollama.chat(
        model=MODELE_LLM,
        messages=[{"role": "user", "content": PROMPT.format(texte=c["texte"])}],
    )
    question = rep["message"]["content"].strip().split("\n")[0]
    tests.append({
        "question": question,
        "source": c["source"],
        "pages": [c["page"] - 1, c["page"] + 1],
    })
    print(f"{len(tests)}. [{c['source']} p.{c['page']}] {question}")

with open("tests.json", "w", encoding="utf-8") as f:
    json.dump(tests, f, ensure_ascii=False, indent=2)
print("\ntests.json créé")