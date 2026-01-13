import torch
try:
    from diffusers import LTXVideoPipeline
except ImportError:
    from diffusers import LTXPipeline as LTXVideoPipeline

def download_model():
    model_id = "Lightricks/LTX-2"
    print(f"Downloading model: {model_id}")
    pipe = LTXVideoPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16
    )
    print("Model downloaded successfully.")

if __name__ == "__main__":
    download_model()
