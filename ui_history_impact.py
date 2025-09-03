# ui_history_impact.py

import streamlit as st
from utils import (
    sync_widget_key,
    update_neck_none,
    update_neck_symptom,
    create_navigation_buttons,
)

# ---------------------------
# STEP 12: 귀 관련 증상
# ---------------------------
def render_step_12_ear_symptoms():
    st.title("귀 관련 증상")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 귀와 관련된 증상이 있으신가요?**")

        ear_symptoms = ["이명 (귀울림)", "귀가 먹먹한 느낌", "귀 통증", "청력 저하"]

        st.session_state.setdefault("selected_ear_symptoms", [])
        st.session_state.setdefault("ear_symptom_other", "")

        def toggle_ear_symptom_none():
            if st.session_state.ear_symptom_none:
                st.session_state.selected_ear_symptoms = ["없음"]
            elif "없음" in st.session_state.selected_ear_symptoms:
                st.session_state.selected_ear_symptoms.remove("없음")

        st.checkbox(
            "없음",
            key="ear_symptom_none",
            value="없음" in st.session_state.selected_ear_symptoms,
            on_change=toggle_ear_symptom_none,
        )

        disabled = "없음" in st.session_state.selected_ear_symptoms

        for symptom in ear_symptoms:
            key = f"ear_symptom_{symptom}"
            default = symptom in st.session_state.selected_ear_symptoms

            def make_callback(s=symptom):
                def cb():
                    if st.session_state.get(f"ear_symptom_{s}"):
                        if s not in st.session_state.selected_ear_symptoms:
                            st.session_state.selected_ear_symptoms.append(s)
                    else:
                        if s in st.session_state.selected_ear_symptoms:
                            st.session_state.selected_ear_symptoms.remove(s)
                return cb

            st.checkbox(symptom, key=key, value=default, disabled=disabled, on_change=make_callback())

    st.markdown("---")

    def validate():
        symptoms = st.session_state.get("selected_ear_symptoms", [])
        if not symptoms:
            return False, ["귀 관련 증상을 한 가지 이상 선택하거나 '없음'을 선택해주세요."]
        if "없음" in symptoms and len(symptoms) > 1:
            return False, ["'없음'과 다른 증상을 동시에 선택할 수 없습니다. 다시 확인해주세요."]
        return True, []

    create_navigation_buttons(prev_step=11, next_step=13, validation_func=validate)


# ---------------------------
# STEP 13: 경추/목/어깨 관련 증상
# ---------------------------
def render_step_13_neck_shoulder():
    st.title("경추/목/어깨 관련 증상")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중의 증상이 있으신가요?**")

        st.checkbox(
            "없음",
            value=st.session_state.get("neck_none", False),
            key="neck_none",
            on_change=update_neck_none,
        )

        st.checkbox(
            "목 통증",
            value=st.session_state.get("neck_pain", False),
            key="neck_pain",
            on_change=update_neck_symptom,
            args=("neck_pain",),
            disabled=st.session_state.get("neck_none", False),
        )

        st.checkbox(
            "어깨 통증",
            value=st.session_state.get("shoulder_pain", False),
            key="shoulder_pain",
            on_change=update_neck_symptom,
            args=("shoulder_pain",),
            disabled=st.session_state.get("neck_none", False),
        )

        st.checkbox(
            "뻣뻣함(강직감)",
            value=st.session_state.get("stiffness", False),
            key="stiffness",
            on_change=update_neck_symptom,
            args=("stiffness",),
            disabled=st.session_state.get("neck_none", False),
        )

        st.session_state.neck_shoulder_symptoms = {
            "목 통증": st.session_state.get("neck_pain", False),
            "어깨 통증": st.session_state.get("shoulder_pain", False),
            "뻣뻣함(강직감)": st.session_state.get("stiffness", False),
        }

    st.markdown("---")
    with st.container(border=True):
        st.markdown("**다음 중 해당되는 증상이 있다면 모두 선택해주세요. (복수 선택 가능)**")
        st.session_state.additional_symptoms = {
            "눈 통증": st.checkbox("눈 통증", key="eye_pain"),
            "코 통증": st.checkbox("코 통증", key="nose_pain"),
            "목구멍 통증": st.checkbox("목구멍 통증", key="throat_pain"),
        }

    st.markdown("---")
    with st.container(border=True):
        st.markdown("**목 외상 관련 이력이 있으신가요?**")
        st.radio(
            label="",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("neck_trauma_radio", "선택 안 함")),
            key="neck_trauma_radio_widget",
            on_change=sync_widget_key,
            args=("neck_trauma_radio_widget", "neck_trauma_radio"),
            label_visibility="collapsed",
        )

    def validate():
        trauma_selected = st.session_state.get("neck_trauma_radio") in ["예", "아니오"]
        symptoms_selected = (
            st.session_state.get("neck_none", False)
            or st.session_state.get("neck_pain", False)
            or st.session_state.get("shoulder_pain", False)
            or st.session_state.get("stiffness", False)
        )

        if st.session_state.get("neck_none", False) and (
            st.session_state.get("neck_pain", False)
            or st.session_state.get("shoulder_pain", False)
            or st.session_state.get("stiffness", False)
        ):
            return False, ["'없음'과 다른 증상을 동시에 선택할 수 없습니다. 다시 확인해주세요."]
        if not symptoms_selected:
            return False, ["증상에서 최소 하나를 선택하거나 '없음'을 체크해주세요."]
        if not trauma_selected:
            return False, ["목 외상 여부를 선택해주세요."]
        return True, []

    create_navigation_buttons(prev_step=12, next_step=14, validation_func=validate)


