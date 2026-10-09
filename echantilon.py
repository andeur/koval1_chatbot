import random
from main import charger_cours

random.seed(1)
docs = charger_cours()

par_source = {}
for d in docs:
    par_source.setdefault(d["source"], []).append(d)

for source, pages in par_source.items():
    for d in random.sample(pages, min(3, len(pages))):
        print("=" * 60)
        print(f"{source}, page {d['page']}")
        print(d["texte"][:600])