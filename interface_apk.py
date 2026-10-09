import streamlit as st

from chatbot import repondre

st.set_page_config(page_title="Chatbot de cours")
st.title("Chatbot de cours")
st.caption("Pose une question : les réponses viennent uniquement de tes PDF.")

if "historique" not in st.session_state:
    st.session_state.historique = []

if st.sidebar.button("Effacer la conversation"):
    st.session_state.historique = []
    st.rerun()


def afficher_sources(sources):
    if sources:
        with st.expander("Sources"):
            for source, page in sources:
                st.write(f"{source}, page {page}")


# Réaffiche toute la conversation à chaque rafraîchissement de la page
for msg in st.session_state.historique:
    with st.chat_message(msg["role"]):
        st.markdown(msg["contenu"])
        afficher_sources(msg.get("sources"))

question = st.chat_input("Ta question...")
if question:
    st.session_state.historique.append({"role": "user", "contenu": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les cours..."):
            texte, sources = repondre(question)
        st.markdown(texte)
        afficher_sources(sources)

    st.session_state.historique.append(
        {"role": "assistant", "contenu": texte, "sources": sources}
    )