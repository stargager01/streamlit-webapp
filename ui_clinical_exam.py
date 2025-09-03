 # ui_clinical_exam.py

import streamlit as st
from utils import (
    sync_widget_key,
    sync_multiple_keys,
    update_neck_none,
    update_neck_symptom,
    create_navigation_buttons,
)

def render_step_7_habits():
    st.title("습관 (Habits)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 해당되는 습관이 있나요?**")

        first_habits = {
            "이갈이 - 밤(수면 중)": "habit_bruxism_night",
            "이 악물기 - 낮": "habit_clenching_day",
            "이 악물기 - 밤(수면 중)": "habit_clenching_night"
        }

        st.checkbox(
            "없음",
            value=st.session_state.get("habit_none", False),
            key="habit_none_widget",
            on_change=sync_widget_key, args=("habit_none_widget", "habit_none")
        )
        none_checked = st.session_state.get("habit_none", False)

        for label, key in first_habits.items():
            widget_key = f"{key}_widget"
            st.checkbox(
                label,
                value=st.session_state.get(key, False),
                key=widget_key,
                on_change=sync_widget_key, args=(widget_key, key),
                disabled=none_checked
            )
            if not none_checked and key not in st.session_state:
                st.session_state[key] = False

        st.markdown("---")
        st.markdown("**다음 중 해당되는 습관이 있다면 모두 선택해주세요.**")

        additional_habits = [
            "옆으로 자는 습관", "코골이", "껌 씹기",
            "단단한 음식 선호(예: 견과류, 딱딱한 사탕 등)", "한쪽으로만 씹기",
            "혀 내밀기 및 밀기(이를 밀거나 입술 사이로 내미는 습관)", "손톱/입술/볼 물기",
            "손가락 빨기", "턱 괴기", "거북목/머리 앞으로 빼기",
            "음주", "흡연", "카페인"
        ]

        if "selected_habits" not in st.session_state:
            st.session_state.selected_habits = []

        for habit in additional_habits:
            widget_key = f"habit_{habit.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('-', '_').replace('.', '').replace(':', '')}_widget"
            checked = st.checkbox(habit, value=(habit in st.session_state.selected_habits), key=widget_key)
            if checked and habit not in st.session_state.selected_habits:
                st.session_state.selected_habits.append(habit)
            elif not checked and habit in st.session_state.selected_habits:
                st.session_state.selected_habits.remove(habit)

    st.markdown("---")

    def _validate():
        first_habit_labels = {
            "habit_bruxism_night": "이갈이 (밤)",
            "habit_clenching_day": "이 악물기 (낮)",
            "habit_clenching_night": "이 악물기 (밤)",
        }

        first_selected = []
        if st.session_state.get("habit_none"):
            first_selected.append("없음")
        else:
            for key, label in first_habit_labels.items():
                if st.session_state.get(key):
                    first_selected.append(label)

        habit_summary = ", ".join(first_selected) if first_selected else "없음"
        additional_summary = ", ".join(st.session_state.selected_habits) if st.session_state.selected_habits else "없음"

        st.session_state["habit_summary"] = habit_summary
        st.session_state["additional_habits"] = additional_summary
        st.session_state["full_habit_summary"] = f"주요 습관: {habit_summary}\n기타 습관: {additional_summary}"

        has_first = any([
            st.session_state.get("habit_bruxism_night", False),
            st.session_state.get("habit_clenching_day", False),
            st.session_state.get("habit_clenching_night", False),
            st.session_state.get("habit_none", False)
        ])

        if not has_first:
            return False, ["‘이갈이/이 악물기/없음’ 중에서 최소 한 가지를 선택해주세요."]

        return True

    create_navigation_buttons(prev_step=6, next_step=8, validation_func=_validate)


def render_step_8_rom_observations_1():
    st.title("턱 운동 범위 및 관찰 (Range of Motion & Observations)")
    st.markdown("---")
    st.markdown(
        "<span style='color:red;'>아래 항목은 실제 측정 및 검사가 필요할 수 있으며, 가능하신 부분만 기입해 주시면 됩니다. 나머지는 진료 중 확인할 수 있습니다.</span>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("---")
        st.subheader("자발적 개구 (Active Opening)")

        st.markdown("**스스로 입을 크게 벌렸을 때 어느 정도까지 벌릴 수 있나요? (의료진이 측정 후 기록)**")
        st.text_input(
            label="",
            key="active_opening_widget",
            value=st.session_state.get("active_opening", ""),
            on_change=sync_widget_key, args=("active_opening_widget", "active_opening"),
            label_visibility="collapsed"
        )

        st.markdown("**통증이 있나요?**")
        st.radio(
            label="",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("active_pain", "선택 안 함")),
            key="active_pain_widget",
            on_change=sync_widget_key, args=("active_pain_widget", "active_pain"),
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.subheader("수동적 개구 (Passive Opening)")

        st.markdown("**타인이 도와서 벌렸을 때 어느 정도까지 벌릴 수 있나요? (의료진이 측정 후 기록)**")
        st.text_input(
            label="",
            key="passive_opening_widget",
            value=st.session_state.get("passive_opening", ""),
            on_change=sync_widget_key, args=("passive_opening_widget", "passive_opening"),
            label_visibility="collapsed"
        )

        st.markdown("**통증이 있나요?**")
        st.radio(
            label="",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("passive_pain", "선택 안 함")),
            key="passive_pain_widget",
            on_change=sync_widget_key, args=("passive_pain_widget", "passive_pain"),
            label_visibility="collapsed"
        )

    st.markdown("---")

    def _validate():
        sync_multiple_keys({
            "active_opening_widget": "active_opening",
            "active_pain_widget": "active_pain",
            "passive_opening_widget": "passive_opening",
            "passive_pain_widget": "passive_pain"
        })
        return True

    create_navigation_buttons(prev_step=7, next_step=9, validation_func=_validate)


