from pathlib import Path
import pickle

import faiss
import numpy as np
import librosa

from embed import ClapEmbedder

DATASET_DIR = Path("../dataset")
INDEX_DIR = Path("index")

INDEX_DIR.mkdir(exist_ok=True)

embedder = ClapEmbedder()

embeddings = []
metadata = []

print("\nBuilding index...\n")

for audio_file in DATASET_DIR.rglob("*.wav"):

    print(audio_file.name)

    embedding = embedder.embed_audio(str(audio_file))

    embeddings.append(embedding)

    duration = librosa.get_duration(path=str(audio_file))

    metadata.append(
        {
            "id": len(metadata),
            "instrument": audio_file.parent.name,
            "filename": audio_file.name,
            "path": str(audio_file),
            "duration": round(duration, 3),
            "sample_rate": 48000
        }
    )

embeddings = np.asarray(
    embeddings,
    dtype=np.float32
)

print("\nEmbedding matrix:", embeddings.shape)

# Normalize so Inner Product == Cosine Similarity
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    str(INDEX_DIR / "audio.index")
)

with open(
    INDEX_DIR / "metadata.pkl",
    "wb"
) as f:
    pickle.dump(metadata, f)

print("\nDone!")
print("Indexed:", index.ntotal)