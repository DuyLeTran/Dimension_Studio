import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

cloud_path = "/Users/tranleduy/FPT_AI_Project/8_EXE201/Dimension_Studio/media/avt_Anh Tuan.png"
person_path = "/Users/tranleduy/FPT_AI_Project/8_EXE201/Dimension_Studio/media/avt_Minh_Thanh.png"

# Configuration       
cloudinary.config( 
    cloud_name = "dghiu2vxd", 
    api_key = "842162347375429", 
    api_secret = 'EPoT1gbLNlGjLtImf5cIvugAfjk', # Click 'View API Keys' above to copy your API secret
    secure=True
)

# Upload an image
upload_cloth = cloudinary.uploader.upload(cloud_path,
                                           public_id="cloth")

upload_image = cloudinary.uploader.upload(person_path,
                                           public_id="images")
print(upload_cloth["secure_url"], '\n',
     upload_image["secure_url"])