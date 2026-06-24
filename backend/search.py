import pickle
from pathlib import Path

import faiss
import numpy as np

from embed import ClapEmbedder


BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index" / "audio.index"
METADATA_PATH = BASE_DIR / "index" / "metadata.pkl"

TOP_K = 5


def _resolve_sample_path(path):
    sample_path = Path(path)

    if sample_path.is_absolute():
        return str(sample_path)

    return str((BASE_DIR / sample_path).resolve())


class AudioSearchEngine:

    def __init__(self):
        self.embedder = ClapEmbedder()

        self.index = faiss.read_index(str(INDEX_PATH))

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search_audio(self, audio_path):

        embedding = self.embedder.embed_audio(audio_path)

        embedding = np.asarray(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(embedding)

        scores, indices = self.index.search(
            embedding,
            TOP_K
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            sample = dict(self.metadata[idx])
            sample["path"] = _resolve_sample_path(sample["path"])

            results.append({
                "score": float(score),
                "instrument": sample["instrument"],
                "filename": sample["filename"],
                "path": sample["path"]
            })

        return results
    
    def search_text(self, query):

        embedding = self.embedder.embed_text(query)

        embedding = np.asarray(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(embedding)

        scores, indices = self.index.search(
            embedding,
            TOP_K
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            sample = dict(self.metadata[idx])
            sample["path"] = _resolve_sample_path(sample["path"])

            results.append({
                "score": float(score),
                **sample
            })

        return results


if __name__ == "__main__":

    engine = AudioSearchEngine()

    print("\nText Search\n")

    results = engine.search_text(
        "short punchy electronic kick"
    )

    for r in results:

        print(
            f"{r['filename']:25}"
            f"{r['instrument']:10}"
            f"{r['duration']:>6}s   "
            f"{r['score']:.3f}"
        )

    
