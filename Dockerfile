FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg is crucial for video export)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up cache directories for RunPod persistent volume
ENV HF_HOME=/workspace/hf \
    HUGGINGFACE_HUB_CACHE=/workspace/hf/hub \
    TRANSFORMERS_CACHE=/workspace/hf/transformers \
    TORCH_HOME=/workspace/torch \
    XDG_CACHE_HOME=/workspace/.cache \
    TMPDIR=/workspace/tmp

# Create these directories
RUN mkdir -p /workspace/hf/hub /workspace/hf/transformers /workspace/torch /workspace/.cache /workspace/tmp

WORKDIR /app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cache the model during build
COPY builder/ builder/
# This step downloads the model so it's baked into the image. 
# It might take a while and increase image size significantly.
# RUN python builder/cache_model.py

# Copy source code
COPY src/ src/

CMD ["python", "-u", "src/handler.py"]
