import streamlit as st

def get_job_recommendations(mbti_type):
    """
    MBTI 유형에 따른 직업 추천을 반환하는 함수
    """
    recommendations = {
        "ISTJ": ["회계사", "공무원", "데이터 분석가", "경찰관", "프로그래머"],
        "ISFJ": ["간호사", "사회복지사", "교사", "사서", "인사 담당자"],
        "ISTP": ["엔지니어", "정비사", "소방관", "파일럿", "프로게이머"],
        "ISFP": ["디자이너", "예술가", "음악가", "요리사", "수의사"],
        "INTJ": ["과학자", "교수", "컨설턴트", "건축가", "전략 기획자"],
        "INFJ": ["상담사", "작가", "성직자", "심리학자", "인사 컨설턴트"],
        "INTP": ["연구원", "프로그래머", "철학자", "발명가", "대학교수"],
        "INFP": ["작가", "예술가", "상담사", "심리학자", "교사"],
        "ESTJ": ["경영자", "관리자", "영업 관리", "군인", "변호사"],
        "ESFJ": ["영업원", "교사", "사회복지사", "행사 기획자", "간호사"],
        "ESTP": ["사업가", "경찰관", "영업원", "스포츠 선수", "트레이너"],
        "ESFP": ["연예인", "이벤트 플래너", "유치원 교사", "서비스업 종사자", "강사"],
        "ENTJ": ["기업가", "경영 컨설턴트", "변호사", "정치인", "프로젝트 매니저"],
        "ENFJ": ["리더", "교사", "상담사", "인사 관리자", "강사"],
        "ENTP": ["창업가", "컨설턴트", "변호사", "마케터", "발명가"],
        "ENFP": ["크리에이터", "마케터", "강사", "상담사", "여행 작가"],
    }
    return recommendations.get(mbti_type, ["해당 MBTI 유형에 대한 추천 직업이 없습니다."])

# --- Streamlit 앱 구성 ---
st.set_page_config(page_title="MBTI 기반 직업 추천", layout="centered")

st.title("💡 MBTI 유형 기반 직업 추천기")
st.markdown("""
<style>
.stSelectbox {
    margin-bottom: 20px;
}
.stButton {
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.write("당신의 MBTI 유형을 선택하면 그에 맞는 직업들을 추천해 드릴게요!")

# MBTI 유형 선택 드롭다운
mbti_options = [
    "선택하세요", "ISTJ", "ISFJ", "ISTP", "ISFP", "INTJ", "INFJ", 
    "INTP", "INFP", "ESTJ", "ESFJ", "ESTP", "ESFP", "ENTJ", 
    "ENFJ", "ENTP", "ENFP"
]
selected_mbti = st.selectbox("당신의 MBTI 유형은 무엇인가요?", mbti_options)

if st.button("직업 추천받기"):
    if selected_mbti == "선택하세요":
        st.warning("⚠️ MBTI 유형을 선택해주세요.")
    else:
        st.subheader(f"✨ {selected_mbti} 유형에게 추천하는 직업:")
        recommended_jobs = get_job_recommendations(selected_mbti)
        
        # 추천 직업을 깔끔하게 리스트로 표시
        st.markdown("---")
        for job in recommended_jobs:
            st.markdown(f"- **{job}**")
        st.markdown("---")
        
        st.info("이 추천은 일반적인 경향을 기반으로 하며, 개인의 흥미와 능력에 따라 달라질 수 있습니다.")

st.markdown("""
---
<div style="text-align: center;">
    <p>본 추천기는 MBTI 특성에 따른 일반적인 직업 선호도를 참고하여 제작되었습니다.</p>
    <p>자세한 직업 탐색은 전문가와 상담하거나 다양한 정보를 찾아보시는 것을 추천합니다.</p>
</div>
""", unsafe_allow_html=True)
