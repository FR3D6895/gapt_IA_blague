import openai
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import tempfile
import os

# 🔐 Clé API stockée dans secrets.toml
openai.api_key = st.secrets["openai"]["api_key"]

def generate_blague(theme, keywords):
    keywords_text = keywords.strip()
    if keywords_text:
        prompt = (f"Raconte une blague {theme}, drôle et originale, "
                  f"qui contient les mots-clés suivants : {keywords_text}. "
                  f"Cette blague vient d'une IA humoristique appelée Guillaume A Pété (G.A.PT).")
    else:
        prompt = (f"Raconte une blague {theme}, drôle et originale, "
                  f"comme si elle venait d'une IA humoristique appelée Guillaume A Pété (G.A.PT).")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es une IA humoristique qui raconte des blagues drôles."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def voix_humoristique(texte):
    tts = gTTS(text=texte, lang='fr')
    temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_mp3.name)

    voix = AudioSegment.from_mp3(temp_mp3.name)
    voix_vite = speedup(voix, playback_speed=1.3)
    voix_pitchee = voix_vite._spawn(voix_vite.raw_data, overrides={
        "frame_rate": int(voix_vite.frame_rate * 1.3)
    }).set_frame_rate(voix.frame_rate)

    final = voix_pitchee
    final_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    final.export(final_temp.name, format="mp3")

    temp_mp3.close()
    os.unlink(temp_mp3.name)

    return final_temp.name

# Interface Streamlit
st.title("🤖 G.A.PT. - Guillaume A Pété")
st.markdown("Une IA qui raconte des blagues absurdes et marrantes avec une voix rigolote 💨")

theme = st.selectbox("Choisis un thème de blague :", 
                     ["absurde", "informatique", "crado", "propre", "animaux", "historique", "dev"])

keywords = st.text_input("Entrez un ou plusieurs mots-clés séparés par des virgules (optionnel) :", "")

if st.button("Encore une !"):
    with st.spinner("Génération de la blague..."):
        blague = generate_blague(theme, keywords)
        st.write(f"💬 Blague ({theme}) :\n\n{blague}")

        audio_path = voix_humoristique(blague)
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

        audio_file.close()
        os.unlink(audio_path)
else:
    st.write("Clique sur **Encore une !** pour recevoir une blague.")
