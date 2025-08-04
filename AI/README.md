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