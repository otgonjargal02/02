import streamlit as st
import requests
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


API_URL = "http://localhost:8000"

st.title("Speaker Identification Demo")

menu = st.sidebar.selectbox("Menu", ["Add Speaker", "Identify Speaker"])

if menu == "Add Speaker":
    st.header("Add new Speaker")
    tag = st.text_input("Speaker Tag (name or id)")
    audio_file = st.file_uploader("Upload audio file (.wav or .mp3)", type=["wav","mp3","m4a"])

    if st.button("Add Speaker"):
        if not tag or not audio_file:
            st.warning("Please provide both tag and audio file.")
        else:
            files = {"audio": (audio_file.name, audio_file, audio_file.type)}
            data = {"tag": tag}
            resp = requests.post(f"{API_URL}/add_speaker/", files=files, data=data)
            if resp.status_code == 200:
                st.success(resp.json()["message"])
            else:
                st.error("Failed to add speaker")

elif menu == "Identify Speaker":
    st.header("Identify Speaker from Audio")
    audio_file = st.file_uploader("Upload audio file to identify", type=["wav","mp3","m4a"])

    if st.button("Identify"):
        if not audio_file:
            st.warning("Please upload an audio file.")
        else:
            files = {"file": (audio_file.name, audio_file.read(), audio_file.type)}
            try:
                response = requests.post(f"{API_URL}/identify/", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"🧠 Таныг '{result['tag']}' гэж танилаа!")
                    st.write(f"Ижил төстэй байдал (similarity): `{result['similarity']:.2f}`")
                else:
                    st.error(f"⚠️ Алдаа гарлаа: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"🚫 Холболтын алдаа: {e}")










            # resp = requests.post(f"{API_URL}/identify/", files=files,timeout=60)
            # if resp.status_code == 200:
            #     data = resp.json()
            #     st.write(f"Identified Tag: **{data['identified_tag']}**")
            #     st.write(f"Similarity: {data['similarity']:.4f}")
            # else:
            #     st.error("Failed to identify speaker")
