import torch
import torch.nn.functional as F
import cv2
import numpy as np
from torchvision import transforms
from .network import SegGenerator, GMM, ALIASGenerator
from types import SimpleNamespace
from PIL import Image
import copy

class VITONHDNet:
    def __init__(self, DEVICE):

        self.device = DEVICE
        self.opt    = self.build_opt()       # semantic_nc = 13
        self.T      = self.reprocess_utils()
        self._model = None

        # ❶ SegGenerator — 21⇢13 kênh (hoàn toàn trùng ckpt)
        self.seg   = SegGenerator(self.opt,
                                  input_nc=self.opt.semantic_nc + 8,   # 13+8=21
                                  output_nc=self.opt.semantic_nc       # 13
                                 ).to(self.device)

        # ❷ GMM — 7⇢3 kênh (trùng ckpt)
        self.gmm   = GMM(self.opt, inputA_nc=7, inputB_nc=3).to(self.device)

        # ❸ ALIASGenerator — pha “hack” semantic_nc = 7
        alias_opt            = copy.deepcopy(self.opt)
        alias_opt.semantic_nc = 7                         # **** quan trọng
        self.alias = ALIASGenerator(alias_opt, input_nc=9).to(self.device)
        
    def build_opt(self):
        return SimpleNamespace(
            load_height = 1024,
            load_width  = 768,
            grid_size   = 5,
            init_type   = 'none',
            init_variance = 0.02,

            # ---------- SỬA ĐÚNG THAM SỐ ----------
            ngf = 64,
            norm_G = 'spectralaliasinstance',   # must include 'spectral'
            num_upsampling_layers = 'most',     # checkpoint dùng 'most'
            semantic_nc = 13,                   # 13 lớp theo ckpt
            # --------------------------------------

            seg_model_path   = 'AI/VITON_HD/checkpoints/seg_final.pth',
            gmm_model_path   = 'AI/VITON_HD/checkpoints/gmm_final.pth',
            alias_model_path = 'AI/VITON_HD/checkpoints/alias_final.pth'
        )
    
    def reprocess_utils(self):
        return transforms.Compose([
            transforms.Resize((self.opt.load_height, self.opt.load_width)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])
    
    def img2tensor(self, path:str):
        return self.T(Image.open(path).convert('RGB')).unsqueeze(0).to(self.device)
    
    def tensor2img(self, tensor: torch.Tensor):
        """
        (-1 … 1) Tensor  ➜  PIL.Image
        """
        t = (tensor.clamp(-1, 1) * 0.5 + 0.5) * 255          # về thang 0‒255
        arr = (
            t[0]                       # (C,H,W)
            .permute(1, 2, 0)          # (H,W,C)
            .detach()                  # <-- tách khỏi graph
            .cpu()
            .numpy()
            .astype("uint8")
        )
        return np.array(arr)

    def load_model(self):
        if self._model is not None:
            return self._model
        
        self.seg.load_state_dict(torch.load(self.opt.seg_model_path, map_location=self.device))
        self.gmm.load_state_dict(torch.load(self.opt.gmm_model_path, map_location=self.device))
        self.alias.load_state_dict(torch.load(self.opt.alias_model_path, map_location=self.device))
        
        self.seg.eval()
        self.gmm.eval()
        self.alias.eval()
        self._model = (self.seg, self.gmm, self.alias, self.opt)
        return self._model

    # def viton_tryon(self, person_path: str, cloth_path: str):
    #     """
    #     Pipeline tối thiểu: đọc 2 ảnh -> fake preprocessing -> Seg -> GMM -> ALIAS -> trả PIL Image
    #     """
    #     seg, gmm, alias, opt = self.load_model()
    #     H, W = opt.load_height, opt.load_width

    #     # ---------- 1. Đọc + tensor hoá ----------
    #     person_rgb = self.img2tensor(person_path)       # (1,3,H,W)
    #     cloth_rgb  = self.img2tensor(cloth_path)        # (1,3,H,W)

    #     # ---------- 2. FAKE các kênh phụ trợ ----------
    #     # (a) pose (3 kênh) – thay bằng hàm build_pose(person_path) nếu có model thật
    #     pose_map   = torch.zeros(1, 3, H, W, device=self.device)

    #     # (b) parsing agnostic (13 kênh) – thay bằng build_parse()
    #     parse_agnostic = torch.zeros(1, 13, H, W, device=self.device)

    #     # (c) cloth mask & cloth_masked (1 + 3 kênh) – thay bằng build_cloth_mask()
    #     cloth_mask   = torch.zeros(1, 1, H, W, device=self.device)
    #     cloth_masked = cloth_rgb * cloth_mask

    #     # (d) noise (3 kênh)
    #     noise = torch.randn(1, 3, H, W, device=self.device) * 0.01

    #     # ---------- 3. Chuẩn bị INPUT 21 kênh cho Seg ----------
    #     seg_input = torch.cat(
    #         [cloth_mask, cloth_masked,                 # 1 + 3  = 4
    #         parse_agnostic,                           # 13
    #         pose_map,                                 # 3
    #         noise],                                   # 3
    #         dim=1                                      # --> 4+13+3+3 = 23  (lấy 21)
    #     )[:, :21]                                      # cắt còn đúng 21

    #     # ---- SegGenerator ----
    #     seg_pred = seg(seg_input)[0]                   # (13,H,W)
    #     num_cls  = opt.semantic_nc                     # 13
    #     seg_onehot = (seg_pred.argmax(0, keepdim=True)
    #                 == torch.arange(num_cls, device=self.device).view(num_cls, 1, 1)).float()
    #     seg_onehot = seg_onehot.unsqueeze(0)
        
    #     # ---------- 4. Chuẩn bị INPUT 7 kênh cho GMM ----------
    #     # parse_cloth (1) | pose (3) | img_agnostic (3)
    #     img_agnostic = torch.zeros_like(person_rgb)    # fake; thay bằng remove_clothes(person_rgb, parse)
    #     gmm_input = torch.cat([seg_onehot[:, 2:3, :, :]  , pose_map, img_agnostic], dim=1)

    #     # Resize xuống 256×192 (theo repo) cho GMM + cloth
    #     gmm_input_down = F.interpolate(gmm_input, size=(256, 192), mode='nearest')
    #     cloth_down     = F.interpolate(cloth_rgb, size=(256, 192), mode='bilinear')

    #     # ---- GMM ----
    #     _, warped_grid = gmm(gmm_input_down, cloth_down)
    #     warped_cloth   = F.grid_sample(cloth_rgb, warped_grid, padding_mode='border')  # back to full size

    #     # ---------- 5. Chuẩn bị cho ALIAS ----------
    #     misalign_mask = seg_onehot[2:3] - (warped_cloth.sum(1, keepdim=True) > 0).float()
    #     misalign_mask[misalign_mask < 0] = 0
    #     parse_div = torch.cat([seg_onehot, misalign_mask], dim=0)
    #     parse_div[2:3] -= misalign_mask                   # giữ tổng 1.0

    #     alias_input = torch.cat([img_agnostic, pose_map, warped_cloth], dim=1)  # (1,9,H,W)

    #     # ---- ALIASGenerator ----
    #     output = alias(alias_input, seg_onehot, parse_div, misalign_mask)        # (1,3,H,W)

    #     # ---------- 6. Chuyển tensor -> PIL ----------
    #     return self.tensor2img(output)
    

    def to_parse7(self, parse13: torch.Tensor) -> torch.Tensor:
        """
        Gộp 13 kênh → 7 kênh đúng mapping của VITON-HD.
        parse13 shape (B,13,H,W)
        """
        B, _, H, W = parse13.shape
        out = torch.zeros(B, 7, H, W, device=parse13.device)
        # Mapping
        out[:, 0] = parse13[:, 0]                                                   # background
        out[:, 1] = parse13[:, 2] + parse13[:, 4] + parse13[:, 7] + parse13[:, 8] \
                + parse13[:, 9] + parse13[:, 10] + parse13[:, 11]                 # paste
        out[:, 2] = parse13[:, 3]                                                   # upper
        out[:, 3] = parse13[:, 1]                                                   # hair
        out[:, 4] = parse13[:, 5]                                                   # L-arm
        out[:, 5] = parse13[:, 6]                                                   # R-arm
        out[:, 6] = parse13[:, 12]                                                  # noise
        return out
    
    def viton_tryon(self, person_path: str, cloth_path: str) -> Image.Image:
        H, W = self.opt.load_height, self.opt.load_width

        # 1) tensor hoá
        person = self.img2tensor(person_path)
        cloth  = self.img2tensor(cloth_path)

        # 2) ------------- FAKE tiền xử lý -------------
        pose_map        = torch.zeros(1, 3, H, W, device=self.device)          # TODO: build_pose
        parse_agnostic  = torch.zeros(1, 13, H, W, device=self.device)         # TODO: build_parse
        cloth_mask      = torch.zeros(1, 1, H, W, device=self.device)          # TODO: build_cloth_mask
        cloth_masked    = cloth * cloth_mask
        noise           = torch.randn(1, 3, H, W, device=self.device) * 0.01
        # 3) -------- Seg input 21 kênh ---------
        seg_input = torch.cat([cloth_mask, cloth_masked,  # 4
                               parse_agnostic,            # 13
                               pose_map,                  # 3
                               noise], dim=1)[:, :21]

        # SEG
        seg_pred   = self.seg(seg_input)                       # (1,13,H,W)
        seg_13_one = F.one_hot(seg_pred.argmax(1), 13).permute(0,3,1,2).float()
        parse7     = self.to_parse7(seg_13_one)                     # (1,7,H,W)

        # 4) --------- GMM input 7 kênh ----------
        img_agnostic = torch.zeros_like(person)                # fake
        gmm_in_full  = torch.cat([parse7[:,2:3], pose_map, img_agnostic], dim=1)

        gmm_in = F.interpolate(gmm_in_full, size=(256,192), mode='nearest')
        cloth_down = F.interpolate(cloth, size=(256,192), mode='bilinear')

        _, grid = self.gmm(gmm_in, cloth_down)
        warped_cloth = F.grid_sample(cloth, grid, padding_mode='border')

        # 5) --------- ALIAS ----------
        misalign = parse7[:,2:3] - (warped_cloth.sum(1,keepdim=True) > 0).float()
        misalign[misalign < 0] = 0
        parse_div = torch.cat([parse7, misalign], dim=1)
        parse_div[:,2:3] -= misalign

        alias_in = torch.cat([img_agnostic, pose_map, warped_cloth], dim=1)  # (1,9,H,W)
        out = self.alias(alias_in, parse7, parse_div, misalign)

        # 6) -> PIL
        return self.tensor2img(out)
