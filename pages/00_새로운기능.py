import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

    # '2025년05월_계_'로 시작하는 연령별 컬럼 추출
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    total_col = "2025년05월_계_총인구수"

    # 연령 숫자만 추출하여 컬럼명 재설정
    new_age_cols = [col.replace("2025년05월_계_", "") for col in age_cols]

    # ',' 제거 후 숫자로 변환
    df[total_col] = df[total_col].str.replace(",", "").astype(int)
    for col in age_cols:
        df[col] = df[col].str.replace(",", "").astype(int)

    # 총인구수 기준 상위 5개 행정구역 선택
    top5_df = df.nlargest(5, total_col).copy()

    # 시각화를 위한 데이터 가공
    top5_df = top5_df[["행정구역", total_col] + age_cols]
    top5_df.columns = ["행정구역", "총인구수"] + new_age_cols

    # 연령을 index로, 행정구역을 열로 전환
    chart_df = top5_df.set_index("행정구역").drop(columns="총인구수").T
    chart_df.index.name = "연령"
    chart_df.reset_index(inplace=True)

    # 데이터 시각화
    st.subheader("📊 총인구수 상위 5개 행정구역의 연령별 인구 추이")
    st.line_chart(chart_df.set_index("연령"))

    # 원본 데이터 표시
    st.subheader("🗂 원본 데이터 (상위 5개 행정구역)")
    st.dataframe(top5_df)

else:
    st.info("왼쪽 사이드바 또는 위에서 CSV 파일을 업로드해주세요.")
