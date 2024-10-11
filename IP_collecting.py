import socket
import os
from datetime import datetime
import pandas as pd

# IP 주소 가져오는 함수
def get_current_ip():
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        '컴퓨터 명': hostname,
        'IP 주소': ipv4_address,
        '수집 시간': execution_time
    }

# CSV 파일에 IP 주소와 실행 시간 업데이트
def update_drive_info_csv(new_data, output_file):
    # new_data를 DataFrame으로 변환 (리스트로 감싸지 않음)
    new_df = pd.DataFrame(new_data, index=[0])

    # 파일이 있는지 확인
    if os.path.exists(output_file):
        try:
            # 기존 파일 읽기
            existing_df = pd.read_csv(output_file, encoding='utf-8-sig')

            # '컴퓨터 명' 컬럼이 있는지 확인
            if '컴퓨터 명' not in existing_df.columns:
                raise KeyError("'컴퓨터 명' 컬럼이 존재하지 않습니다.")
            
            # 동일한 컴퓨터 명의 기존 데이터 제거
            existing_df = existing_df[existing_df['컴퓨터 명'] != new_df['컴퓨터 명'].iloc[0]]
            
            # 새로운 데이터와 결합
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        except (KeyError, pd.errors.EmptyDataError):
            # 파일이 잘못된 경우 새로운 데이터를 생성
            print("CSV 파일이 손상되었거나 '컴퓨터 명' 컬럼이 없습니다. 새로 작성합니다.")
            updated_df = new_df
    else:
        # 파일이 없으면 새로운 데이터를 그대로 사용
        updated_df = new_df

    # CSV 파일에 저장 (헤더 포함, UTF-8 with BOM 인코딩)
    updated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f'IP information updated in {output_file}')


if __name__ == "__main__":
    output_file = "C:/Users/hyeongryeol.jeon/Desktop/2DDSD/drive_info.csv"

    # 새로운 IP 정보 가져오기
    new_data = get_current_ip()

    # CSV 파일 업데이트
    update_drive_info_csv(new_data, output_file)
