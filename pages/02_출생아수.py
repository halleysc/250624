import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="wide")

# Streamlit 앱의 제목 설정
st.title("2025년 5월 연령별 인구 현황 분석")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file is not None:
    try:
        # EUC-KR 인코딩으로 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='EUC-KR')

        st.subheader("원본 데이터")
        st.dataframe(df)

        # 컬럼명 전처리
        # '2025년05월_계_'로 시작하는 컬럼만 선택하여 연령으로 변환
        age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]
        
        # 새로운 컬럼 리스트 생성: '행정구역', '총인구수', 그리고 전처리된 연령 컬럼
        processed_columns = ['행정구역', '총인구수']
        clean_age_columns_map = {}

        for col in age_columns:
            # 숫자 부분만 추출 (예: '2025년05월_계_10세' -> '10')
            match = re.search(r'(\d+)세', col)
            if match:
                age = match.group(1)
                new_col_name = f"{age}세" # '10세', '20세' 등으로 유지
                clean_age_columns_map[col] = new_col_name
                processed_columns.append(new_col_name) # 전처리된 컬럼 이름 추가
            else:
                # '2025년05월_계_0_9세'와 같은 범위 처리
                match_range = re.search(r'(\d+)_(\d+)세', col)
                if match_range:
                    age_range = f"{match_range.group(1)}~{match_range.group(2)}세"
                    new_col_name = age_range
                    clean_age_columns_map[col] = new_col_name
                    processed_columns.append(new_col_name)
                else:
                    # '2025년05월_계_100세이상' 처리
                    if '100세이상' in col:
                        new_col_name = '100세이상'
                        clean_age_columns_map[col] = new_col_name
                        processed_columns.append(new_col_name)
                    else:
                        # 예상치 못한 패턴은 일단 제외
                        pass

        # 필요한 컬럼만 선택하고 컬럼명 변경
        # '2025년05월_남_0세' 컬럼도 포함시켜야 하므로 컬럼 리스트에 추가
        required_cols = ['행정구역', '총인구수', '2025년05월_남_0세'] + age_columns
        df_processed = df[required_cols].copy()
        df_processed = df_processed.rename(columns=clean_age_columns_map)

        # '2025년05월_남_0세' 기준으로 상위 5개 행정구역 추출
        # '2025년05월_남_0세' 컬럼이 데이터에 없는 경우를 대비한 예외 처리
        if '2025년05월_남_0세' in df_processed.columns:
            df_top5 = df_processed.nlargest(5, '2025년05월_남_0세')
        else:
            st.warning("'2025년05월_남_0세' 컬럼이 데이터에 없습니다. '총인구수' 기준으로 상위 5개 지역을 표시합니다.")
            df_top5 = df_processed.nlargest(5, '총인구수')


        st.subheader("2025년 5월 남성 0세 인구 상위 5개 행정구역")
        # '2025년05월_남_0세' 컬럼을 함께 보여주기
        if '2025년05월_남_0세' in df_top5.columns:
            st.dataframe(df_top5[['행정구역', '2025년05월_남_0세']])
        else:
            st.dataframe(df_top5[['행정구역', '총인구수']]) # 대체 컬럼 표시


        st.subheader("연령별 인구 분포 (남성 0세 인구 상위 5개 행정구역)")

        # 시각화를 위한 데이터 준비
        # 연령 컬럼만 선택
        age_population_data = df_top5.set_index('행정구역').drop(columns=['총인구수', '2025년05월_남_0세'], errors='ignore')

        # 연령 컬럼의 순서를 정렬하기 위한 로직
        sorted_age_columns = []
        age_ranges_and_over = []

        for col in age_population_data.columns:
            if re.match(r'^\d+세$', col): # '10세', '20세' 등
                sorted_age_columns.append(int(re.search(r'(\d+)', col).group(1)))
            else: # '0~9세', '100세이상' 등
                age_ranges_and_over.append(col)
        
        sorted_age_columns.sort()
        sorted_age_columns_str = [f"{age}세" for age in sorted_age_columns]

        final_sorted_columns = []
        if '0~9세' in age_ranges_and_over:
            final_sorted_columns.append('0~9세')
            age_ranges_and_over.remove('0~9세')
        
        final_sorted_columns.extend(sorted_age_columns_str)

        if '100세이상' in age_ranges_and_over:
            final_sorted_columns.append('100세이상')
            age_ranges_and_over.remove('100세이상')
        
        final_sorted_columns.extend(sorted(age_ranges_and_over)) # 나머지 처리되지 않은 컬럼 추가

        # 실제 데이터프레임의 컬럼 순서 재정렬
        age_population_data_sorted = age_population_data[final_sorted_columns]

        # 데이터프레임을 Streamlit 기본 line_chart에 맞게 변환
        for index, row in age_population_data_sorted.iterrows():
            # 행정구역명 전처리: "서울특별시 ㅇㅇ구 ㅇㅇ동"에서 "ㅇㅇ동"만 추출
            original_location_name = index
            dong_name_match = re.search(r'\s([가-힣]+동)$', original_location_name)
            if dong_name_match:
                display_location_name = dong_name_match.group(1)
            else:
                display_location_name = original_location_name # 동 이름이 없으면 원본 유지

            st.subheader(f"{display_location_name}의 연령별 인구")
            # Series를 데이터프레임으로 변환하여 st.line_chart에 전달
            chart_data = pd.DataFrame({'연령': row.index, '인구수': row.values})
            st.line_chart(chart_data, x='연령', y='인구수')


    except UnicodeDecodeError:
        st.error("파일 인코딩 오류! EUC-KR로 인코딩된 파일이 맞는지 확인해주세요.")
    except KeyError as ke:
        st.error(f"필수 컬럼이 데이터에 없습니다: {ke}. CSV 파일에 '2025년05월_남_0세' 컬럼이 있는지 확인해주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("CSV 파일을 업로드하여 분석을 시작하세요.")
