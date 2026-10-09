
import ollama
from indexation import rechercher

MODELE_LLM = "llama3.2"  # mets le nom exact affiché par `ollama list`

SYSTEME = (
    "Tu es un assistant pédagogique. Réponds en français, uniquement à partir "
    "des extraits de cours fournis. Si la réponse n'y figure pas, dis-le "
    "clairement au lieu d'inventer."
)


def repondre(question, n=4):
    passages = rechercher(question, n)
    contexte = "\n\n".join(
        f"[{meta['source']}, page {meta['page']}]\n{texte}"
        for texte, meta, _ in passages
    )
    reponse = ollama.chat(
        model=MODELE_LLM,
        messages=[
            {"role": "system", "content": SYSTEME},
            {
                "role": "user",
                "content": f"Extraits de cours :\n{contexte}\n\nQuestion : {question}",
            },
        ],
    )
    sources = sorted({(m["source"], m["page"]) for _, m, _ in passages})
    return reponse["message"]["content"], sources


if __name__ == "__main__":
    while True:
        question = input("\nQuestion (q pour quitter) : ").strip()
        if question.lower() == "q":
            break
        texte, sources = repondre(question)
        print("\n" + texte)
        print("\nSources :", ", ".join(f"{s} p.{p}" for s, p in sources))