# ---------------------------
# STEP 14: 정서적 스트레스 이력
# ---------------------------
def render_step_14_stress_history():
    st.title("정서적 스트레스 이력")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**스트레스, 불안, 우울감 등을 많이 느끼시나요?**")

        stress_options = ["예", "아니오", "선택 안 함"]
        st.radio(
            label="",
            options=stress_options,
            key="stress_radio_widget",
            index=stress_options.index(st.session_state.get("stress_radio", "선택 안 함")),
            on_change=sync_widget_key,
            args=("stress_radio_widget", "stress_radio"),
            label_visibility="collapsed",
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
            label_visibility="collapsed",
        )

    st.markdown("---")

    def validate():
        if st.session_state.get("stress_radio") == "선택 안 함":
            return False, ["스트레스 여부를 선택해주세요."]
        return True, []

    create_navigation_buttons(prev_step=13, next_step=15, validation_func=validate)


# ---------------------------
# STEP 15: 과거 치과적 이력
# ---------------------------
def render_step_15_past_dental_history():
    st.title("과거 치과적 이력 (Past Dental History)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**교정치료(치아 교정) 경험**")
        ortho_options = ["예", "아니오", "선택 안 함"]
        st.radio(
            "",
            ortho_options,
            index=ortho_options.index(st.session_state.get("ortho_exp", "선택 안 함")),
            key="ortho_exp_widget",
            on_change=sync_widget_key,
            args=("ortho_exp_widget", "ortho_exp"),
            label_visibility="collapsed",
        )
        st.text_input(
            "예라면 언제, 얼마나 받았는지 적어주세요:",
            key="ortho_detail_widget",
            value=st.session_state.get("ortho_detail", ""),
            on_change=sync_widget_key,
            args=("ortho_detail_widget", "ortho_detail"),
        )

        st.markdown("---")
        st.markdown("**보철치료(의치, 브리지, 임플란트 등) 경험**")
        prosth_options = ["예", "아니오", "선택 안 함"]
        st.radio(
            "",
            prosth_options,
            index=prosth_options.index(st.session_state.get("prosth_exp", "선택 안 함")),
            key="prosth_exp_widget",
            on_change=sync_widget_key,
            args=("prosth_exp_widget", "prosth_exp"),
            label_visibility="collapsed",
        )
        st.text_input(
            "예라면 어떤 치료였는지 적어주세요:",
            key="prosth_detail_widget",
            value=st.session_state.get("prosth_detail", ""),
            on_change=sync_widget_key,
            args=("prosth_detail_widget", "prosth_detail"),
        )

        st.markdown("---")
        st.markdown("**기타 치과 치료 이력 (주요 치과 시술, 수술 등)**")
        st.text_area(
            "",
            key="other_dental_widget",
            value=st.session_state.get("other_dental", ""),
            on_change=sync_widget_key,
            args=("other_dental_widget", "other_dental"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**이전에 턱관절 질환 치료를 받은 적 있나요?**")
        st.radio(
            "",
            ["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("tmd_treatment_history", "선택 안 함")),
            key="tmd_treatment_history_widget",
            on_change=sync_widget_key,
            args=("tmd_treatment_history_widget", "tmd_treatment_history"),
            label_visibility="collapsed",
        )
        if st.session_state.get("tmd_treatment_history") == "예":
            st.text_input(
                "어떤 치료를 받으셨나요?",
                key="tmd_treatment_detail_widget",
                value=st.session_state.get("tmd_treatment_detail", ""),
                on_change=sync_widget_key,
                args=("tmd_treatment_detail_widget", "tmd_treatment_detail"),
            )
            st.text_input(
                "해당 치료에 대한 반응(효과나 문제점 등):",
                key="tmd_treatment_response_widget",
                value=st.session_state.get("tmd_treatment_response", ""),
                on_change=sync_widget_key,
                args=("tmd_treatment_response_widget", "tmd_treatment_response"),
            )
            st.text_input(
                "현재 복용 중인 턱관절 관련 약물이 있다면 입력해주세요:",
                key="tmd_current_medications_widget",
                value=st.session_state.get("tmd_current_medications", ""),
                on_change=sync_widget_key,
                args=("tmd_current_medications_widget", "tmd_current_medications"),
            )
        else:
            st.session_state["tmd_treatment_detail"] = ""
            st.session_state["tmd_treatment_response"] = ""
            st.session_state["tmd_current_medications"] = ""

    st.markdown("---")

    def validate():
        errors = []
        if st.session_state.get("ortho_exp") == "선택 안 함":
            errors.append("교정치료 경험 여부를 선택해주세요.")
        if st.session_state.get("prosth_exp") == "선택 안 함":
            errors.append("보철치료 경험 여부를 선택해주세요.")
        if st.session_state.get("tmd_treatment_history") == "선택 안 함":
            errors.append("턱관절 치료 경험 여부를 선택해주세요.")
        if errors:
            return False, errors
        return True, []

    create_navigation_buttons(prev_step=14, next_step=16, validation_func=validate)


# ---------------------------
# STEP 16: 과거 의과적 이력
# ---------------------------
def render_step_16_past_medical_history():
    st.title("과거 의과적 이력 (Past Medical History)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**과거에 앓았던 질환, 입원 등 주요 의학적 이력이 있다면 적어주세요:**")
        st.text_area(
            label="",
            key="past_history_widget",
            value=st.session_state.get("past_history", ""),
            on_change=sync_widget_key,
            args=("past_history_widget", "past_history"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**현재 복용 중인 약이 있다면 적어주세요:**")
        st.text_area(
            label="",
            key="current_medications_widget",
            value=st.session_state.get("current_medications", ""),
            on_change=sync_widget_key,
            args=("current_medications_widget", "current_medications"),
            label_visibility="collapsed",
        )

    st.markdown("---")
    create_navigation_buttons(prev_step=15, next_step=17)


# ---------------------------
# STEP 17: 자극 검사
# ---------------------------
def render_step_17_provocation_tests():
    st.title("자극 검사 (Provocation Tests)")
    st.markdown("---")

    st.markdown(
        "<span style='color:red;'>아래 항목은 실제 측정 및 검사가 필요할 수 있으며, 가능하신 부분만 기입해 주시면 됩니다.</span>",
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("**오른쪽으로 어금니를 강하게 물 때:**")
        st.radio(
            label="",
            options=["통증 있음", "통증 없음", "선택 안 함"],
            key="bite_right_widget",
            index=["통증 있음", "통증 없음", "선택 안 함"].index(st.session_state.get("bite_right", "선택 안 함")),
            on_change=sync_widget_key,
            args=("bite_right_widget", "bite_right"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**왼쪽으로 어금니를 강하게 물 때:**")
        st.radio(
            label="",
            options=["통증 있음", "통증 없음", "선택 안 함"],
            key="bite_left_widget",
            index=["통증 있음", "통증 없음", "선택 안 함"].index(st.session_state.get("bite_left", "선택 안 함")),
            on_change=sync_widget_key,
            args=("bite_left_widget", "bite_left"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**압력 가하기 (Loading Test):**")
        st.radio(
            label="",
            options=["통증 있음", "통증 없음", "선택 안 함"],
            key="loading_test_widget",
            index=["통증 있음", "통증 없음", "선택 안 함"].index(st.session_state.get("loading_test", "선택 안 함")),
            on_change=sync_widget_key,
            args=("loading_test_widget", "loading_test"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**저항 검사 (Resistance Test, 턱 움직임 막기):**")
        st.radio(
            label="",
            options=["통증 있음", "통증 없음", "선택 안 함"],
            key="resistance_test_widget",
            index=["통증 있음", "통증 없음", "선택 안 함"].index(st.session_state.get("resistance_test", "선택 안 함")),
            on_change=sync_widget_key,
            args=("resistance_test_widget", "resistance_test"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**치아 마모 (Attrition)**")
        st.radio(
            label="",
            options=["경미", "중간", "심함", "선택 안 함"],
            key="attrition_widget",
            index=["경미", "중간", "심함", "선택 안 함"].index(st.session_state.get("attrition", "선택 안 함")),
            on_change=sync_widget_key,
            args=("attrition_widget", "attrition"),
            label_visibility="collapsed",
        )

    st.markdown("---")
    create_navigation_buttons(prev_step=16, next_step=18)


# ---------------------------
# STEP 18: 기능 평가
# ---------------------------
def render_step_18_functional_impact():
    st.title("기능 평가 (Functional Impact)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**턱관절 증상으로 인해 일상생활(음식 섭취, 말하기, 하품 등)에 불편함을 느끼시나요?**")
        st.radio(
            label="일상생활 영향",
            options=["전혀 불편하지 않음", "약간 불편함", "자주 불편함", "매우 불편함", "선택 안 함"],
            index=["전혀 불편하지 않음", "약간 불편함", "자주 불편함", "매우 불편함", "선택 안 함"].index(
                st.session_state.get("impact_daily", "선택 안 함")
            ),
            key="impact_daily",
            on_change=sync_widget_key,
            args=("impact_daily", "impact_daily"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**턱관절 증상으로 인해 직장 업무나 학업 성과에 영향을 받은 적이 있나요?**")
        st.radio(
            label="직장/학교 영향",
            options=[
                "전혀 영향 없음",
                "약간 집중에 어려움 있음",
                "자주 집중이 힘들고 성과 저하 경험",
                "매우 큰 영향으로 일/학업 중단 고려한 적 있음",
                "선택 안 함",
            ],
            index=[
                "전혀 영향 없음",
                "약간 집중에 어려움 있음",
                "자주 집중이 힘들고 성과 저하 경험",
                "매우 큰 영향으로 일/학업 중단 고려한 적 있음",
                "선택 안 함",
            ].index(st.session_state.get("impact_work", "선택 안 함")),
            key="impact_work",
            on_change=sync_widget_key,
            args=("impact_work", "impact_work"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**턱관절 증상이 귀하의 전반적인 삶의 질에 얼마나 영향을 미치고 있다고 느끼시나요?**")
        st.radio(
            label="삶의 질 영향",
            options=["전혀 영향을 미치지 않음", "약간 영향을 미침", "영향을 많이 받음", "심각하게 삶의 질 저하", "선택 안 함"],
            index=["전혀 영향을 미치지 않음", "약간 영향을 미침", "영향을 많이 받음", "심각하게 삶의 질 저하", "선택 안 함"].index(
                st.session_state.get("impact_quality_of_life", "선택 안 함")
            ),
            key="impact_quality_of_life",
            on_change=sync_widget_key,
            args=("impact_quality_of_life", "impact_quality_of_life"),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**최근 2주간 수면의 질은 어떠셨나요?**")
        st.radio(
            label="수면 질",
            options=["좋음", "보통", "나쁨", "매우 나쁨", "선택 안 함"],
            index=["좋음", "보통", "나쁨", "매우 나쁨", "선택 안 함"].index(
                st.session_state.get("sleep_quality", "선택 안 함")
            ),
            key="sleep_quality",
            on_change=sync_widget_key,
            args=("sleep_quality", "sleep_quality"),
            label_visibility="collapsed",
        )

        st.markdown("**수면의 질이 턱관절 증상(통증, 근육 경직 등)에 영향을 준다고 느끼시나요?**")
        st.radio(
            label="수면과 턱관절 질환 연관성",
            options=["영향을 미침", "영향을 미치지 않음", "잘 모르겠음", "선택 안 함"],
            index=["영향을 미침", "영향을 미치지 않음", "잘 모르겠음", "선택 안 함"].index(
                st.session_state.get("sleep_tmd_relation", "선택 안 함")
            ),
            key="sleep_tmd_relation",
            on_change=sync_widget_key,
            args=("sleep_tmd_relation", "sleep_tmd_relation"),
            label_visibility="collapsed",
        )

    st.markdown("---")

    def validate():
        errors = []
        if st.session_state.get("impact_daily") == "선택 안 함":
            errors.append("일상생활 영향 여부를 선택해주세요.")
        if st.session_state.get("impact_work") == "선택 안 함":
            errors.append("직장/학교 영향 여부를 선택해주세요.")
        if st.session_state.get("impact_quality_of_life") == "선택 안 함":
            errors.append("삶의 질 영향 여부를 선택해주세요.")
        if st.session_state.get("sleep_quality") == "선택 안 함":
            errors.append("수면의 질을 선택해주세요.")
        if st.session_state.get("sleep_tmd_relation") == "선택 안 함":
            errors.append("수면과 턱관절 연관성 여부를 선택해주세요.")

        if errors:
            return False, errors
        return True, []

    create_navigation_buttons(prev_step=17, next_step=19, validation_func=validate)
