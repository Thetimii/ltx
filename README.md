# LTX-2 (LTX-Video) on RunPod Serverless

This worker deploys the [Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video) model to RunPod Serverless. It generates a video from a text prompt and uploads the result to S3, returning a presigned URL.

## Prerequisites

- **RunPod Account**: You need a RunPod account.
- **AWS S3 Bucket**: You need an S3 bucket (or compatible storage like Cloudflare R2, Wasabi) to store the generated videos.
- **GitHub Account**: To push this code and build the image via RunPod's integration.

## Setup Instructions

### 1. Push to GitHub
Initialize a git repository and push this code.
```bash
git init
git add .
git commit -m "Initial commit of LTX-2 worker"
# Add your remote
# git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
# git push -u origin main
```

### 2. Configure RunPod
1. Go to **RunPod Serverless**.
2. Create a **New Template**.
3. **Container Image**: Choose "Build only" or verify if you can point it to your GitHub repo so it builds automatically. Alternatively, build this image locally and push to Docker Hub, then use that image name.
   - *Recommendation*: Use RunPod's GitHub integration to build the image for you.
4. **Environment Variables**: Add the following keys:
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key.
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Key.
   - `AWS_BUCKET_NAME`: The name of your bucket.
   - `AWS_REGION`: (Optional) Region of your bucket (default: `us-east-1`).

### 3. Create Endpoint
1. Deploy the template to a GPU worker (Recommended: **RTX 3090** or **RTX 4090** or **A100**).
   - This model requires roughly 20-24GB VRAM for bf16 inference with offloading, so an A6000 or A100 is safest, but optimization might fit it on 24GB cards.
2. Wait for the image to build (this will take a while as it downloads the large model during build).

### 4. API Usage
**Request Payload:**
```json
{
  "input": {
    "prompt": "A cinematic drone shot of a futuristic cyberpunk city at night, rain falling, neon lights reflecting",
    "negative_prompt": "low quality, blurry",
    "width": 768,
    "height": 512,
    "num_frames": 121,
    "step": 50
  }
}
```

**Response:**
```json
{
  "video_url": "https://your-bucket.s3.amazonaws.com/uuid.mp4?..."
}
```
