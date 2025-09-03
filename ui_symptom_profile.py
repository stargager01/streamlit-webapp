# ui_symptom_profile.py

import streamlit as st
from utils import (
    sync_widget_key,
    sync_multiple_keys,
    update_headache_frequency,
    reset_headache_details,
    create_navigation_buttons,
)

def render_step_3_pain_profile():
    st.title("현재 증상 (통증 양상)")
    st.markdown("---")

    field_mapping = {
        "jaw_aggravation_widget": "jaw_aggravation",
        "pain_quality_widget": "pain_quality",
        "pain_quality_other_widget": "pain_quality_other",
    }

    with st.container(border=True):
        st.markdown(
            "**턱을 움직이거나 씹기, 말하기 등의 기능 또는 악습관(이갈이, 턱 괴기 등)으로 인해 통증이 악화되나요?**"
        )
        st.radio(
            label="악화 여부",
            options=["예", "아니오", "선택 안 함"],
            key="jaw_aggravation_widget",
            index=["예", "아니오", "선택 안 함"].index(
                st.session_state.get("jaw_aggravation", "선택 안 함")
            ),
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("jaw_aggravation_widget", "jaw_aggravation"),
        )

        st.markdown("---")
        st.markdown(
            "**통증을 어떻게 표현하시겠습니까? (예: 둔함, 날카로움, 욱신거림 등)**"
        )
        st.radio(
            label="통증 양상",
            options=["둔함", "날카로움", "욱신거림", "간헐적", "선택 안 함"],
            key="pain_quality_widget",
            index=["둔함", "날카로움", "욱신거림", "간헐적", "선택 안 함"].index(
                st.session_state.get("pain_quality", "선택 안 함")
            ),
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("pain_quality_widget", "pain_quality"),
        )

    st.markdown("---")

    def validate_pain_profile():
        sync_multiple_keys(field_mapping)
        if st.session_state.get("jaw_aggravation") == "선택 안 함":
            st.warning("악화 여부는 필수 항목입니다. 선택해주세요.")
            return False
        if st.session_state.get("pain_quality") == "선택 안 함":
            st.warning("통증 양상 항목을 선택해주세요.")
            return False
        return True

    create_navigation_buttons(prev_step=2, next_step=4, validation_func=validate_pain_profile)


