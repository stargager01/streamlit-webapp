 import streamlit as st
from utils import create_navigation_buttons


def render_step_7_habits():
    st.title("습관 및 행동 양상")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 중 해당되는 습관이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "수면 중 이갈이",
            key="habit_bruxism_night",
            value=st.session_state.get("habit_bruxism_night", False)
        )
        st.checkbox(
            "주간 이 악물기",
            key="habit_clenching_day",
            value=st.session_state.get("habit_clenching_day", False)
        )
        st.checkbox(
            "수면 중 이 악물기",
            key="habit_clenching_night",
            value=st.session_state.get("habit_clenching_night", False)
        )
        st.checkbox(
            "해당 없음",
            key="habit_none",
            value=st.session_state.get("habit_none", False)
        )

        st.markdown("---")
        st.markdown("**기타 습관이 있다면 자유롭게 기재해주세요:**")
        st.text_area(
            label="",
            key="habit_other_widget",
            value=st.session_state.get("habit_other", ""),
            on_change=lambda: st.session_state.update({"habit_other": st.session_state["habit_other_widget"]}),
            placeholder="예: 턱 괴기, 손톱 물어뜯기 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    def validate_habits():
        has_main = any([
            st.session_state.get("habit_bruxism_night"),
            st.session_state.get("habit_clenching_day"),
            st.session_state.get("habit_clenching_night"),
            st.session_state.get("habit_none")
        ])
        if not has_main:
            st.warning("‘이갈이/이 악물기/없음’ 중에서 최소 한 가지를 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=6, next_step=8, validation_func=validate_habits)


def render_step_8_rom_observations_1():
    st.title("턱관절 움직임 범위 관찰 (1/2)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**입을 벌릴 때의 움직임을 관찰해주세요.**")
        st.radio(
            label="입 벌릴 때 턱이 한쪽으로 치우치나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_deviation", "선택 안 함")),
            key="jaw_deviation_widget",
            on_change=lambda: st.session_state.update({"jaw_deviation": st.session_state["jaw_deviation_widget"]})
        )

        st.radio(
            label="입을 벌릴 때 턱이 흔들리거나 비정상적인 움직임이 있나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_instability", "선택 안 함")),
            key="jaw_instability_widget",
            on_change=lambda: st.session_state.update({"jaw_instability": st.session_state["jaw_instability_widget"]})
        )

        st.radio(
            label="입을 벌릴 때 통증이 있나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_opening_pain", "선택 안 함")),
            key="jaw_opening_pain_widget",
            on_change=lambda: st.session_state.update({"jaw_opening_pain": st.session_state["jaw_opening_pain_widget"]})
        )

        st.radio(
            label="입을 벌릴 때 소리가 나나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_opening_sound", "선택 안 함")),
            key="jaw_opening_sound_widget",
            on_change=lambda: st.session_state.update({"jaw_opening_sound": st.session_state["jaw_opening_sound_widget"]})
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=7, next_step=9)


def render_step_9_rom_observations_2():
    st.title("턱관절 움직임 범위 관찰 (2/2)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**입을 다물 때의 움직임을 관찰해주세요.**")

        st.radio(
            label="입을 다물 때 턱이 한쪽으로 치우치나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_closing_deviation", "선택 안 함")),
            key="jaw_closing_deviation_widget",
            on_change=lambda: st.session_state.update({"jaw_closing_deviation": st.session_state["jaw_closing_deviation_widget"]})
        )

        st.radio(
            label="입을 다물 때 턱이 흔들리거나 비정상적인 움직임이 있나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_closing_instability", "선택 안 함")),
            key="jaw_closing_instability_widget",
            on_change=lambda: st.session_state.update({"jaw_closing_instability": st.session_state["jaw_closing_instability_widget"]})
        )

        st.radio(
            label="입을 다물 때 통증이 있나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_closing_pain", "선택 안 함")),
            key="jaw_closing_pain_widget",
            on_change=lambda: st.session_state.update({"jaw_closing_pain": st.session_state["jaw_closing_pain_widget"]})
        )

        st.radio(
            label="입을 다물 때 소리가 나나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_closing_sound", "선택 안 함")),
            key="jaw_closing_sound_widget",
            on_change=lambda: st.session_state.update({"jaw_closing_sound": st.session_state["jaw_closing_sound_widget"]})
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=8, next_step=10)


def render_step_10_rom_observations_3():
    st.title("턱관절 움직임 범위 관찰 (3/3)")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**측면 움직임을 관찰해주세요.**")

        st.radio(
            label="턱을 좌우로 움직일 때 한쪽으로 제한되거나 비대칭적인가요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_lateral_asymmetry", "선택 안 함")),
            key="jaw_lateral_asymmetry_widget",
            on_change=lambda: st.session_state.update({"jaw_lateral_asymmetry": st.session_state["jaw_lateral_asymmetry_widget"]})
        )

        st.radio(
            label="측면 움직임 시 통증이 있나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_lateral_pain", "선택 안 함")),
            key="jaw_lateral_pain_widget",
            on_change=lambda: st.session_state.update({"jaw_lateral_pain": st.session_state["jaw_lateral_pain_widget"]})
        )

        st.radio(
            label="측면 움직임 시 소리가 나나요?",
            options=["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("jaw_lateral_sound", "선택 안 함")),
            key="jaw_lateral_sound_widget",
            on_change=lambda: st.session_state.update({"jaw_lateral_sound": st.session_state["jaw_lateral_sound_widget"]})
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=9, next_step=11)


def render_step_11_palpation():
    st.title("촉진 검사: 통증 유무 확인")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**다음 부위를 눌렀을 때 통증이 있나요? (복수 선택 가능)**")

        st.checkbox(
            "관자놀이 근육(측두근)",
            key="palpation_temporalis",
            value=st.session_state.get("palpation_temporalis", False)
        )
        st.checkbox(
            "턱을 움직이는 근육(교근)",
            key="palpation_masseter",
            value=st.session_state.get("palpation_masseter", False)
        )
        st.checkbox(
            "턱관절 앞쪽(관절 돌기 부위)",
            key="palpation_tmj_front",
            value=st.session_state.get("palpation_tmj_front", False)
        )
        st.checkbox(
            "귀 앞쪽(외이도 앞)",
            key="palpation_tmj_ear",
            value=st.session_state.get("palpation_tmj_ear", False)
        )
        st.checkbox(
            "목 근육(흉쇄유돌근 등)",
            key="palpation_neck",
            value=st.session_state.get("palpation_neck", False)
        )
        st.checkbox(
            "어깨 부위",
            key="palpation_shoulder",
            value=st.session_state.get("palpation_shoulder", False)
        )
        st.checkbox(
            "해당 없음",
            key="palpation_none",
            value=st.session_state.get("palpation_none", False)
        )

        st.text_area(
            label="기타 통증 부위가 있다면 기재해주세요:",
            key="palpation_other_widget",
            value=st.session_state.get("palpation_other", ""),
            on_change=lambda: st.session_state.update({"palpation_other": st.session_state["palpation_other_widget"]}),
            placeholder="예: 턱 아래쪽, 안면 중앙 등",
            label_visibility="collapsed"
        )

    st.markdown("---")

    create_navigation_buttons(prev_step=10, next_step=12)
