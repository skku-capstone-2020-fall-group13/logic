# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qZjfnvKJ1MNDIOSBajI2BkI0cLV-DEDo
"""

import numpy as np
from PIL import Image


'''
테스트를 위해서 드라이브에서 이미지를 받아옴
실제 어플리케이션에선 segmentation된 이미지를 받아올것
'''

def logic(image):
  

  
  cat_im = image
  
  h,w = cat_im.shape[:2]
  obj = []
  Color_class = ["도로", "주택", "아파트", "공장", "강", "주택", "녹지", "대형건물", "미분류"]




  colours, counts = np.unique(cat_im, return_counts=1)
  for ind, x in enumerate(colours):
    counts[ind] = 0


#100~900사이의 값은 중앙 그 외는 외곽으로 판정
  for height in range(h):
    for width in range(w):
      if height >= 100 and height <= 900 and width >= 100 and width <= 900:
        i = np.where((colours == cat_im[height][width]))
        counts[i[0][0]] += 1
      else:
        i = np.where((colours == cat_im[height][width]))
        counts[i[0][0]] += 0.7


  env_ret = 0.0
  conv_ret = 0.0

  syn = 0


  for index, colour in enumerate(colours):
    count = counts[index]
    
    proportion = (100 * count) / (sum(counts)) #외곽 픽셀 0.7 반영
    ci = int(colour)

    obj.append({"Object" : Color_class[ci] , "Proportion" : proportion})
    
    
    if(colour == 6): #녹지
      env_ret += proportion
      syn += 1
    elif(colour == 3): #공장
      env_ret -= proportion * 1.25 / 2
    elif(colour == 7): #대형건물
      if(proportion <= 20):
        conv_ret += proportion
      else:
        conv_ret += 20
    elif(colour == 0): #도로
      env_ret -= proportion * 1.25 / 10
    elif(colour == 4): #강
      env_ret += proportion
      syn += 1

  if(syn == 2): #강 + 녹지 시너지
    env_ret += 5
  
  obj.append({"쾌적도" : env_ret+conv_ret})
  return obj