def render_step_4_pain_classification():
    st.title("현재 증상 (통증 분류 및 검사)")
    st.markdown("---")

    pain_type_options = [
        "선택 안 함",
        "넓은 부위의 통증",
        "근육 통증",
        "턱관절 통증",
        "두통",
    ]
    yes_no_options = ["예", "아니오", "선택 안 함"]

    # 기본값 초기화
    keys_to_init = [
        "pain_types_value",
        "muscle_movement_pain_value",
        "muscle_pressure_2s_value",
        "muscle_referred_pain_value",
        "muscle_referred_remote_pain_value",
        "tmj_movement_pain_value",
        "tmj_press_pain_value",
        "headache_temples_value",
        "headache_with_jaw_value",
        "headache_reproduce_by_pressure_value",
        "headache_not_elsewhere_value",
    ]
    for k in keys_to_init:
        st.session_state.setdefault(k, "선택 안 함")

    def get_idx(k):
        return yes_no_options.index(st.session_state.get(k, "선택 안 함"))

    def update_session(src, dst_widget):
        st.session_state[src] = st.session_state[dst_widget]

    with st.container(border=True):
        st.markdown("**아래 중 해당되는 통증 유형을 선택해주세요.**")
        st.selectbox(
            "",
            pain_type_options,
            index=pain_type_options.index(st.session_state.pain_types_value),
            key="pain_types_widget_key",
            on_change=lambda: update_session(
                "pain_types_value", "pain_types_widget_key"
            ),
        )

        st.markdown("---")
        pt = st.session_state.pain_types_value

        if pt in ["넓은 부위의 통증", "근육 통증"]:
            st.markdown("#### 💬 근육/넓은 부위 관련")
            st.radio(
                "입을 벌릴 때나 턱을 움직일 때 통증이 있나요?",
                yes_no_options,
                index=get_idx("muscle_movement_pain_value"),
                key="muscle_movement_pain_widget_key",
                on_change=lambda: update_session(
                    "muscle_movement_pain_value", "muscle_movement_pain_widget_key"
                ),
            )
            st.radio(
                "근육을 2초간 눌렀을 때 통증이 느껴지나요?",
                yes_no_options,
                index=get_idx("muscle_pressure_2s_value"),
                key="muscle_pressure_2s_widget_key",
                on_change=lambda: update_session(
                    "muscle_pressure_2s_value", "muscle_pressure_2s_widget_key"
                ),
            )
            if st.session_state.muscle_pressure_2s_value == "예":
                st.radio(
                    "근육을 5초간 눌렀을 때, 통증이 눌린 부위 넘어서 퍼지나요?",
                    yes_no_options,
                    index=get_idx("muscle_referred_pain_value"),
                    key="muscle_referred_pain_widget_key",
                    on_change=lambda: update_session(
                        "muscle_referred_pain_value", "muscle_referred_pain_widget_key"
                    ),
                )
                if st.session_state.muscle_referred_pain_value == "예":
                    st.radio(
                        "통증이 눌린 부위 외 다른 곳(눈, 귀 등)까지 퍼지나요?",
                        yes_no_options,
                        index=get_idx("muscle_referred_remote_pain_value"),
                        key="muscle_referred_remote_pain_widget_key",
                        on_change=lambda: update_session(
                            "muscle_referred_remote_pain_value",
                            "muscle_referred_remote_pain_widget_key",
                        ),
                    )

        elif pt == "턱관절 통증":
            st.markdown("#### 💬 턱관절 관련")
            st.radio(
                "입을 벌릴 때나 움직일 때 통증이 있나요?",
                yes_no_options,
                index=get_idx("tmj_movement_pain_value"),
                key="tmj_movement_pain_widget_key",
                on_change=lambda: update_session(
                    "tmj_movement_pain_value", "tmj_movement_pain_widget_key"
                ),
            )
            st.radio(
                "턱관절 부위를 눌렀을 때 기존 통증이 재현되나요?",
                yes_no_options,
                index=get_idx("tmj_press_pain_value"),
                key="tmj_press_pain_widget_key",
                on_change=lambda: update_session(
                    "tmj_press_pain_value", "tmj_press_pain_widget_key"
                ),
            )

        elif pt == "두통":
            st.markdown("#### 💬 두통 관련")
            st.radio(
                "두통이 관자놀이 부위에서 발생하나요?",
                yes_no_options,
                index=get_idx("headache_temples_value"),
                key="headache_temples_widget_key",
                on_change=lambda: update_session(
                    "headache_temples_value", "headache_temples_widget_key"
                ),
            )
            st.radio(
                "관자놀이 근육을 눌렀을 때 기존 두통이 재현되나요?",
                yes_no_options,
                index=get_idx("headache_reproduce_by_pressure_value"),
                key="headache_reproduce_by_pressure_widget_key",
                on_change=lambda: update_session(
                    "headache_reproduce_by_pressure_value",
                    "headache_reproduce_by_pressure_widget_key",
                ),
            )
            st.radio(
                "턱을 움직일 때 두통이 심해지나요?",
                yes_no_options,
                index=get_idx("headache_with_jaw_value"),
                key="headache_with_jaw_widget_key",
                on_change=lambda: update_session(
                    "headache_with_jaw_value", "headache_with_jaw_widget_key"
                ),
            )
            if st.session_state.headache_with_jaw_value == "예":
                st.radio(
                    "해당 두통이 다른 의학적 진단으로 설명되지 않나요?",
                    yes_no_options,
                    index=get_idx("headache_not_elsewhere_value"),
                    key="headache_not_elsewhere_widget_key",
                    on_change=lambda: update_session(
                        "headache_not_elsewhere_value",
                        "headache_not_elsewhere_widget_key",
                    ),
                )

    st.markdown("---")

    def validate_pain_classification():
        errors = []
        pt = st.session_state.pain_types_value

        if pt == "선택 안 함":
            errors.append("통증 유형을 선택해주세요.")

        if pt in ["넓은 부위의 통증", "근육 통증"]:
            if st.session_state.muscle_movement_pain_value == "선택 안 함":
                errors.append("근육: 입 벌릴 때 통증 여부를 선택해주세요.")
            if st.session_state.muscle_pressure_2s_value == "선택 안 함":
                errors.append("근육: 2초간 압통 여부를 선택해주세요.")
            if st.session_state.muscle_pressure_2s_value == "예":
                if st.session_state.muscle_referred_pain_value == "선택 안 함":
                    errors.append("근육: 5초간 통증 전이 여부를 선택해주세요.")
                if (
                    st.session_state.muscle_referred_pain_value == "예"
                    and st.session_state.muscle_referred_remote_pain_value
                    == "선택 안 함"
                ):
                    errors.append("근육: 통증이 다른 부위까지 퍼지는지 여부를 선택해주세요.")

        if pt == "턱관절 통증":
            if st.session_state.tmj_movement_pain_value == "선택 안 함":
                errors.append("턱관절: 움직일 때 통증 여부를 선택해주세요.")
            if st.session_state.tmj_press_pain_value == "선택 안 함":
                errors.append("턱관절: 눌렀을 때 통증 여부를 선택해주세요.")

        if pt == "두통":
            if st.session_state.headache_temples_value == "선택 안 함":
                errors.append("두통: 관자놀이 여부를 선택해주세요.")
            if st.session_state.headache_reproduce_by_pressure_value == "선택 안 함":
                errors.append("두통: 관자놀이 압통 시 두통 재현 여부를 선택해주세요.")
            if st.session_state.headache_with_jaw_value == "선택 안 함":
                errors.append("두통: 턱 움직임 시 두통 악화 여부를 선택해주세요.")
            if (
                st.session_state.headache_with_jaw_value == "예"
                and st.session_state.headache_not_elsewhere_value == "선택 안 함"
            ):
                errors.append("두통: 다른 진단 여부를 선택해주세요.")

        if errors:
            for err in errors:
                st.warning(err)
            return False
        return True

    create_navigation_buttons(
        prev_step=3, next_step=6, validation_func=validate_pain_classification
    )


