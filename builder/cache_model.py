import torch
from diffusers import DiffusionPipeline

def download_model():
    model_id = "Lightricks/LTX-2"
    print(f"Downloading model: {model_id}")
    pipe = DiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    )
    print("Model downloaded successfully.")

if __name__ == "__main__":
    download_model()
