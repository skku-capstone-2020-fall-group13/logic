import numpy as np

def analyze(category_arr):  
  arr_height, arr_width = category_arr.shape[:2]

  response = {}
  response['standard'] = []
  response['ratio'] = []
  response['score'] = []

  color_classes = ["도로", "주택", "아파트", "공장", "강", "논밭", "녹지", "대형건물", "미분류"]

  colors, counts = np.unique(category_arr, return_counts=1)
  for idx, x in enumerate(colors):
    counts[idx] = 0

  # 10% ~ 90% 사이의 값은 중앙, 그 외는 외곽으로 판정
  hmin = arr_height * 0.1
  hmax = arr_height * 0.9
  wmin = arr_width * 0.1
  wmax = arr_width * 0.9

  for h in range(arr_height):
    for w in range(arr_width):
      if h >= hmin and h <= hmax and w >= wmin and w <= wmax:
        i = np.where((colors == category_arr[h][w]))
        counts[i[0][0]] += 1
      else:
        i = np.where((colors == category_arr[h][w]))
        counts[i[0][0]] += 0.7

  green_score = 0.0
  green_synergy = 0

  factory_road_score = 0.0
  convenience_score = 0.0

  house_score = 0.0
  house_count = 0
  apartment_count = 0

  development_score = 100

  for index, color in enumerate(colors):
    count = counts[index]
    
    proportion = (100 * count) / (sum(counts)) # 외곽 픽셀 0.7 반영
    ci = int(color)

    response['classes'].append({"name" : color_classes[ci] , "proportion" : proportion})
    
    if(color == 6): # 녹지
      green_score += proportion
      development_score -= proportion
      green_synergy += 1
    elif(color == 3): # 공장
      factory_road_score -= proportion * 1.25 / 2
    elif(color == 7): # 대형건물
      if(proportion <= 20):
        convenience_score += proportion
      else:
        convenience_score += 20
    elif(color == 0): # 도로
      factory_road_score -= proportion * 1.25 / 10
    elif(color == 4): # 강
      green_score += proportion
      development_score -= proportion
      green_synergy += 1
    elif(color == 1): # 주택
      house_count = count
    elif(color == 2): # 아파트
      appartment_count = count
    elif(color == 5): # 논밭
      development_score -= proportion

  if(green_synergy == 2): #강 + 녹지 시너지
    green_score += 5

  if apartment_count + house_count != 0:
    house_score = (100 * apartment_count) / (apartment_count + house_count)
  else:
    house_score = 0
  
  response['criterion'].append({"name" : "편의성 점수", "desc" : "주변의 대형 건물(관공서 등)의 비율", "score" : convenience_score})
  response['criterion'].append({"name" : "공장, 도로 점수", "desc" : "매연과 소음을 발생시키는 공장과 도로의 비율", "score" : factory_road_score})
  response['criterion'].append({"name" : "녹지, 강 점수", "desc" : "공기의 질과 정서적 안정에 도움을 주는 녹지와 수변공간의 비율", "score" : green_score})
  response['criterion'].append({"name" : "주택/아파트 지수", "desc" : "구역에 주택과 아파트 중 어느 쪽이 많은지의 비율", "score" : house_score})
  response['criterion'].append({"name" : "개발 지수", "desc" : "시내와 교외를 판단할 수 있는 개발도 점수", "score" : development_score})
  
  response['score'] = green_score + factory_road_score + convenience_score

  return response
