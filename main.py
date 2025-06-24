import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
uploaded_file = st.file_uploader("CSV 파일 업로드 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # 열 이름 중 '2025년05월_계_'로 시작하는 열 추출 및 연령 숫자만 남김
    age_cols = [col for col in df.columns if col.startswith('2025년05월_계_')]
    new_age_cols = [col.replace('2025년05월_계_', '') for col in age_cols]
    age_df = df[['행정기관명', '총인구수'] + age_cols].copy()
    age_df.columns = ['행정기관명', '총인구수'] + new_age_cols

    # 총인구수 기준 상위 5개 행정기관 추출
    top5_df = age_df.sort_values('총인구수', ascending=False).head(5)

    # 시각화를 위한 데이터 변형
    plot_df = top5_df.set_index('행정기관명').drop(columns='총인구수').transpose()
    plot_df.index.name = '연령'
    plot_df.reset_index(inplace=True)

    st.subheader("📊 상위 5개 행정기관 연령별 인구 선 그래프")
    st.line_chart(plot_df.set_index('연령'))

    st.markdown("✅ **참고**: 위 그래프는 2025년 5월 기준 총인구수 상위 5개 행정기관의 연령별 인구 현황입니다.")

else:
    st.warning("먼저 CSV 파일을 업로드해주세요.")
