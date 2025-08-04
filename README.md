# EXE201 - Virtual Try-On System

## Mô tả dự án
Hệ thống thử đồ ảo sử dụng AI để cho phép người dùng thử quần áo trên ảnh của mình.

## Công nghệ sử dụng
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: VITON-HD
- **Database**: SQLite

## Cài đặt và chạy dự án

### Yêu cầu hệ thống
- Python 3.8+
- pip

### Cài đặt
1. Clone repository:
```bash
git clone <repository-url>
cd EXE201_frontend_backend
```

2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Trên Linux/Mac
# hoặc
venv\Scripts\activate  # Trên Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy migrations:
```bash
python manage.py migrate
```

5. Tạo superuser (tùy chọn):
```bash
python manage.py createsuperuser
```

6. Chạy server:
```bash
python manage.py runserver
```

Truy cập http://localhost:8000 để sử dụng ứng dụng.

## Cấu trúc dự án
```
EXE201_frontend_backend/
├── VTON/                 # Django settings và config
├── home/                 # App chính
├── user/                 # App quản lý user
├── admin_site/           # Admin dashboard
├── AI/                   # AI models và logic
├── media/                # Upload files
├── staticfiles/          # Static files
└── requirements.txt      # Python dependencies
```

## Tính năng chính
- Đăng ký/Đăng nhập người dùng
- Upload ảnh và thử đồ ảo
- Quản lý profile và thanh toán
- Admin dashboard
- AI-powered virtual try-on

## Tác giả
EXE201 Team

# AI Models

## VITON-HD Models

Các file model AI đã được loại trừ khỏi Git repository do kích thước lớn (>100MB).

### Tải models

Để sử dụng hệ thống, bạn cần tải các file model sau vào thư mục `AI/VITON_HD/checkpoints/`:

1. **alias_final.pth** (384MB) - Alias generation model
2. **gmm_final.pth** (73MB) - Geometric matching model  
3. **seg_final.pth** (132MB) - Segmentation model

### Cách tải models:

#### Option 1: Tải từ Google Drive
- Link: [VITON-HD Models](https://drive.google.com/drive/folders/...)
- Tải và giải nén vào thư mục `AI/VITON_HD/checkpoints/`

#### Option 2: Tải từ Hugging Face
```bash
# Cài đặt huggingface_hub
pip install huggingface_hub

# Tải models
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

#### Option 3: Tải thủ công
- Tải từ trang chủ VITON-HD: https://github.com/levindabhi/VITON-HD
- Đặt các file vào thư mục `AI/VITON_HD/checkpoints/`

### Cấu trúc thư mục sau khi tải:
```
AI/VITON_HD/checkpoints/
├── alias_final.pth
├── gmm_final.pth
└── seg_final.pth
```

### Lưu ý:
- Các file model này rất lớn (>500MB tổng cộng)
- Đảm bảo có đủ dung lượng ổ cứng
- Models này được sử dụng cho virtual try-on functionality 