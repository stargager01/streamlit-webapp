import streamlit as st
from utilsimport (
    sync_widget_key,
    update_neck_none,
    update_neck_symptom,
    create_navigation_buttons,
)


def render_step_12_ear_symptoms():
    st.title("귀 관련 증상 확인")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 해당되는 귀 증상이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "이명(귀에서 소리)",
            key="ear_symptom_tinnitus",
            value=st.session_state.get("ear_symptom_tinnitus", False)
        )
        st.checkbox(
            "귀 먹먹함",
            key="ear_symptom_fullness",
            value=st.session_state.get("ear_symptom_fullness", False)
        )
        st.checkbox(
            "청력 저하",
            key="ear_symptom_hearing_loss",
            value=st.session_state.get("ear_symptom_hearing_loss", False)
        )
        st.checkbox(
            "귀 통증",
            key="ear_symptom_pain",
            value=st.session_state.get("ear_symptom_pain", False)
        )
        st.checkbox(
            "해당 없음",
            key="ear_symptom_none",
            value=st.session_state.get("ear_symptom_none", False)
        )

        st.text_area(
            label="기타 귀 관련 증상이 있다면 기재해주세요:",
            key="ear_symptom_other_widget",
            value=st.session_state.get("ear_symptom_other", ""),
            on_change=lambda: st.session_state.update({"ear_symptom_other": st.session_state["ear_symptom_other_widget"]}),
            placeholder="예: 귀에서 압력감, 귀울림 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    # 단순 체크 기반이므로 유효성 검사 없이 버튼 생성
    create_navigation_buttons(prev_step=11, next_step=13)


def render_step_13_neck_shoulder():
    st.title("목/어깨 관련 증상")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 해당되는 증상이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "목 통증",
            key="neck_pain",
            value=st.session_state.get("neck_pain", False),
            on_change=update_neck_symptom,
            args=("neck_pain",)
        )
        st.checkbox(
            "어깨 통증",
            key="shoulder_pain",
            value=st.session_state.get("shoulder_pain", False),
            on_change=update_neck_symptom,
            args=("shoulder_pain",)
        )
        st.checkbox(
            "뻣뻣함/긴장감",
            key="stiffness",
            value=st.session_state.get("stiffness", False),
            on_change=update_neck_symptom,
            args=("stiffness",)
        )
        st.checkbox(
            "해당 없음",
            key="neck_none",
            value=st.session_state.get("neck_none", False),
            on_change=update_neck_none
        )

        st.text_area(
            label="기타 증상이 있다면 기재해주세요:",
            key="neck_other_widget",
            value=st.session_state.get("neck_other", ""),
            on_change=lambda: st.session_state.update({"neck_other": st.session_state["neck_other_widget"]}),
            placeholder="예: 팔 저림, 등 통증 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=12, next_step=14)


def render_step_14_stress_history():
    st.title("정서적 스트레스 이력")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**스트레스, 불안, 우울감 등을 많이 느끼시나요?**")
        stress_options = ["예", "아니오", "선택 안 함"]
        st.radio(
            label="",
            options=stress_options,
            index=stress_options.index(st.session_state.get("stress_radio", "선택 안 함")),
            key="stress_radio_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("stress_radio_widget", "stress_radio")
        )

        st.markdown("---")
        st.markdown("**있다면 간단히 기재해 주세요:**")
        st.text_area(
            label="",
            key="stress_detail_widget",
            value=st.session_state.get("stress_detail", ""),
            on_change=sync_widget_key,
            args=("stress_detail_widget", "stress_detail"),
            placeholder="예: 최근 업무 스트레스, 가족 문제 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    def validate_stress_step():
        if st.session_state.get("stress_radio") == "선택 안 함":
            st.warning("스트레스 여부를 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=13, next_step=15, validation_func=validate_stress_step)


def render_step_15_past_dental_history():
    st.title("과거 치과 치료 이력")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**과거에 다음과 같은 치과 치료를 받은 적이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "교정 치료",
            key="dental_history_orthodontics",
            value=st.session_state.get("dental_history_orthodontics", False)
        )
        st.checkbox(
            "턱관절 치료",
            key="dental_history_tmj",
            value=st.session_state.get("dental_history_tmj", False)
        )
        st.checkbox(
            "보철 치료 (임플란트, 크라운 등)",
            key="dental_history_prosthetics",
            value=st.session_state.get("dental_history_prosthetics", False)
        )
        st.checkbox(
            "외과적 치료 (발치, 수술 등)",
            key="dental_history_surgery",
            value=st.session_state.get("dental_history_surgery", False)
        )
        st.checkbox(
            "해당 없음",
            key="dental_history_none",
            value=st.session_state.get("dental_history_none", False)
        )

        st.text_area(
            label="기타 치과 치료 이력이 있다면 기재해주세요:",
            key="dental_history_other_widget",
            value=st.session_state.get("dental_history_other", ""),
            on_change=lambda: st.session_state.update({"dental_history_other": st.session_state["dental_history_other_widget"]}),
            placeholder="예: 턱 수술, 교합 조정 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    def validate_dental_history():
        selected = any([
            st.session_state.get("dental_history_orthodontics"),
            st.session_state.get("dental_history_tmj"),
            st.session_state.get("dental_history_prosthetics"),
            st.session_state.get("dental_history_surgery"),
            st.session_state.get("dental_history_none")
        ])
        if not selected:
            st.warning("치과 치료 이력을 최소 1개 이상 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=14, next_step=16, validation_func=validate_dental_history)


def render_step_16_past_medical_history():
    st.title("과거 병력 및 치료 이력")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 과거에 진단받거나 치료받은 질환이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "고혈압",
            key="medical_history_hypertension",
            value=st.session_state.get("medical_history_hypertension", False)
        )
        st.checkbox(
            "당뇨병",
            key="medical_history_diabetes",
            value=st.session_state.get("medical_history_diabetes", False)
        )
        st.checkbox(
            "심장 질환",
            key="medical_history_heart",
            value=st.session_state.get("medical_history_heart", False)
        )
        st.checkbox(
            "신경계 질환",
            key="medical_history_neuro",
            value=st.session_state.get("medical_history_neuro", False)
        )
        st.checkbox(
            "정신과적 질환",
            key="medical_history_psych",
            value=st.session_state.get("medical_history_psych", False)
        )
        st.checkbox(
            "해당 없음",
            key="medical_history_none",
            value=st.session_state.get("medical_history_none", False)
        )

        st.text_area(
            label="기타 병력이나 치료 이력이 있다면 기재해주세요:",
            key="medical_history_other_widget",
            value=st.session_state.get("medical_history_other", ""),
            on_change=lambda: st.session_state.update({"medical_history_other": st.session_state["medical_history_other_widget"]}),
            placeholder="예: 갑상선 질환, 암 치료 이력 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    def validate_medical_history():
        selected = any([
            st.session_state.get("medical_history_hypertension"),
            st.session_state.get("medical_history_diabetes"),
            st.session_state.get("medical_history_heart"),
            st.session_state.get("medical_history_neuro"),
            st.session_state.get("medical_history_psych"),
            st.session_state.get("medical_history_none")
        ])
        if not selected:
            st.warning("과거 병력을 최소 1개 이상 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=15, next_step=17, validation_func=validate_medical_history)


def render_step_17_provocation_tests():
    st.title("유발 검사 반응")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 동작을 수행했을 때 증상이 유발되거나 악화되었나요? (복수 선택 가능)**")

        st.checkbox(
            "입을 크게 벌릴 때",
            key="provocation_opening",
            value=st.session_state.get("provocation_opening", False)
        )
        st.checkbox(
            "입을 다물 때",
            key="provocation_closing",
            value=st.session_state.get("provocation_closing", False)
        )
        st.checkbox(
            "입을 좌우로 움직일 때",
            key="provocation_lateral",
            value=st.session_state.get("provocation_lateral", False)
        )
        st.checkbox(
            "입을 앞으로 내밀 때",
            key="provocation_protrusion",
            value=st.session_state.get("provocation_protrusion", False)
        )
        st.checkbox(
            "해당 없음",
            key="provocation_none",
            value=st.session_state.get("provocation_none", False)
        )

        st.text_area(
            label="기타 유발 동작이나 반응이 있다면 기재해주세요:",
            key="provocation_other_widget",
            value=st.session_state.get("provocation_other", ""),
            on_change=lambda: st.session_state.update({"provocation_other": st.session_state["provocation_other_widget"]}),
            placeholder="예: 하품, 음식 씹기, 특정 자세 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=16, next_step=18)


def render_step_18_functional_impact():
    st.title("일상생활에 미치는 영향")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**턱관절 증상이 다음 활동에 영향을 미치나요? (복수 선택 가능)**")

        st.checkbox(
            "식사하기",
            key="impact_eating",
            value=st.session_state.get("impact_eating", False)
        )
        st.checkbox(
            "말하기",
            key="impact_speaking",
            value=st.session_state.get("impact_speaking", False)
        )
        st.checkbox(
            "하품/입 벌리기",
            key="impact_yawning",
            value=st.session_state.get("impact_yawning", False)
        )
        st.checkbox(
            "노래/발성",
            key="impact_singing",
            value=st.session_state.get("impact_singing", False)
        )
        st.checkbox(
            "해당 없음",
            key="impact_none",
            value=st.session_state.get("impact_none", False)
        )

        st.text_area(
            label="기타 영향을 받는 활동이 있다면 기재해주세요:",
            key="impact_other_widget",
            value=st.session_state.get("impact_other", ""),
            on_change=lambda: st.session_state.update({"impact_other": st.session_state["impact_other_widget"]}),
            placeholder="예: 운동, 집중력 저하, 수면 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    def validate_functional_impact():
        selected = any([
            st.session_state.get("impact_eating"),
            st.session_state.get("impact_speaking"),
            st.session_state.get("impact_yawning"),
            st.session_state.get("impact_singing"),
            st.session_state.get("impact_none")
        ])
        if not selected:
            st.warning("영향을 받는 활동을 최소 1개 이상 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=17, next_step=19, validation_func=validate_functional_impact)
