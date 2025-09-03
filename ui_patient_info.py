import streamlit as st
import os
import datetime
from utils import sync_widget_key, sync_multiple_keys, create_navigation_buttons

def render_step_0_welcome():
    st.header("✨ 당신의 턱관절 건강, 지금 바로 확인하세요!")
    st.write("""
    이 시스템은 턱관절 건강 상태를 스스로 점검하고, 잠재적인 문제를 조기에 파악할 수 있도록 설계되었습니다.
    간단한 몇 단계의 설문을 통해, 맞춤형 예비 진단 결과를 받아보세요.
    """)
    st.markdown("---")

    col_intro1, col_intro2, col_intro3 = st.columns(3)
    with col_intro1:
        st.info("**🚀 신속한 검사:** 짧은 시간 안에 주요 증상 확인")
    with col_intro2:
        st.info("**📊 직관적인 결과:** 시각적으로 이해하기 쉬운 진단 요약")
    with col_intro3:
        st.info("**📝 보고서 생성:** 개인 맞춤형 PDF 보고서 제공")

    st.markdown("---")

    if 'show_exercise' not in st.session_state:
        st.session_state.show_exercise = False

    if not st.session_state.show_exercise:
        if st.button("턱관절 운동 안내 보기"):
            st.session_state.show_exercise = True
    else:
        if os.path.exists("tmj_exercise.png"):
            st.image("tmj_exercise.png", use_container_width=True)
        else:
            st.warning("운동 안내 이미지를 찾을 수 없습니다.")
        if st.button("운동 안내 닫기"):
            st.session_state.show_exercise = False

    st.markdown("---")
    if st.button("문진 시작하기 🚀"):
        st.session_state.step = 1
        st.rerun()

def render_step_1_patient_info():
    st.header("📝 환자 기본 정보 입력")
    st.markdown("---")

    field_mapping = {
        "name_widget": "name",
        "birthdate_widget": "birthdate",
        "gender_widget": "gender",
        "email_widget": "email",
        "phone_widget": "phone",
        "address_widget": "address",
        "occupation_widget": "occupation",
        "visit_reason_widget": "visit_reason",
    }

    with st.container(border=True):
        st.text_input("이름*", key="name_widget", value=st.session_state.get("name", ""), on_change=sync_widget_key, args=("name_widget", "name"))
        st.date_input("생년월일*", key="birthdate_widget", value=st.session_state.get("birthdate", datetime.date(2000, 1, 1)), on_change=sync_widget_key, args=("birthdate_widget", "birthdate"))
        st.radio("성별*", ["남성", "여성", "기타", "선택 안 함"], key="gender_widget", index=3, horizontal=True, on_change=sync_widget_key, args=("gender_widget", "gender"))
        st.text_input("이메일*", key="email_widget", value=st.session_state.get("email", ""), on_change=sync_widget_key, args=("email_widget", "email"))
        st.text_input("연락처*", key="phone_widget", value=st.session_state.get("phone", ""), on_change=sync_widget_key, args=("phone_widget", "phone"))
        st.text_input("주소", key="address_widget", value=st.session_state.get("address", ""), on_change=sync_widget_key, args=("address_widget", "address"))
        st.text_input("직업", key="occupation_widget", value=st.session_state.get("occupation", ""), on_change=sync_widget_key, args=("occupation_widget", "occupation"))
        st.text_area("내원 목적", key="visit_reason_widget", value=st.session_state.get("visit_reason", ""), on_change=sync_widget_key, args=("visit_reason_widget", "visit_reason"))

    def validate_patient_info():
        ok = all([
            st.session_state.get("name"),
            st.session_state.get("gender") != "선택 안 함",
            st.session_state.get("email"),
            st.session_state.get("phone")
        ])
        if ok:
            sync_multiple_keys(field_mapping)
        else:
            st.warning("필수 항목을 모두 입력해주세요.")
        return ok

    create_navigation_buttons(prev_step=0, next_step=2, validation_func=validate_patient_info)

def render_step_2_chief_complaint():
    st.title("주 호소 (Chief Complaint)")
    st.markdown("---")

    field_mapping = {
        "chief_complaint_widget": "chief_complaint",
        "chief_complaint_other_widget": "chief_complaint_other",
        "onset_widget": "onset"
    }

    with st.container(border=True):
        st.radio("방문 이유*", ["턱 통증", "턱관절 소리", "두통", "기타", "선택 안 함"], key="chief_complaint_widget", index=4, on_change=sync_widget_key, args=("chief_complaint_widget", "chief_complaint"))
        if st.session_state.get("chief_complaint") == "기타":
            st.text_input("기타 사유", key="chief_complaint_other_widget", value=st.session_state.get("chief_complaint_other", ""), on_change=sync_widget_key, args=("chief_complaint_other_widget", "chief_complaint_other"))
        st.radio("문제 발생 시기*", ["일주일 이내", "1개월 이내", "6개월 이내", "1년 이상", "선택 안 함"], key="onset_widget", index=4, on_change=sync_widget_key, args=("onset_widget", "onset"))

    def validate_cc_step():
        sync_multiple_keys(field_mapping)
        if st.session_state.get("chief_complaint") == "선택 안 함" or st.session_state.get("onset") == "선택 안 함":
            st.warning("주 호소 및 발생 시기를 선택해주세요.")
            return False
        if st.session_state.get("chief_complaint") == "기타" and not st.session_state.get("chief_complaint_other"):
            st.warning("기타 사유를 입력해주세요.")
            return False
        return True

    next_step = {
        "턱 통증": 3,
        "두통": 3,
        "턱관절 소리": 5,
        "기타": 6
    }.get(st.session_state.get("chief_complaint"), 3)

    create_navigation_buttons(prev_step=1, next_step=next_step, validation_func=validate_cc_step)