def render_step_9_rom_observations_2():
    st.title("턱 운동 범위 및 관찰 (Range of Motion & Observations)")
    st.markdown("---")
    st.markdown(
        "<span style='color:red;'>아래 항목은 실제 측정 및 검사가 필요할 수 있으며, 가능하신 부분만 기입해 주시면 됩니다. 나머지는 진료 중 확인할 수 있습니다.</span>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("---")
        st.subheader("턱 움직임 패턴 (Mandibular Movement Pattern)")
        st.markdown("**입을 벌리고 닫을 때 턱이 한쪽으로 치우치는 것 같나요?**")
        st.radio(
            label=" ",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("deviation", "선택 안 함")),
            key="deviation_widget",
            on_change=sync_widget_key, args=("deviation_widget", "deviation"),
            label_visibility="collapsed"
        )
        st.markdown("**편위(Deviation, 치우치지만 마지막에는 중앙으로 돌아옴)**")
        st.radio(
            label=" ",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("deviation2", "선택 안 함")),
            key="deviation2_widget",
            on_change=sync_widget_key, args=("deviation2_widget", "deviation2"),
            label_visibility="collapsed"
        )
        st.markdown("**편향(Deflection, 치우친 채 돌아오지 않음)**")
        st.radio(
            label="편향(Deflection): 치우치고 돌아오지 않음",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("deflection", "선택 안 함")),
            key="deflection_widget",
            on_change=sync_widget_key, args=("deflection_widget", "deflection"),
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("**앞으로 내밀기(Protrusion) ______ mm (의료진이 측정 후 기록)**")
        st.text_input(
            label="",
            key="protrusion_widget",
            value=st.session_state.get("protrusion", ""),
            on_change=sync_widget_key, args=("protrusion_widget", "protrusion"),
            label_visibility="collapsed"
        )

        st.radio(
            "**Protrusion 시 통증 여부**",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("protrusion_pain", "선택 안 함")),
            key="protrusion_pain_widget",
            on_change=sync_widget_key, args=("protrusion_pain_widget", "protrusion_pain")
        )

        st.markdown("---")
        st.markdown("**측방운동(Laterotrusion) 오른쪽: ______ mm (의료진이 측정 후 기록)**")
        st.text_input(
            label="",
            key="latero_right_widget",
            value=st.session_state.get("latero_right", ""),
            on_change=sync_widget_key, args=("latero_right_widget", "latero_right"),
            label_visibility="collapsed"
        )

        st.radio(
            "**Laterotrusion 오른쪽 통증 여부**",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("latero_right_pain", "선택 안 함")),
            key="latero_right_pain_widget",
            on_change=sync_widget_key, args=("latero_right_pain_widget", "latero_right_pain")
        )

        st.markdown("---")
        st.markdown("**측방운동(Laterotrusion) 왼쪽: ______ mm (의료진이 측정 후 기록)**")
        st.text_input(
            label="",
            key="latero_left_widget",
            value=st.session_state.get("latero_left", ""),
            on_change=sync_widget_key, args=("latero_left_widget", "latero_left"),
            label_visibility="collapsed"
        )

        st.radio(
            "**Laterotrusion 왼쪽 통증 여부**",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("latero_left_pain", "선택 안 함")),
            key="latero_left_pain_widget",
            on_change=sync_widget_key, args=("latero_left_pain_widget", "latero_left_pain")
        )

        st.markdown("---")
        st.markdown("**교합(Occlusion): 앞니(위, 아래)가 정중앙에서 잘 맞물리나요?**")
        st.radio(
            label="",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("occlusion", "선택 안 함")),
            key="occlusion_widget",
            on_change=sync_widget_key, args=("occlusion_widget", "occlusion"),
            label_visibility="collapsed"
        )

        if st.session_state.get("occlusion") == "아니오":
            st.markdown("**정중앙이 어느 쪽으로 어긋나는지:**")
            shift_value = st.session_state.get("occlusion_shift", "선택 안 함")
            shift_options = ["오른쪽", "왼쪽", "선택 안 함"]
            shift_index = shift_options.index(shift_value) if shift_value in shift_options else 2
            st.radio(
                label="",
                options=shift_options,
                index=shift_index,
                key="occlusion_shift_widget",
                on_change=sync_widget_key, args=("occlusion_shift_widget", "occlusion_shift"),
                label_visibility="collapsed"
            )
        else:
            st.session_state["occlusion_shift"] = ""

    st.markdown("---")

    def _validate():
        sync_multiple_keys({
            "deviation_widget": "deviation",
            "deviation2_widget": "deviation2",
            "deflection_widget": "deflection",
            "protrusion_widget": "protrusion",
            "protrusion_pain_widget": "protrusion_pain",
            "latero_right_widget": "latero_right",
            "latero_right_pain_widget": "latero_right_pain",
            "latero_left_widget": "latero_left",
            "latero_left_pain_widget": "latero_left_pain",
            "occlusion_widget": "occlusion",
            "occlusion_shift_widget": "occlusion_shift"
        })
        return True

    create_navigation_buttons(prev_step=8, next_step=10, validation_func=_validate)


