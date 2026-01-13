import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")
    return create_client(url, key)

def upload_file_to_supabase(file_path, bucket_name, object_name=None):
    """Upload a file to Supabase Storage and return the public URL."""
    
    if object_name is None:
        object_name = os.path.basename(file_path)

    supabase = get_supabase_client()
    
    try:
        with open(file_path, 'rb') as f:
            # upsert=True to overwrite if exists
            supabase.storage.from_(bucket_name).upload(
                path=object_name,
                file=f,
                file_options={"content-type": "video/mp4", "upsert": "true"}
            )
            
        # Get public URL
        # Ensure your bucket is set to Public in Supabase dashboard
        public_url = supabase.storage.from_(bucket_name).get_public_url(object_name)
        return public_url
        
    except Exception as e:
        logger.error(f"Failed to upload to Supabase: {e}")
        return None
