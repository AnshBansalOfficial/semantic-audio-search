# ◈ Semantic Audio Search

> Retrieve music samples by meaning — not by name.

An AI-powered retrieval engine built on **CLAP embeddings** and **FAISS**. Describe a sound in plain language, or upload a reference clip — the engine finds what matches, acoustically and semantically.

No filenames. No metadata. Just the audio itself.

---

## How It Works

### Text → Audio

```
"short punchy electronic kick"
        ↓
   CLAP Text Encoder
        ↓
   512-D Embedding
        ↓
   FAISS Index Search
        ↓
kick-808.wav  ▸  kick-deep.wav  ▸  kick-electro01.wav
```

### Audio → Audio

```
my_kick.wav  (uploaded)
        ↓
   CLAP Audio Encoder
        ↓
   512-D Embedding
        ↓
   FAISS Index Search
        ↓
kick-808.wav  ▸  kick-deep.wav  ▸  kick-classic.wav
```

Text and audio embeddings live in the **same 512-dimensional space** — one index handles both query modes.

---

## Indexing Pipeline

Each sample is preprocessed before embedding:

```
kick.wav
  │
  ├─ Resample → 48 kHz
  ├─ Mono conversion
  ├─ Trim silence
  └─ Peak normalize
        ↓
  CLAP Audio Encoder
        ↓
  512-D Vector  →  FAISS Index
                →  metadata.pkl  (filename, instrument, duration, path)
```

---

## Features

- Semantic **text-to-audio** search via natural language
- Semantic **audio-to-audio** similarity search
- LAION CLAP multimodal embeddings
- Fast nearest-neighbor retrieval with FAISS
- Automatic audio preprocessing (resample, trim, normalize)
- Streamlit UI for interactive exploration
- Embedding model cached for low-latency inference

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Audio Processing | Librosa |
| Deep Learning | PyTorch |
| Embedding Model | LAION CLAP |
| Vector Search | FAISS |
| Transformers | HuggingFace Transformers |

---

## Project Structure

```
.
├── backend/
│   ├── app.py          ← Streamlit interface
│   ├── embed.py        ← CLAP embedding logic
│   ├── preprocess.py   ← Audio normalization pipeline
│   ├── search.py       ← FAISS query handling
│   ├── build_index.py  ← Index construction
│   └── index/
│       ├── audio.index
│       └── metadata.pkl
│
├── dataset/
│   ├── kick/
│   ├── snare/
│   ├── clap/
│   └── hat/
│
└── README.md
```

---

## Setup

```bash
# Clone
git clone https://github.com/<your-username>/ai-music-sample-search.git
cd ai-music-sample-search

# Environment
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
```

---

## Build & Run

```bash
# Build the FAISS index
python build_index.py
# → generates index/audio.index and index/metadata.pkl

# Launch the app
streamlit run app.py
```

---

## Dataset

The prototype indexes ~40 drum samples across four classes: **kick, snare, clap, hi-hat**.

The retrieval pipeline is dataset-agnostic — scaling to thousands of samples requires only rebuilding the FAISS index.

---

## Planned

- [ ] Cloudflare R2 object storage
- [ ] FastAPI backend
- [ ] React / Next.js frontend
- [ ] Metadata filtering — BPM, genre, key
- [ ] Waveform visualization
- [ ] Approximate indexing — IVF / HNSW
- [ ] Real-time sample ingestion

---

## What This Explores

CLAP (Contrastive Language-Audio Pretraining) projects both text and audio into a shared embedding space. This project applies that to sample retrieval: instead of tagging files manually, the system understands acoustic and semantic similarity directly from the signal.

The result is a search experience closer to how producers actually think — *"something dark and metallic"* — rather than how file systems are organized.

---

## License

MIT