def render_step_10_rom_observations_3():
    st.title("턱 운동 범위 및 관찰 (Range of Motion & Observations)")
    st.markdown("---")
    st.markdown(
        "<span style='color:red;'>아래 항목은 실제 측정 및 검사가 필요할 수 있으며, 가능하신 부분만 기입해 주시면 됩니다. 나머지는 진료 중 확인할 수 있습니다.</span>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("---")
        st.subheader("턱관절 소리 (TMJ Noise)")

        st.markdown("**오른쪽 - 입 벌릴 때**")
        st.radio(
            label="",
            options=["딸깍/소리", "없음", "선택 안 함"],
            index=["딸깍/소리", "없음", "선택 안 함"].index(st.session_state.get("tmj_noise_right_open", "선택 안 함")),
            key="tmj_noise_right_open_widget",
            on_change=sync_widget_key, args=("tmj_noise_right_open_widget", "tmj_noise_right_open"),
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("**왼쪽 - 입 벌릴 때**")
        st.radio(
            label="",
            options=["딸깍/소리", "없음", "선택 안 함"],
            index=["딸깍/소리", "없음", "선택 안 함"].index(st.session_state.get("tmj_noise_left_open", "선택 안 함")),
            key="tmj_noise_left_open_widget",
            on_change=sync_widget_key, args=("tmj_noise_left_open_widget", "tmj_noise_left_open"),
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("**오른쪽 - 입 다물 때**")
        st.radio(
            label="",
            options=["딸깍/소리", "없음", "선택 안 함"],
            index=["딸깍/소리", "없음", "선택 안 함"].index(st.session_state.get("tmj_noise_right_close", "선택 안 함")),
            key="tmj_noise_right_close_widget",
            on_change=sync_widget_key, args=("tmj_noise_right_close_widget", "tmj_noise_right_close"),
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("**왼쪽 - 입 다물 때**")
        st.radio(
            label="",
            options=["딸깍/소리", "없음", "선택 안 함"],
            index=["딸깍/소리", "없음", "선택 안 함"].index(st.session_state.get("tmj_noise_left_close", "선택 안 함")),
            key="tmj_noise_left_close_widget",
            on_change=sync_widget_key, args=("tmj_noise_left_close_widget", "tmj_noise_left_close"),
            label_visibility="collapsed"
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=9, next_step=11)


def render_step_11_palpation():
    st.title("근육 촉진 평가")
    st.markdown("---")

    with st.container(border=True):
        st.markdown(
            "<span style='color:red;'>아래 항목은 검사가 필요한 항목으로, 진료 중 확인할 수 있습니다.</span>",
            unsafe_allow_html=True
        )
        st.markdown("### 의료진 촉진 소견")

        palpation_fields = [
            ("측두근 촉진 소견", "palpation_temporalis_widget", "palpation_temporalis"),
            ("내측 익돌근 촉진 소견", "palpation_medial_pterygoid_widget", "palpation_medial_pterygoid"),
            ("외측 익돌근 촉진 소견", "palpation_lateral_pterygoid_widget", "palpation_lateral_pterygoid"),
            ("통증 위치 매핑 (지도 또는 상세 설명)", "pain_mapping_widget", "pain_mapping"),
        ]

        for label, widget_key, session_key in palpation_fields:
            st.markdown(f"**{label}**")
            st.text_area(
                label=label,
                key=widget_key,
                value=st.session_state.get(session_key, ""),
                on_change=sync_widget_key, args=(widget_key, session_key),
                placeholder="검사가 필요한 항목입니다.",
                label_visibility="collapsed"
            )

    st.markdown("---")

    def _validate():
        sync_multiple_keys({
            "palpation_temporalis_widget": "palpation_temporalis",
            "palpation_medial_pterygoid_widget": "palpation_medial_pterygoid",
            "palpation_lateral_pterygoid_widget": "palpation_lateral_pterygoid",
            "pain_mapping_widget": "pain_mapping",
        })
        return True

    create_navigation_buttons(prev_step=10, next_step=12, validation_func=_validate)
