import numpy as np

def analyze(category_arr):  
  arr_height, arr_width = category_arr.shape[:2]

  response = {}
  response['standard'] = []
  response['ratio'] = []
  response['score'] = []

  hcount = 0
  acount = 0
  field = 0.0

  color_classes = ["도로", "주택", "아파트", "공장", "강", "논밭", "녹지", "대형건물", "미분류"]

  colors, counts = np.unique(category_arr, return_counts=1)
  for idx, x in enumerate(colors):
    counts[idx] = 0

  # 10% ~ 90% 사이의 값은 중앙 그 외는 외곽으로 판정
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

  env_plus_ret = 0.0
  env_minus_ret = 0.0
  conv_ret = 0.0

  syn = 0

  for index, color in enumerate(colors):
    count = counts[index]
    
    proportion = (100 * count) / (sum(counts)) #외곽 픽셀 0.7 반영
    ci = int(color)

    response['ratio'].append({"class" : color_classes[ci] , "proportion" : proportion})
    
    if(color == 6): #녹지
      env_plus_ret += proportion
      syn += 1
    elif(color == 3): #공장
      env_minus_ret -= proportion * 1.25 / 2
    elif(color == 7): #대형건물
      if(proportion <= 20):
        conv_ret += proportion
      else:
        conv_ret += 20
    elif(color == 0): #도로
      env_minus_ret -= proportion * 1.25 / 10
    elif(color == 4): #강
      env_plus_ret += proportion
      syn += 1
    elif(color == 1): #주택
      hcount = count
    elif(color == 2): #아파트
      acount = count
    elif(color == 5): #논밭
      field = proportion

  if(syn == 2): #강 + 녹지 시너지
    env_plus_ret += 5

  if acount + hcount != 0:
    score_house = (100 * acount) / (acount+hcount)
  else:
    score_house = 0
  
  response['standard'].append({"name" : "편의성 점수", "desc" : "대형건물 수", "score" : conv_ret})
  response['standard'].append({"name" : "공장, 도로 점수", "desc" : "매연, 소음 등 마이너스 요소", "score" : env_minus_ret})
  response['standard'].append({"name" : "녹지, 강 점수", "desc" : "환경 요소", "score" : env_plus_ret})
  response['standard'].append({"name" : "주택/아파트 점수", "desc" : "개인 선호도", "score" : score_house})
  response['standard'].append({"name" : "논밭 점수", "desc" : "개인 지표", "score" : field})
  
  response['score'] = env_plus_ret+env_minus_ret+conv_ret

  return response
