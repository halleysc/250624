import streamlit as st
import pandas as pd

st.set_page_config(page_title="연령별 인구현황 분석", layout="wide")

st.title("2025년 5월 연령별 인구현황 분석")
st.write("업로드한 CSV 파일을 기반으로 총인구수 상위 5개 지역의 연령별 인구를 시각화합니다.")

# 📁 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

    # ✅ 필요한 열만 선별
    population_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
    age_cols = [col for col in population_cols if "세" in col or "100세 이상" in col]
    total_col = "2025년05월_계_총인구수"
    admin_col = "행정구역"

    # ✅ 쉼표 제거 및 정수형 변환
    for col in [total_col] + age_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

    # ✅ 총인구수 기준 상위 5개 지역 선택
    top5_df = df.sort_values(by=total_col, ascending=False).head(5)

    # ✅ 시각화용 데이터 전처리
    age_labels = [col.replace("2025년05월_계_", "") for col in age_cols]
    line_df = top5_df[[admin_col] + age_cols].copy()
    line_df.columns = [admin_col] + age_labels

    line_df = line_df.set_index(admin_col).T  # 행: 연령, 열: 지역

    # 📊 선 그래프 출력
    st.subheader("📈 연령별 인구 선 그래프 (총인구수 상위 5개 지역)")
    st.line_chart(line_df)

    # 📄 원본 데이터 표시
    st.subheader("🧾 원본 데이터")
    st.dataframe(df)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
