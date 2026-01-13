import runpod
import torch
import os
import uuid
import logging
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
from src.utils import upload_file_to_supabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
pipe = None

def init_model():
    global pipe
    if pipe is None:
        model_id = "Lightricks/LTX-2"
        logger.info(f"Loading model: {model_id}")
        pipe = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        pipe.to("cuda")
        logger.info("Model loaded successfully")

def handler(job):
    global pipe
    job_input = job['input']
    
    # Input validation and defaults
    prompt = job_input.get('prompt')
    if not prompt:
        return {"error": "Missing 'prompt' in input"}
        
    negative_prompt = job_input.get('negative_prompt', "worst quality, inconsistent motion, blurry, jittery, distorted")
    width = job_input.get('width', 768)
    height = job_input.get('height', 512)
    num_frames = job_input.get('num_frames', 121)
    num_inference_steps = job_input.get('num_inference_steps', 50)
    guidance_scale = job_input.get('guidance_scale', 3.0)
    seed = job_input.get('seed', None)
    
    # Check for Supabase config
    bucket_name = os.environ.get('SUPABASE_BUCKET', 'videos') # Default to 'videos' bucket

    # Set seed if provided
    generator = None
    if seed:
        generator = torch.manual_seed(int(seed))

    try:
        logger.info("Starting generation")
        output = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        video_frames = output.frames[0]
        
        # Save locally
        output_filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join("/tmp", output_filename)
        export_to_video(video_frames, output_path, fps=24)
        logger.info(f"Video saved to {output_path}")

        # Upload to Supabase
        logger.info(f"Uploading to Supabase bucket: {bucket_name}")
        from src.utils import upload_file_to_supabase
        video_url = upload_file_to_supabase(output_path, bucket_name, object_name=output_filename)
        
        # Cleanup
        if os.path.exists(output_path):
            # os.remove(output_path) # Keep for debugging if needed, or remove
            os.remove(output_path)
            
        return {"video_url": video_url}

    except Exception as e:
        logger.error(f"Error during generation: {e}")
        return {"error": str(e)}

# Initialize model on cold start
init_model()

runpod.serverless.start({"handler": handler})
