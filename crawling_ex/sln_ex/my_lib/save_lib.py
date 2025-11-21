from datetime import datetime
import os
import csv

# 데이터 저장 함수 정의부
def save_datas(data_keyword, head, movie_lists):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H")   # → 2025111713 형태
    # 폴더 / 파일명 설정
    folder = f"{data_keyword}_datas"
    filename = f"{data_keyword}_{timestamp}.csv"
    # "movie_datas/movie_2025112112.csv"
    filepath = os.path.join(folder, filename)
    # 폴더 자동 생성
    os.makedirs(folder, exist_ok=True)
    # CSV 저장 (2차원 리스트 여야함.)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 영화제목 | 개봉일 | 예매매출액 | 예매관람수
        # 1차원 리스트 저장
        writer.writerow(head)
        # 2차원 list로 만들어서 저장(수집한 데이터)
        writer.writerows(movie_lists)
    print("CSV 저장 완료:", filepath)