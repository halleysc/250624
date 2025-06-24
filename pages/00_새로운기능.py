import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="연령별 인구현황 분석", layout="wide")

st.title("2025년 5월 연령별 인구현황 분석")
st.write("기본 파일 또는 업로드한 CSV 파일을 기반으로 총인구수 상위 5개 지역의 연령별 인구를 시각화합니다.")

# 기본 파일 경로
default_file_path = "202505_202505_연령별인구현황_월간.csv"

# 업로드 받기
uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (선택 사항)", type="csv")

# 파일 결정 로직
if uploaded_file is not None:
    st.success("✅ 업로드된 파일이 사용됩니다.")
    file_to_use = uploaded_file
elif os.path.exists(default_file_path):
    st.info("ℹ️ 업로드된 파일이 없으므로 기본 파일을 사용합니다.")
    file_to_use = default_file_path
else:
    st.error("❌ 사용할 수 있는 CSV 파일이 없습니다.")
    st.stop()

# 데이터 불러오기
df = pd.read_csv(file_to_use, encoding="euc-kr")

# ✅ 필요한 열 추출
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
