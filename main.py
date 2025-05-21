from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from speaker_id import SpeakerIdentifier
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
app = FastAPI()
sid = SpeakerIdentifier()

DATA_DIR = "data"
MODEL_FILE = "speaker_model.pkl"

os.makedirs(DATA_DIR, exist_ok=True)

if os.path.exists(MODEL_FILE):
    sid.load(MODEL_FILE)

@app.post("/add_speaker/")
async def add_speaker(tag: str = Form(...), audio: UploadFile = File(...)):
    file_location = os.path.join(DATA_DIR, audio.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    sid.add_audio(file_location, tag)
    sid.save(MODEL_FILE)
    return {"message": f"Speaker {tag} added successfully."}

@app.post("/identify/")
async def identify(file: UploadFile = File(...)):
   #file_path = f"temp_{file.filename}"
    file_path =os.path.join(DATA_DIR,file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
   #with open(file_path, "wb") as f:
      # f.write(await file.read())

    tag, similarity = sid.identify(file_path)
  # os.remove(file_path)
    return {"tag": tag, "similarity": float(similarity)}

