import numpy as np
from pathlib import Path
from resemblyzer import VoiceEncoder, preprocess_wav
import faiss
import pickle

class SpeakerIdentifier:
    def __init__(self):
        self.encoder = VoiceEncoder()
        self.index = faiss.IndexFlatL2(256)
        self.tags = []

    def add_audio(self, file_path: str, tag: str):
        wav = preprocess_wav(Path(file_path))
        emb = self.encoder.embed_utterance(wav)
        emb = np.expand_dims(emb, axis=0).astype("float32")
        self.index.add(emb)
        self.tags.append(tag)

    def identify(self, file_path,threshold=0.6):
        embedding = self._get_embedding(file_path)
        D, I = self.index.search(np.array([embedding]), k=1)
        idx = I[0][0]
        similarity = D[0][0]

        #if idx >= len(self.tags):
           # return "Unknown", 0.0
        if similarity > threshold:
            return "unknown", similarity
        return self.tags[idx], similarity

    def _get_embedding(self, file_path):
        wav = preprocess_wav(Path(file_path))
        return self.encoder.embed_utterance(wav).astype("float32")

    def save(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump((self.index, self.tags), f)

    def load(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.index, self.tags = pickle.load(f)
