import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.system('clear')

from AI.VITON_HD.models import VITONHDNet
import torch
import cv2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)

viton = VITONHDNet(device)

result = viton.viton_tryon('test/person.png', 'test/cloth.png')

cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()