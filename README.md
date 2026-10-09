# Chatbot RAG sur mes cours

Assistant qui répond aux questions à partir de mes PDF de cours, en citant la source (fichier et page). Tout tourne en local.

## Fonctionnement
1. Extraction du texte des PDF (pypdf)
2. Découpage en passages de 200 mots avec chevauchement de 40
3. Embeddings avec `intfloat/multilingual-e5-small`, stockés dans ChromaDB
4. À chaque question : recherche des passages les plus proches, filtrés par un seuil de distance
5. Génération de la réponse avec un LLM local (Ollama), limité aux extraits fournis

## Évaluation
- 20 questions générées à partir de passages tirés au hasard dans 8 PDF : le bon passage est retrouvé dans X/Y cas
- Questions hors sujet : refusées dans 3 cas sur 3
- Seuil de distance fixé à 0,18 après calibrage (questions de cours : 0,10 à 0,16 ; hors sujet : 0,19 à 0,24)

## Limites
- Les questions de test sont générées à partir des passages, donc le score de recherche est probablement optimiste
- Les formules mathématiques sont mal extraites des PDF
- Chaque question est traitée seule, sans mémoire de la conversation
- Le seuil est calibré sur peu d'exemples

## Lancer le projet
```bash
pip install -r requirements.txt
ollama pull <ton_modèle>
python indexation.py
streamlit run interface_apk.py
```
