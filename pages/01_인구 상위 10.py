import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="연령별 인구 분석", layout="wide")

st.title("2025년 5월 연령별 인구 분석 (총인구수 기준 상위 10개 지역)")
st.write("총인구수 상위 10개 지역(동 단위 기준)의 연령별 인구를 선 그래프로 시각화합니다.")

# 기본 파일 경로
default_file_path = "/mnt/data/202505_202505_연령별인구현황_월간.csv"

# 파일 업로드
uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (선택 사항)", type="csv")

# 파일 선택
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

# 주요 컬럼 설정
admin_col = "행정구역"
total_col = "2025년05월_계_총인구수"
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and ("세" in col or "100세 이상" in col)]

# 쉼표 제거 후 정수형 변환
for col in [total_col] + age_cols:
    df[col] = df[col].astype(str).str.replace(",", "").astype(int)

# ⛏️ 행정구역 이름에서 '서울특별시 ㅇㅇ구' 제거 → 동 이름만
df[admin_col] = df[admin_col].apply(lambda x: re.sub(r'^서울특별시\s+\S+\s+', '', x).strip())

# 상위 10개 지역 추출
top10_df = df.sort_values(by=total_col, ascending=False).head(10)

# 연령 컬럼명 정제
age_labels = [col.replace("2025년05월_계_", "") for col in age_cols]

# 시각화용 데이터 준비
plot_df = top10_df[[admin_col] + age_cols].copy()
plot_df.columns = [admin_col] + age_labels
plot_df = plot_df.set_index(admin_col).T
plot_df.index.name = "연령"

# 📈 선 그래프 출력
st.subheader("📊 연령별 인구 선 그래프 (총인구수 기준 상위 10개 동)")
st.line_chart(plot_df)

# 📄 원본 데이터 일부 표시
st.subheader("🧾 원본 데이터 미리보기")
preview_cols = [admin_col, total_col] + age_cols[:5]  # 앞쪽 일부 열만 보기
st.dataframe(df[preview_cols])
