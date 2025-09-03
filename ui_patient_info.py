 # ui_patient_info.py

import os
import datetime
import streamlit as st
from utils import (
    sync_widget_key,
    sync_multiple_keys,
    create_navigation_buttons,
)

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
    with st.expander("시작하기 전에 꼭 읽어주세요!"):
        st.markdown("""
        * 본 시스템은 **의료 진단을 대체하지 않습니다.** 정확한 진단과 치료는 반드시 전문 의료기관을 방문하시기 바랍니다.
        * 제공된 모든 정보는 **익명으로 처리**되며, 개인 정보 보호를 최우선으로 합니다.
        * 솔직하게 답변해주시면 더욱 정확한 예비 진단 결과를 얻을 수 있습니다.
        """)

    if 'show_exercise' not in st.session_state:
        st.session_state.show_exercise = False

    if not st.session_state.show_exercise:
        if st.button("턱관절 운동 안내 보기", key="btn_show_exercise"):
            st.session_state.show_exercise = True
            st.rerun()
    else:
        exercise_img_path = "tmj_exercise.png"
        if os.path.exists(exercise_img_path):
            st.image(exercise_img_path, use_container_width=True)
        else:
            st.warning(f"운동 안내 이미지({exercise_img_path})를 찾을 수 없습니다.")

        if st.button("운동 안내 닫기", key="btn_hide_exercise"):
            st.session_state.show_exercise = False
            st.rerun()

    st.markdown("---")
    # 시작하기 -> 1단계로 이동
    create_navigation_buttons(prev_step=None, next_step=1)


def render_step_1_patient_info():
    st.header("📝 환자 기본 정보 입력")
    st.write("정확한 문진을 위해 필수 정보를 입력해주세요. (*표시는 필수 항목입니다.)")

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
        col_name, col_birthdate = st.columns(2)
        with col_name:
            st.text_input(
                "이름*",
                key="name_widget",
                value=st.session_state.get("name", ""),
                placeholder="이름을 입력하세요",
                on_change=sync_widget_key, args=("name_widget", "name")
            )
            if 'name' in st.session_state.get("validation_errors", {}):
                st.error(st.session_state.validation_errors['name'])

        with col_birthdate:
            st.date_input(
                "생년월일*",
                key="birthdate_widget",
                value=st.session_state.get("birthdate", datetime.date(2000, 1, 1)),
                min_value=datetime.date(1900, 1, 1),
                on_change=sync_widget_key, args=("birthdate_widget", "birthdate")
            )

        st.radio(
            "성별*",
            ["남성", "여성", "기타", "선택 안 함"],
            key="gender_widget",
            index=["남성", "여성", "기타", "선택 안 함"].index(st.session_state.get("gender", "선택 안 함")),
            horizontal=True,
            on_change=sync_widget_key, args=("gender_widget", "gender")
        )
        if 'gender' in st.session_state.get("validation_errors", {}):
            st.error(st.session_state.validation_errors['gender'])

        col_email, col_phone = st.columns(2)
        with col_email:
            st.text_input(
                "이메일*",
                key="email_widget",
                value=st.session_state.get("email", ""),
                placeholder="예: user@example.com",
                on_change=sync_widget_key, args=("email_widget", "email")
            )
            if 'email' in st.session_state.get("validation_errors", {}):
                st.error(st.session_state.validation_errors['email'])

        with col_phone:
            st.text_input(
                "연락처*",
                key="phone_widget",
                value=st.session_state.get("phone", ""),
                placeholder="예: 01012345678 (숫자만 입력)",
                on_change=sync_widget_key, args=("phone_widget", "phone")
            )
            if 'phone' in st.session_state.get("validation_errors", {}):
                st.error(st.session_state.validation_errors['phone'])

        st.markdown("---")
        st.text_input(
            "주소 (선택 사항)",
            key="address_widget",
            value=st.session_state.get("address", ""),
            placeholder="도로명 주소 또는 지번 주소",
            on_change=sync_widget_key, args=("address_widget", "address")
        )
        st.text_input(
            "직업 (선택 사항)",
            key="occupation_widget",
            value=st.session_state.get("occupation", ""),
            placeholder="직업을 입력하세요",
            on_change=sync_widget_key, args=("occupation_widget", "occupation")
        )
        st.text_area(
            "내원 목적 (선택 사항)",
            key="visit_reason_widget",
            value=st.session_state.get("visit_reason", ""),
            placeholder="예: 턱에서 소리가 나고 통증이 있어서 진료를 받고 싶습니다.",
            on_change=sync_widget_key, args=("visit_reason_widget", "visit_reason")
        )

    st.markdown("---")

    def _validate():
        # on_change 미호출 대비 강제 동기화
        sync_multiple_keys(field_mapping)
        st.session_state.validation_errors = {}
        ok = True
        messages = []
        if not st.session_state.get('name'):
            st.session_state.validation_errors['name'] = "이름은 필수 입력 항목입니다."
            messages.append("이름은 필수 입력 항목입니다.")
            ok = False
        if st.session_state.get('gender') == '선택 안 함':
            st.session_state.validation_errors['gender'] = "성별은 필수 선택 항목입니다."
            messages.append("성별은 필수 선택 항목입니다.")
            ok = False
        if not st.session_state.get('email'):
            st.session_state.validation_errors['email'] = "이메일은 필수 입력 항목입니다."
            messages.append("이메일은 필수 입력 항목입니다.")
            ok = False
        if not st.session_state.get('phone'):
            st.session_state.validation_errors['phone'] = "연락처는 필수 입력 항목입니다."
            messages.append("연락처는 필수 입력 항목입니다.")
            ok = False
        return (ok, messages) if not ok else True

    create_navigation_buttons(prev_step=0, next_step=2, validation_func=_validate)


