import cloudinary
import cloudinary.uploader
from django.conf import settings
import requests
import time
import logging

# Set up logging
logger = logging.getLogger(__name__)

class API_Client:
    def __init__(self):
        self.secure = True
        self._configure()
    
    def _configure(self):
        """Configure Cloudinary with API credentials"""
        try:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=self.secure
            )
        except AttributeError as e:
            logger.error("Missing Cloudinary configuration in settings")
            raise Exception("Cloudinary configuration not found in settings")
    
    def upload_cloth_image(self, image, public_id="cloth"):
        """Upload cloth image to Cloudinary"""
        try:
            upload_result = cloudinary.uploader.upload(
                image,
                public_id=public_id
            )
            return upload_result
        except Exception as e:
            logger.error(f"Error uploading cloth image: {str(e)}")
            return None
    
    def upload_person_image(self, image, public_id="images"):
        """Upload person image to Cloudinary"""
        try:
            upload_result = cloudinary.uploader.upload(
                image,
                public_id=public_id
            )
            return upload_result
        except Exception as e:
            logger.error(f"Error uploading person image: {str(e)}")
            return None
    
    def fashion_api_client(self, person_image_path, cloth_image_path):
        """
        Process fashion try-on using Fashn.ai API
        
        Args:
            person_image_path: Path to person image
            cloth_image_path: Path to cloth image
            
        Returns:
            API response or error message
        """
        try:

    
            BASE_URL = "https://api.fashn.ai/v1"
            
            input_data = {
                "model_name": "tryon-v1.6",
                "inputs": {
                    "model_image": person_image_path,
                    "garment_image": cloth_image_path
                }
            }
            
            # Check if API key exists
            if not hasattr(settings, 'FASHN_API_KEY'):
                logger.error("FASHN_API_KEY not found in settings")
                return {"error": "API configuration error"}
                
            headers = {
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {settings.FASHN_API_KEY}"
            }
            
            # Run the model
            run_response = requests.post(f"{BASE_URL}/run", json=input_data, headers=headers)
            run_response.raise_for_status()  # Raise exception for bad status codes
            run_data = run_response.json()
            
            prediction_id = run_data.get('id')
            if not prediction_id:
                return {"error": "No prediction ID received"}
            
            # Poll for completion
            max_attempts = 1000  # Prevent infinite loop
            attempts = 0
            
            while attempts < max_attempts:
                try:
                    status_response = requests.get(f"{BASE_URL}/status/{prediction_id}", headers=headers)
                    status_response.raise_for_status()
                    status_data = status_response.json()
                    if status_data.get('status') == 'completed':
                        return status_data.get('output', {})
                                        
                    time.sleep(3)
                    attempts += 1
                    
                except requests.RequestException as e:
                    logger.error(f"Request error: {str(e)}")
                    return {"error": f"Request failed: {str(e)}"}
                    
            return {"error": "Request timeout"}
            
        except Exception as e:
            logger.error(f"Fashion API error: {str(e)}")
            return {"error": "Internal processing error"}