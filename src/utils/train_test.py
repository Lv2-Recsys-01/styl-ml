import pandas as pd
from pathlib import Path


def process_data(implicit_df, output_file):
    # 중복 제거
    implicit_df = implicit_df.drop_duplicates(
        subset=["session_id", "outfit_id"], keep="last"
    )

    # rating 추가
    implicit_df["rating"] = 1

    # 파일로 저장
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    implicit_df.to_csv(output_file, index=False)


def make_implicit(data_dates, click_path, like_path, share_path, output_path):
    # 좋아요 데이터 불러오기
    like = pd.read_csv(like_path)
    like = like[like["is_deleted"] == False]

    # 클릭과 공유 데이터를 저장할 빈 리스트 생성
    click_data = []
    share_data = []

    # 클릭과 공유 데이터를 묶어서 리스트에 추가
    for date in data_dates:
        click_file = click_path.format(date)
        share_file = share_path.format(date)

        # 파일 존재 여부 확인 후 데이터 불러오기
        if Path(click_file).is_file() and Path(share_file).is_file():
            click = pd.read_csv(click_file)
            share = pd.read_csv(share_file)
            click_data.append(click)
            share_data.append(share)
        elif Path(click_file).is_file():
            click = pd.read_csv(click_file)
            click_data.append(click)
        elif Path(share_file).is_file():
            share = pd.read_csv(share_file)
            share_data.append(share)
        else:
            pass

    # 클릭과 공유 데이터 병합
    click = pd.concat(click_data, axis=0, ignore_index=True)
    share = pd.concat(share_data, axis=0, ignore_index=True)

    # 클릭, 좋아요, 공유 데이터를 하나로 합치기
    implicit_df = pd.concat([click, like, share])
    implicit_df = implicit_df[["session_id", "outfit_id"]]

    process_data(implicit_df, output_path)


if __name__ == "__main__":
    # 일자별로 데이터 추가, like csv파일은 DB에서 직접 저장해서 사용
    data_dates = ["2023-07-19", "2023-07-20", "2023-07-21"]
    click_path = "../../data/{}/click_image_log.txt"
    like_path = "../../data/like.csv"
    share_path = "../../data/{}/click_share_musinsa_log.txt"
    output_path = "../../data/train-test/implicit_data.csv"

    make_implicit(data_dates, click_path, like_path, share_path, output_path)
