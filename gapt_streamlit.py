import streamlit as st
import google.generativeai as genai

# 🔐 Clé API stockée dans secrets.toml
genai.configure(api_key=st.secrets["gemini_api_key"])


def generate_blague(theme, keywords):
    keywords_text = keywords.strip()
    if keywords_text:
        prompt = (f"Raconte une blague {theme}, drôle et originale, "
                  f"qui contient les mots-clés suivants : {keywords_text}. "
                  f"Cette blague vient d'une IA humoristique appelée Guillaume A Pété (G.A.PT) 💨.")
    else:
        prompt = (f"Raconte une blague {theme}, drôle et originale, "
                  f"comme si elle venait d'une IA humoristique appelée Guillaume A Pété (G.A.PT) 💨.")

    # syntaxe client 
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Interface Streamlit
st.title("🤖 G.A.PT. - Guillaume A Pété")
st.markdown("Une IA qui raconte des blagues absurdes et marrantes 💬")

theme = st.selectbox("Choisis un thème de blague :", 
                     ["Chuck Norris", "absurde", "informatique", "drôle", "propre", "animaux", "historique", "dev"])

keywords = st.text_input("Entrez un ou plusieurs mots-clés séparés par des virgules (optionnel) :", "")

if st.button("Encore une !"):
    with st.spinner("Génération de la blague..."):
        blague = generate_blague(theme, keywords)
        st.success("😄 Blague générée avec succès !")
        st.write(f"💬 Blague ({theme}) :\n\n{blague}")


else:
    st.write("Clique sur **Encore une !** pour recevoir une blague.")