def render_step_5_tmj_sounds_locking():
    st.title("턱관절 소리 및 잠김 여부")
    st.markdown("---")

    sound_options = ["딸깍소리", "사각사각소리(크레피투스)", "없음", "선택 안 함"]
    yes_no = ["예", "아니오", "선택 안 함"]

    with st.container(border=True):
        st.markdown("**턱관절에서 소리가 나나요?**")
        st.radio(
            "",
            options=sound_options,
            index=sound_options.index(st.session_state.get("tmj_sound_value", "선택 안 함")),
            key="tmj_sound_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("tmj_sound_widget", "tmj_sound_value"),
        )

        if st.session_state.tmj_sound_value == "딸깍소리":
            st.markdown("**딸깍소리가 언제 발생하나요? (복수 선택 가능)**")
            st.multiselect(
                "",
                ["입 벌릴 때", "입 다물 때", "입 벌릴 때와 다물 때 모두", "기타"],
                default=st.session_state.get("tmj_click_context", []),
                key="tmj_click_context_widget",
                label_visibility="collapsed",
                on_change=sync_widget_key,
                args=("tmj_click_context_widget", "tmj_click_context"),
            )

        if st.session_state.tmj_sound_value == "사각사각소리(크레피투스)":
            st.markdown("**사각사각소리가 확실한가요?**")
            st.radio(
                "",
                yes_no,
                index=yes_no.index(st.session_state.get("crepitus_confirmed_value", "선택 안 함")),
                key="crepitus_confirmed_widget",
                label_visibility="collapsed",
                on_change=sync_widget_key,
                args=("crepitus_confirmed_widget", "crepitus_confirmed_value"),
            )

        if st.session_state.crepitus_confirmed_value == "아니오":
            st.markdown("---")
            st.markdown("**현재 턱이 잠겨 있나요?**")
            st.radio(
                "",
                yes_no,
                index=yes_no.index(st.session_state.get("jaw_locked_now_value", "선택 안 함")),
                key="jaw_locked_now_widget",
                label_visibility="collapsed",
                on_change=sync_widget_key,
                args=("jaw_locked_now_widget", "jaw_locked_now_value"),
            )

            if st.session_state.jaw_locked_now_value == "예":
                st.markdown("**손으로 조작해서 턱 잠김을 풀 수 있나요?**")
                st.radio(
                    "",
                    yes_no,
                    index=yes_no.index(st.session_state.get("jaw_unlock_possible_value", "선택 안 함")),
                    key="jaw_unlock_possible_widget",
                    label_visibility="collapsed",
                    on_change=sync_widget_key,
                    args=("jaw_unlock_possible_widget", "jaw_unlock_possible_value"),
                )

            if st.session_state.jaw_locked_now_value == "아니오":
                st.markdown("**과거에 턱이 잠긴 경험이 있나요?**")
                st.radio(
                    "",
                    yes_no,
                    index=yes_no.index(st.session_state.get("jaw_locked_past_value", "선택 안 함")),
                    key="jaw_locked_past_widget",
                    label_visibility="collapsed",
                    on_change=sync_widget_key,
                    args=("jaw_locked_past_widget", "jaw_locked_past_value"),
                )

                if st.session_state.jaw_locked_past_value == "예":
                    st.markdown("**MAO 검사 시 손가락 3개가 들어가나요?**")
                    st.radio(
                        "",
                        yes_no,
                        index=yes_no.index(st.session_state.get("mao_fits_3fingers_value", "선택 안 함")),
                        key="mao_fits_3fingers_widget",
                        label_visibility="collapsed",
                        on_change=sync_widget_key,
                        args=("mao_fits_3fingers_widget", "mao_fits_3fingers_value"),
                    )

    st.markdown("---")

    def validate_tmj():
        errors = []
        sound = st.session_state.get("tmj_sound_value", "선택 안 함")

        if sound == "선택 안 함":
            errors.append("턱관절 소리 여부를 선택해주세요.")
        if sound == "딸깍소리" and not st.session_state.get("tmj_click_context"):
            errors.append("딸깍소리가 언제 나는지 최소 1개 이상 선택해주세요.")
        if sound == "사각사각소리(크레피투스)" and st.session_state.get("crepitus_confirmed_value") == "선택 안 함":
            errors.append("사각사각소리가 확실한지 여부를 선택해주세요.")

        if st.session_state.get("crepitus_confirmed_value") == "아니오":
            if st.session_state.get("jaw_locked_now_value") == "선택 안 함":
                errors.append("현재 턱 잠김 여부를 선택해주세요.")
            if st.session_state.get("jaw_locked_now_value") == "예" and st.session_state.get("jaw_unlock_possible_value") == "선택 안 함":
                errors.append("턱 잠김이 조작으로 풀리는지 여부를 선택해주세요.")
            if st.session_state.get("jaw_locked_now_value") == "아니오":
                if st.session_state.get("jaw_locked_past_value") == "선택 안 함":
                    errors.append("과거 턱 잠김 경험 여부를 선택해주세요.")
                if st.session_state.get("jaw_locked_past_value") == "예" and st.session_state.get("mao_fits_3fingers_value") == "선택 안 함":
                    errors.append("MAO 시 손가락 3개가 들어가는지 여부를 선택해주세요.")

        if errors:
            for e in errors:
                st.warning(e)
            return False
        return True

    create_navigation_buttons(prev_step=4, next_step=6, validation_func=validate_tmj)


