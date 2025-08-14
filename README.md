# EXE201 - Virtual Try-On System

## Project Description
AI-powered virtual try-on system that allows users to try clothes on their photos.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: VITON-HD
- **Database**: SQLite

## Installation and Setup

### System Requirements
- Python 3.8+
- pip

### Installation
1. Clone repository:
```bash
git clone <repository-url>
cd EXE201_frontend_backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to use the application.

## Project Structure
```
EXE201_frontend_backend/
├── VTON/                 # Django settings and config
├── home/                 # Main app
├── user/                 # User management app
├── admin_site/           # Admin dashboard
├── AI/                   # AI models and logic
├── media/                # Upload files
├── staticfiles/          # Static files
└── requirements.txt      # Python dependencies
```

## Main Features
- User registration/login
- Image upload and virtual try-on
- Profile and payment management
- Admin dashboard
- AI-powered virtual try-on

## Author
EXE201 Team

# AI Models

## VITON-HD Models

AI model files have been excluded from the Git repository due to large size (>100MB).

### Download Models

To use the system, you need to download the following model files to the `AI/VITON_HD/checkpoints/` directory:

1. **alias_final.pth** (384MB) - Alias generation model
2. **gmm_final.pth** (73MB) - Geometric matching model  
3. **seg_final.pth** (132MB) - Segmentation model

### How to Download Models:

#### Option 1: Download from Google Drive
- Link: [VITON-HD Models](https://drive.google.com/drive/folders/...)
- Download and extract to the `AI/VITON_HD/checkpoints/` directory

#### Option 2: Download from Hugging Face
```bash
# Install huggingface_hub
pip install huggingface_hub

# Download models
python -c "
from huggingface_hub import hf_hub_download
import os

os.makedirs('AI/VITON_HD/checkpoints/', exist_ok=True)

models = [
    'alias_final.pth',
    'gmm_final.pth', 
    'seg_final.pth'
]

for model in models:
    hf_hub_download(
        repo_id='your-repo/viton-hd',
        filename=f'checkpoints/{model}',
        local_dir='AI/VITON_HD/'
    )
"
```

#### Option 3: Manual Download
- Download from VITON-HD homepage: https://github.com/levindabhi/VITON-HD
- Place the files in the `AI/VITON_HD/checkpoints/` directory

### Directory Structure After Download:
```
AI/VITON_HD/checkpoints/
├── alias_final.pth
├── gmm_final.pth
└── seg_final.pth
```

### Notes:
- These model files are very large (>500MB total)
- Ensure sufficient hard drive space
- These models are used for virtual try-on functionality 