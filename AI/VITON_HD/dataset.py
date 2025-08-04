import json
from os import path 
import numpy as np
from PIL import Image, ImageDraw
import torch
from torch.utils import data
from torchvision import transforms

class VITONDataset(data.Dataset):
    def __init__(self, opt):
        super(VITONDataset, self).__init__()
        self.opt = opt
        self.root = opt.dataroot
        self.list_path = opt.test_list
        self.data_list = self.load_data()

    def load_data(self):