def render_step_6_frequency_timing():
    st.title("증상 빈도 및 시간대")
    st.markdown("---")

    with st.container(border=True):
        st.markdown("**증상이 얼마나 자주 발생하나요?**")
        freq_opts = ["매일", "주 3~4회", "주 1~2회", "월 1~2회", "거의 없음", "선택 안 함"]
        st.radio(
            "",
            freq_opts,
            index=freq_opts.index(st.session_state.get("frequency_choice", "선택 안 함")),
            key="frequency_choice_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("frequency_choice_widget", "frequency_choice"),
        )

        st.markdown("---")
        st.markdown("**어느 시간대에 증상이 가장 심한가요? (복수 선택 가능)**")
        for t in ["아침", "오후", "저녁"]:
            st.checkbox(
                t,
                key=f"time_{t}",
                value=st.session_state.get(f"time_{t}", False),
            )

    st.markdown("---")
    st.markdown("**현재 두통이 있나요?**")
    yes_no = ["예", "아니오", "선택 안 함"]
    st.radio(
        "",
        yes_no,
        index=yes_no.index(st.session_state.get("has_headache_now", "선택 안 함")),
        key="has_headache_widget",
        label_visibility="collapsed",
        on_change=sync_widget_key,
        args=("has_headache_widget", "has_headache_now"),
    )

    if st.session_state.get("has_headache_now") == "예":
        st.markdown("---")
        st.markdown("**두통 부위 선택 (복수 선택 가능)**")
        ha_opts = ["관자놀이", "이마", "뒤통수", "측두부", "기타"]
        st.multiselect(
            "",
            ha_opts,
            default=st.session_state.get("headache_areas", []),
            key="headache_areas_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("headache_areas_widget", "headache_areas"),
        )

        st.markdown("**두통 빈도**")
        hf_opts = ["매일", "주 3~4회", "주 1~2회", "월 1~2회", "거의 없음", "선택 안 함"]
        st.radio(
            "",
            hf_opts,
            index=hf_opts.index(st.session_state.get("headache_frequency", "선택 안 함")),
            key="headache_frequency_widget",
            label_visibility="collapsed",
            on_change=update_headache_frequency,
        )

        st.markdown("**두통 강도 (0: 없음 ~ 10: 매우 심함)**")
        st.slider(
            "",
            min_value=0,
            max_value=10,
            value=st.session_state.get("headache_severity", 0),
            key="headache_severity_widget",
            label_visibility="collapsed",
            on_change=sync_widget_key,
            args=("headache_severity_widget", "headache_severity"),
        )
    else:
        reset_headache_details()

    st.markdown("---")

    def validate_frequency_timing():
        errors = []
        if st.session_state.get("frequency_choice") == "선택 안 함":
            errors.append("증상 빈도를 선택해주세요.")
        if not any(st.session_state.get(f"time_{t}", False) for t in ["아침", "오후", "저녁"]):
            errors.append("증상이 발생하는 시간대를 최소 1개 이상 선택해주세요.")
        if st.session_state.get("has_headache_now") == "예":
            if not st.session_state.get("headache_areas"):
                errors.append("두통 부위를 최소 1개 이상 선택해주세요.")
            if st.session_state.get("headache_frequency", "선택 안 함") == "선택 안 함":
                errors.append("두통 빈도를 선택해주세요.")
            if st.session_state.get("headache_severity", 0) == 0:
                errors.append("두통 강도를 선택해주세요.")
        if errors:
            for e in errors:
                st.warning(e)
            return False
        return True

    create_navigation_buttons(
        prev_step=5, next_step=7, validation_func=validate_frequency_timing
    )
