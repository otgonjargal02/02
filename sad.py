import requests

url = "http://127.0.0.1:8000/identify/"
files = {"file": open(r"C:\Users\otgon\OneDrive\Documents\Sound Recordings\Recording (2).wav", "rb")}
response = requests.post(url, files=files)

print(response.json())

# otgoo.wav, batka.wav, sara.wav гэх мэт
requests.post("http://127.0.0.1:8000/add_speaker/", files={"audio": open("batka.wav", "rb")}, data={"tag": "batka"})


uploaded_file = r"C:\Users\otgon\OneDrive\Documents\Sound Recordings\Recording (2).wav"

files = {'file': open(r"C:\Users\otgon\OneDrive\Documents\Sound Recordings\Recording (2).wav"
                      , "rb")}
response = requests.post("http://127.0.0.1:8000/identify/", files=files)

print(response.json())



#python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
#python -m streamlit run app_streamlit.py
