# 🎵 AI Music Sample Search

An AI-powered semantic music sample retrieval engine that enables **text-to-audio** and **audio-to-audio** search using **CLAP embeddings** and **FAISS**.

Instead of relying on filenames or metadata, the system retrieves acoustically and semantically similar samples by searching in a shared embedding space.

---

## Demo

### Text Search

```
Query:
"short punchy electronic kick"

↓

Top Results

kick-808.wav
kick-deep.wav
kick-electro01.wav
kick-classic.wav
...
```

### Audio Search

```
Upload:

my_kick.wav

↓

Top Results

kick-808.wav
kick-deep.wav
kick-classic.wav
...
```

---

## Features

- Semantic text-to-audio search
- Audio similarity search
- CLAP multimodal embeddings
- Fast nearest-neighbor retrieval using FAISS
- Automatic audio preprocessing
- Streamlit interface for interactive search
- Cached embedding model for low-latency inference

---

## Project Architecture

```
                  User

                    │

         ┌──────────┴──────────┐
         │                     │

    Text Query          Audio Upload

         │                     │
         └──────────┬──────────┘

                    ▼

            CLAP Embedding Model

                    ▼

             512-D Embedding

                    ▼

                FAISS Index

                    ▼

             Top-K Neighbors

                    ▼

         Metadata Lookup

                    ▼

             Audio Playback
```

---

## How It Works

### 1. Build the Index

Each audio sample is

- Loaded
- Resampled to 48 kHz
- Converted to mono
- Trimmed
- Peak normalized

The preprocessed waveform is passed through CLAP to generate a **512-dimensional embedding**.

```
kick.wav
      │
      ▼
Audio Preprocessing
      │
      ▼
CLAP Audio Encoder
      │
      ▼
512-D Vector
      │
      ▼
FAISS Index
```

Metadata such as filename, instrument, duration, and file path is stored separately.

---

### 2. Audio Search

```
Upload Audio

↓

CLAP Audio Encoder

↓

512-D Query Vector

↓

FAISS Similarity Search

↓

Top Matching Samples
```

---

### 3. Text Search

```
Text Prompt

↓

CLAP Text Encoder

↓

512-D Query Vector

↓

FAISS Similarity Search

↓

Top Matching Audio Samples
```

Both text and audio embeddings exist in the same semantic embedding space, enabling multimodal retrieval using a single vector index.

---

## Tech Stack

| Component | Technology |
|------------|------------|
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
├── backend
│   ├── app.py
│   ├── embed.py
│   ├── preprocess.py
│   ├── search.py
│   ├── build_index.py
│   └── index
│       ├── audio.index
│       └── metadata.pkl
│
├── dataset
│   ├── kick
│   ├── snare
│   ├── clap
│   └── hat
│
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/ai-music-sample-search.git

cd ai-music-sample-search
```

Create a virtual environment

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Build the Vector Index

```bash
python build_index.py
```

This generates

```
audio.index
metadata.pkl
```

inside the `index/` directory.

---

## Run the Application

```bash
streamlit run app.py
```

---

## Dataset

The prototype currently indexes approximately **40 drum samples** across four instrument classes:

- Kick
- Snare
- Clap
- Hi-Hat

The retrieval pipeline is independent of dataset size and can be extended to thousands of samples by rebuilding the FAISS index.

---

## Future Improvements

- Cloudflare R2 object storage
- FastAPI backend
- React / Next.js frontend
- Metadata filtering (BPM, genre, key)
- Waveform visualization
- Approximate indexing (IVF / HNSW)
- Real-time sample ingestion
- Larger production-scale dataset

---

## Key Learnings

This project explores practical applications of multimodal representation learning by combining pretrained CLAP embeddings with vector similarity search. It demonstrates how text and audio can be projected into a shared embedding space, enabling semantic retrieval without relying on filenames or manually curated metadata.

---

## License

MIT License