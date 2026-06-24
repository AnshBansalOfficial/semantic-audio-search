import torch
from transformers import ClapProcessor, ClapModel
from preprocess import preprocess_audio


class ClapEmbedder:
    def __init__(self):
        print("Loading CLAP model...")

        self.processor = ClapProcessor.from_pretrained(
            "laion/clap-htsat-unfused"
        )

        self.model = ClapModel.from_pretrained(
            "laion/clap-htsat-unfused"
        )

        self.model.eval()

        print("CLAP loaded.\n")

    def embed_audio(self, audio_path):
        audio, sr = preprocess_audio(audio_path)

        inputs = self.processor(
            audio=audio,
            sampling_rate=sr,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model.get_audio_features(**inputs)

        return outputs.pooler_output.squeeze().cpu().numpy()
    
    def embed_text(self, text):
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs)

        return outputs.pooler_output.squeeze().cpu().numpy()