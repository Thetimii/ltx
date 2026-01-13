FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg is crucial for video export)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

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