def render_step_2_chief_complaint():
    st.title("주 호소 (Chief Complaint)")
    st.markdown("---")

    field_mapping = {
        "chief_complaint_widget": "chief_complaint",
        "chief_complaint_other_widget": "chief_complaint_other",
        "onset_widget": "onset"
    }

    with st.container(border=True):
        st.markdown("**이번에 병원을 방문한 주된 이유는 무엇인가요?**")
        st.radio(
            label="",
            options=[
                "턱 주변의 통증(턱 근육, 관자놀이, 귀 앞쪽)",
                "턱관절 소리/잠김",
                "턱 움직임 관련 두통",
                "기타 불편한 증상",
                "선택 안 함"
            ],
            key="chief_complaint_widget",
            index=4,
            label_visibility="collapsed",
            on_change=sync_widget_key, args=("chief_complaint_widget", "chief_complaint")
        )

        if st.session_state.get("chief_complaint") == "기타 불편한 증상":
            st.text_input(
                "기타 사유를 적어주세요:",
                key="chief_complaint_other_widget",
                value=st.session_state.get("chief_complaint_other", ""),
                on_change=sync_widget_key, args=("chief_complaint_other_widget", "chief_complaint_other")
            )
        else:
            st.session_state["chief_complaint_other"] = ""

        st.markdown("---")
        st.markdown("**문제가 처음 발생한 시기가 어떻게 되나요?**")
        onset_options = ["일주일 이내", "1개월 이내", "6개월 이내", "1년 이내", "1년 이상 전", "선택 안 함"]
        st.radio(
            label="",
            options=onset_options,
            index=onset_options.index(st.session_state.get("onset", "선택 안 함")),
            key="onset_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key, args=("onset_widget", "onset")
        )

    st.markdown("---")

    def _next_step():
        complaint = st.session_state.get("chief_complaint")
        if complaint in ["턱 주변의 통증(턱 근육, 관자놀이, 귀 앞쪽)", "턱 움직임 관련 두통"]:
            return 3
        if complaint == "턱관절 소리/잠김":
            return 5
        if complaint == "기타 불편한 증상":
            return 6
        return 2

    def _validate():
        sync_multiple_keys(field_mapping)
        complaint = st.session_state.get("chief_complaint")
        other_text = st.session_state.get("chief_complaint_other", "").strip()
        onset_selected = st.session_state.get("onset")
        messages, ok = [], True
        if complaint == "선택 안 함":
            messages.append("주 호소 항목을 선택해주세요.")
            ok = False
        elif complaint == "기타 불편한 증상" and not other_text:
            messages.append("기타 증상을 입력해주세요.")
            ok = False
        if onset_selected == "선택 안 함":
            messages.append("문제 발생 시기를 선택해주세요.")
            ok = False
        st.session_state.__next_step_for_2 = _next_step()
        return (ok, messages) if not ok else True

    next_step = st.session_state.get("__next_step_for_2", _next_step())
    create_navigation_buttons(prev_step=1, next_step=next_step, validation_func=_validate)
