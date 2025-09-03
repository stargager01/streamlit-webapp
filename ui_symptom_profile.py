 # ui_symptom_profile.py

import streamlit as st
from utils import (
    sync_widget_key,
    sync_multiple_keys,
    reset_headache_details,
    update_headache_frequency,
    create_navigation_buttons,
)

def render_step_3_pain_profile():
    st.title("현재 증상 (통증 양상)")
    st.markdown("---")

    field_mapping = {
        "jaw_aggravation_widget": "jaw_aggravation",
        "pain_quality_widget": "pain_quality",
        "pain_quality_other_widget": "pain_quality_other"
    }

    with st.container(border=True):
        st.markdown("**턱을 움직이거나 씹기, 말하기 등의 기능 또는 악습관(이갈이, 턱 괴기 등)으로 인해 통증이 악화되나요?**")
        st.radio(
            label="악화 여부",
            options=["예", "아니오", "선택 안 함"],
            key="jaw_aggravation_widget",
            index=2,
            label_visibility="collapsed",
            on_change=sync_widget_key, args=("jaw_aggravation_widget", "jaw_aggravation")
        )

        st.markdown("---")
        st.markdown("**통증을 어떻게 표현하시겠습니까? (예: 둔함, 날카로움, 욱신거림 등)**")
        st.radio(
            label="통증 양상",
            options=["둔함", "날카로움", "욱신거림", "간헐적", "선택 안 함"],
            key="pain_quality_widget",
            index=4,
            label_visibility="collapsed",
            on_change=sync_widget_key, args=("pain_quality_widget", "pain_quality")
        )

    st.markdown("---")

    def _validate():
        sync_multiple_keys(field_mapping)
        if st.session_state.get("jaw_aggravation") == "선택 안 함":
            return False, ["악화 여부는 필수 항목입니다. 선택해주세요."]
        if st.session_state.get("pain_quality") == "선택 안 함":
            return False, ["통증 양상 항목을 선택해주세요."]
        return True

    create_navigation_buttons(prev_step=2, next_step=4, validation_func=_validate)


def render_step_4_pain_classification():
    st.title("현재 증상 (통증 분류 및 검사)")
    st.markdown("---")

    pain_type_options = ["선택 안 함", "넓은 부위의 통증", "근육 통증", "턱관절 통증", "두통"]
    yes_no_options = ["예", "아니오", "선택 안 함"]

    for key in [
        "pain_types_value", "muscle_movement_pain_value", "muscle_pressure_2s_value",
        "muscle_referred_pain_value", "muscle_referred_remote_pain_value",
        "tmj_movement_pain_value", "tmj_press_pain_value",
        "headache_temples_value", "headache_with_jaw_value",
        "headache_reproduce_by_pressure_value", "headache_not_elsewhere_value"
    ]:
        st.session_state.setdefault(key, "선택 안 함")

    def get_radio_index(key, options=yes_no_options):
        return options.index(st.session_state.get(key, "선택 안 함"))

    def update_session(key, widget_key):
        st.session_state[key] = st.session_state[widget_key]

    with st.container(border=True):
        st.markdown("**아래 중 해당되는 통증 유형을 선택해주세요.**")
        st.selectbox(
            "",
            pain_type_options,
            index=pain_type_options.index(st.session_state.pain_types_value),
            key="pain_types_widget_key",
            on_change=lambda: update_session("pain_types_value", "pain_types_widget_key")
        )

        st.markdown("---")
        pain_type = st.session_state.pain_types_value

        if pain_type in ["넓은 부위의 통증", "근육 통증"]:
            st.markdown("#### 💬 근육/넓은 부위 관련")
            st.markdown("**입을 벌릴 때나 턱을 움직일 때 통증이 있나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("muscle_movement_pain_value"),
                key="muscle_movement_pain_widget_key",
                on_change=lambda: update_session("muscle_movement_pain_value", "muscle_movement_pain_widget_key")
            )

            st.markdown("**근육을 2초간 눌렀을 때 통증이 느껴지나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("muscle_pressure_2s_value"),
                key="muscle_pressure_2s_widget_key",
                on_change=lambda: update_session("muscle_pressure_2s_value", "muscle_pressure_2s_widget_key")
            )

            if st.session_state.muscle_pressure_2s_value == "예":
                st.markdown("**근육을 5초간 눌렀을 때, 통증이 눌린 부위 넘어서 퍼지나요?**")
                st.radio(
                    "", yes_no_options, index=get_radio_index("muscle_referred_pain_value"),
                    key="muscle_referred_pain_widget_key",
                    on_change=lambda: update_session("muscle_referred_pain_value", "muscle_referred_pain_widget_key")
                )

                if st.session_state.muscle_referred_pain_value == "예":
                    st.markdown("**통증이 눌린 부위 외 다른 곳(눈, 귀 등)까지 퍼지나요?**")
                    st.radio(
                        "", yes_no_options, index=get_radio_index("muscle_referred_remote_pain_value"),
                        key="muscle_referred_remote_pain_widget_key",
                        on_change=lambda: update_session("muscle_referred_remote_pain_value", "muscle_referred_remote_pain_widget_key")
                    )
                else:
                    st.session_state.muscle_referred_remote_pain_value = "선택 안 함"
            else:
                st.session_state.muscle_referred_pain_value = "선택 안 함"
                st.session_state.muscle_referred_remote_pain_value = "선택 안 함"

        elif pain_type == "턱관절 통증":
            st.markdown("#### 💬 턱관절 관련")
            st.markdown("**입을 벌릴 때나 움직일 때 통증이 있나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("tmj_movement_pain_value"),
                key="tmj_movement_pain_widget_key",
                on_change=lambda: update_session("tmj_movement_pain_value", "tmj_movement_pain_widget_key")
            )

            st.markdown("**턱관절 부위를 눌렀을 때 기존 통증이 재현되나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("tmj_press_pain_value"),
                key="tmj_press_pain_widget_key",
                on_change=lambda: update_session("tmj_press_pain_value", "tmj_press_pain_widget_key")
            )

        elif pain_type == "두통":
            st.markdown("#### 💬 두통 관련")
            st.markdown("**두통이 관자놀이 부위에서 발생하나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("headache_temples_value"),
                key="headache_temples_widget_key",
                on_change=lambda: update_session("headache_temples_value", "headache_temples_widget_key")
            )

            st.markdown("**관자놀이 근육을 눌렀을 때 기존 두통이 재현되나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("headache_reproduce_by_pressure_value"),
                key="headache_reproduce_by_pressure_widget_key",
                on_change=lambda: update_session("headache_reproduce_by_pressure_value", "headache_reproduce_by_pressure_widget_key")
            )

            st.markdown("**턱을 움직일 때 두통이 심해지나요?**")
            st.radio(
                "", yes_no_options, index=get_radio_index("headache_with_jaw_value"),
                key="headache_with_jaw_widget_key",
                on_change=lambda: update_session("headache_with_jaw_value", "headache_with_jaw_widget_key")
            )

            if st.session_state.headache_with_jaw_value == "예":
                st.markdown("**해당 두통이 다른 의학적 진단으로 설명되지 않나요?**")
                st.radio(
                    "", yes_no_options, index=get_radio_index("headache_not_elsewhere_value"),
                    key="headache_not_elsewhere_widget_key",
                    on_change=lambda: update_session("headache_not_elsewhere_value", "headache_not_elsewhere_widget_key")
                )
            else:
                st.session_state.headache_not_elsewhere_value = "선택 안 함"

    st.markdown("---")

    def _validate():
        errors = []
        pain_type = st.session_state.pain_types_value
        if pain_type == "선택 안 함":
            errors.append("통증 유형을 선택해주세요.")

        if pain_type in ["넓은 부위의 통증", "근육 통증"]:
            if st.session_state.muscle_movement_pain_value == "선택 안 함":
                errors.append("근육: 입 벌릴 때 통증 여부를 선택해주세요.")
            if st.session_state.muscle_pressure_2s_value == "선택 안 함":
                errors.append("근육: 2초간 압통 여부를 선택해주세요.")
            if st.session_state.muscle_pressure_2s_value == "예":
                if st.session_state.muscle_referred_pain_value == "선택 안 함":
                    errors.append("근육: 5초간 통증 전이 여부를 선택해주세요.")
                elif (st.session_state.muscle_referred_pain_value == "예" and
                      st.session_state.muscle_referred_remote_pain_value == "선택 안 함"):
                    errors.append("근육: 통증이 다른 부위까지 퍼지는지 여부를 선택해주세요.")

        if pain_type == "턱관절 통증":
            if st.session_state.tmj_movement_pain_value == "선택 안 함":
                errors.append("턱관절: 움직일 때 통증 여부를 선택해주세요.")
            if st.session_state.tmj_press_pain_value == "선택 안 함":
                errors.append("턱관절: 눌렀을 때 통증 여부를 선택해주세요.")

        if pain_type == "두통":
            if st.session_state.headache_temples_value == "선택 안 함":
                errors.append("두통: 관자놀이 여부를 선택해주세요.")
            if st.session_state.headache_reproduce_by_pressure_value == "선택 안 함":
                errors.append("두통: 관자놀이 압통 시 두통 재현 여부를 선택해주세요.")
            if st.session_state.headache_with_jaw_value == "선택 안 함":
                errors.append("두통: 턱 움직임 시 두통 악화 여부를 선택해주세요.")
            if (st.session_state.headache_with_jaw_value == "예" and
                    st.session_state.headache_not_elsewhere_value == "선택 안 함"):
                errors.append("두통: 다른 진단 여부를 선택해주세요.")

        return True if not errors else (False, errors)

    create_navigation_buttons(prev_step=3, next_step=6, validation_func=_validate)


def render_step_5_tmj_sounds_locking():
    st.title("현재 증상 (턱관절 소리 및 잠김 증상)")
    st.markdown("---")

    st.session_state.setdefault("tmj_sound_value", "선택 안 함")
    st.session_state.setdefault("crepitus_confirmed_value", "선택 안 함")
    st.session_state.setdefault("tmj_click_context", [])
    st.session_state.setdefault("jaw_locked_now_value", "선택 안 함")
    st.session_state.setdefault("jaw_unlock_possible_value", "선택 안 함")
    st.session_state.setdefault("jaw_locked_past_value", "선택 안 함")
    st.session_state.setdefault("mao_fits_3fingers_value", "선택 안 함")

    def get_radio_index(key_value, options):
        val = st.session_state.get(key_value, "선택 안 함")
        return options.index(val) if val in options else options.index("선택 안 함")

    def update_tmj_sound():
        st.session_state.tmj_sound_value = st.session_state.tmj_sound_widget_key

    def update_crepitus_confirmed():
        st.session_state.crepitus_confirmed_value = st.session_state.crepitus_confirmed_widget_key

    def update_jaw_locked_now():
        st.session_state.jaw_locked_now_value = st.session_state.jaw_locked_now_widget_key

    def update_jaw_unlock_possible():
        st.session_state.jaw_unlock_possible_value = st.session_state.jaw_unlock_possible_widget_key

    def update_jaw_locked_past():
        st.session_state.jaw_locked_past_value = st.session_state.jaw_locked_past_widget_key

    def update_mao_fits_3fingers():
        st.session_state.mao_fits_3fingers_value = st.session_state.mao_fits_3fingers_widget_key

    joint_sound_options = ["딸깍소리", "사각사각소리(크레피투스)", "없음", "선택 안 함"]
    st.markdown("**턱에서 나는 소리가 있나요?**")
    st.radio(
        "턱에서 나는 소리를 선택하세요.",
        options=joint_sound_options,
        key="tmj_sound_widget_key",
        index=get_radio_index("tmj_sound_value", joint_sound_options),
        on_change=update_tmj_sound
    )

    if st.session_state.tmj_sound_value == "딸깍소리":
        st.markdown("**딸깍 소리가 나는 상황을 모두 선택하세요.**")
        click_options = ["입 벌릴 때", "입 다물 때", "음식 씹을 때"]
        updated_context = []
        for option in click_options:
            key = f"click_{option}"
            is_checked = option in st.session_state.tmj_click_context
            if st.checkbox(f"- {option}", value=is_checked, key=key):
                updated_context.append(option)
        st.session_state.tmj_click_context = updated_context

    elif st.session_state.tmj_sound_value == "사각사각소리(크레피투스)":
        crepitus_options = ["예", "아니오", "선택 안 함"]
        st.radio(
            "**사각사각소리가 확실하게 느껴지나요?**",
            options=crepitus_options,
            key="crepitus_confirmed_widget_key",
            index=get_radio_index("crepitus_confirmed_value", crepitus_options),
            on_change=update_crepitus_confirmed
        )

    show_lock_questions = (
        st.session_state.tmj_sound_value == "사각사각소리(크레피투스)" and
        st.session_state.crepitus_confirmed_value == "아니오"
    )

    if show_lock_questions:
        st.markdown("---")
        st.radio(
            "**현재 턱이 걸려서 입이 잘 안 벌어지는 증상이 있나요?**",
            options=["예", "아니오", "선택 안 함"],
            key="jaw_locked_now_widget_key",
            index=get_radio_index("jaw_locked_now_value", ["예", "아니오", "선택 안 함"]),
            on_change=update_jaw_locked_now
        )

        if st.session_state.jaw_locked_now_value == "예":
            st.radio(
                "**해당 증상은 조작해야 풀리나요?**",
                options=["예", "아니오", "선택 안 함"],
                key="jaw_unlock_possible_widget_key",
                index=get_radio_index("jaw_unlock_possible_value", ["예", "아니오", "선택 안 함"]),
                on_change=update_jaw_unlock_possible
            )
        elif st.session_state.jaw_locked_now_value == "아니오":
            st.radio(
                "**과거에 턱 잠김 또는 개방성 잠김을 경험한 적이 있나요?**",
                options=["예", "아니오", "선택 안 함"],
                key="jaw_locked_past_widget_key",
                index=get_radio_index("jaw_locked_past_value", ["예", "아니오", "선택 안 함"]),
                on_change=update_jaw_locked_past
            )
            if st.session_state.jaw_locked_past_value == "예":
                st.radio(
                    "**입을 최대한 벌렸을 때 (MAO), 손가락 3개가 들어가나요?**",
                    options=["예", "아니오", "선택 안 함"],
                    key="mao_fits_3fingers_widget_key",
                    index=get_radio_index("mao_fits_3fingers_value", ["예", "아니오", "선택 안 함"]),
                    on_change=update_mao_fits_3fingers
                )
            else:
                st.session_state.mao_fits_3fingers_value = "선택 안 함"
        else:
            st.session_state.jaw_unlock_possible_value = "선택 안 함"
            st.session_state.jaw_locked_past_value = "선택 안 함"
            st.session_state.mao_fits_3fingers_value = "선택 안 함"
    else:
        st.session_state.jaw_locked_now_value = "선택 안 함"
        st.session_state.jaw_unlock_possible_value = "선택 안 함"
        st.session_state.jaw_locked_past_value = "선택 안 함"
        st.session_state.mao_fits_3fingers_value = "선택 안 함"

    if st.session_state.tmj_sound_value != "딸깍소리":
        st.session_state.tmj_click_context = []

    st.session_state.tmj_click_summary = (
        ", ".join(st.session_state.tmj_click_context)
        if st.session_state.tmj_click_context else "해당 없음"
    )

    st.markdown("---")

    def _validate():
        errors = []
        if st.session_state.tmj_sound_value == "선택 안 함":
            errors.append("턱관절 소리 여부를 선택해주세요.")
        if st.session_state.tmj_sound_value == "딸깍소리" and not st.session_state.tmj_click_context:
            errors.append("딸깍소리가 언제 나는지 최소 1개 이상 선택해주세요.")
        if (st.session_state.tmj_sound_value == "사각사각소리(크레피투스)" and
                st.session_state.crepitus_confirmed_value == "선택 안 함"):
            errors.append("사각사각소리가 확실한지 여부를 선택해주세요.")
        if show_lock_questions:
            if st.session_state.jaw_locked_now_value == "선택 안 함":
                errors.append("현재 턱 잠김 여부를 선택해주세요.")
            if (st.session_state.jaw_locked_now_value == "예" and
                    st.session_state.jaw_unlock_possible_value == "선택 안 함"):
                errors.append("현재 턱 잠김이 조작으로 풀리는지 여부를 선택해주세요.")
            if st.session_state.jaw_locked_now_value == "아니오":
                if st.session_state.jaw_locked_past_value == "선택 안 함":
                    errors.append("과거 턱 잠김 경험 여부를 선택해주세요.")
                elif (st.session_state.jaw_locked_past_value == "예" and
                      st.session_state.mao_fits_3fingers_value == "선택 안 함"):
                    errors.append("MAO 시 손가락 3개가 들어가는지 여부를 선택해주세요.")
        return True if not errors else (False, errors)

    create_navigation_buttons(prev_step=2, next_step=6, validation_func=_validate)


def render_step_6_frequency_timing():
    st.title("현재 증상 (빈도 및 시기)")
    st.markdown("---")

    widget_map = {
        "frequency_choice_widget": "frequency_choice",
        "pain_level_widget": "pain_level",
        "time_morning_widget": "time_morning",
        "time_afternoon_widget": "time_afternoon",
        "time_evening_widget": "time_evening",
        "has_headache_widget": "has_headache_now",
        "headache_frequency_widget": "headache_frequency"
    }

    time_options = [
        {"key": "morning", "label": "오전"},
        {"key": "afternoon", "label": "오후"},
        {"key": "evening", "label": "저녁"},
    ]
    with st.container(border=True):
        st.markdown("**통증 또는 다른 증상이 얼마나 자주 발생하나요?**")
        freq_opts = ["주 1~2회", "주 3~4회", "주 5~6회", "매일", "선택 안 함"]
        st.radio(
            "", freq_opts, index=4,
            key="frequency_choice_widget",
            on_change=sync_widget_key, args=("frequency_choice_widget", "frequency_choice")
        )

        st.markdown("---")
        st.markdown("**(통증이 있을 시) 현재 통증 정도는 어느 정도인가요? (0=없음, 10=극심한 통증)**")
        st.slider(
            "통증 정도 선택", 0, 10,
            value=st.session_state.get("pain_level", 0),
            key="pain_level_widget",
            on_change=sync_widget_key, args=("pain_level_widget", "pain_level")
        )

        st.markdown("---")
        st.markdown("**주로 어느 시간대에 발생하나요?**")
        time_labels = {"morning": "오전", "afternoon": "오후", "evening": "저녁"}
        for key in ["morning", "afternoon", "evening"]:
            widget_key = f"time_{key}_widget"
            state_key = f"time_{key}"
            st.checkbox(
                label=time_labels[key],
                value=st.session_state.get(state_key, False),
                key=widget_key,
                on_change=sync_widget_key, args=(widget_key, state_key)
            )

        st.markdown("---")
        st.markdown("**두통이 있나요?**")
        st.radio(
            "", ["예", "아니오", "선택 안 함"],
            index=["예", "아니오", "선택 안 함"].index(st.session_state.get("has_headache_now", "선택 안 함")),
            key="has_headache_widget",
            on_change=reset_headache_details
        )

        st.session_state["has_headache_now"] = st.session_state.get("has_headache_widget")

        if st.session_state.get("has_headache_now") == "예":
            st.markdown("---")
            st.markdown("**두통 부위를 모두 선택해주세요.**")
            headache_area_opts = ["이마", "측두부(관자놀이)", "뒤통수", "정수리"]
            selected_areas = []
            for area in headache_area_opts:
                if st.checkbox(area, value=(area in st.session_state.get("headache_areas", [])), key=f"headache_area_{area}"):
                    selected_areas.append(area)
            st.session_state["headache_areas"] = selected_areas

            st.markdown("**현재 두통 강도는 얼마나 되나요? (0=없음, 10=극심한 통증)**")
            st.session_state["headache_severity"] = st.slider(
                "두통 강도", 0, 10, value=st.session_state.get("headache_severity", 0))

            st.markdown("**두통 빈도는 얼마나 자주 발생하나요?**")
            headache_freq_opts = ["주 1~2회", "주 3~4회", "주 5~6회", "매일", "선택 안 함"]
            st.radio(
                "", headache_freq_opts,
                index=headache_freq_opts.index(st.session_state.get("headache_frequency", "선택 안 함")),
                key="headache_frequency_widget",
                on_change=update_headache_frequency
            )

            st.markdown("**두통을 유발하거나 악화시키는 요인이 있나요? (복수 선택 가능)**")
            trigger_opts = ["스트레스", "수면 부족", "음식 섭취", "소음", "밝은 빛"]
            selected_triggers = []
            for trig in trigger_opts:
                if st.checkbox(trig, value=(trig in st.session_state.get("headache_triggers", [])), key=f"trigger_{trig}"):
                    selected_triggers.append(trig)
            st.session_state["headache_triggers"] = selected_triggers

            st.markdown("**두통을 완화시키는 요인이 있나요? (복수 선택 가능)**")
            relief_opts = ["휴식", "약물", "안마", "수면"]
            selected_reliefs = []
            for rel in relief_opts:
                if st.checkbox(rel, value=(rel in st.session_state.get("headache_reliefs", [])), key=f"relief_{rel}"):
                    selected_reliefs.append(rel)
            st.session_state["headache_reliefs"] = selected_reliefs

    st.markdown("---")

    def _validate():
        sync_multiple_keys(widget_map)

        errors = []
        freq = st.session_state.get("frequency_choice", "선택 안 함")
        freq_other = st.session_state.get("frequency_other_text", "").strip()
        freq_valid = freq not in ["선택 안 함", "기타"] or (freq == "기타" and freq_other != "")

        time_valid = any([st.session_state.get(f"time_{opt['key']}", False) for opt in time_options])

        if st.session_state.get("has_headache_now") == "예":
            if not st.session_state.get("headache_areas"):
                errors.append("두통 부위를 최소 1개 이상 선택해주세요.")
            if st.session_state.get("headache_frequency") == "선택 안 함":
                errors.append("두통 빈도를 선택해주세요.")
            if st.session_state.get("headache_severity", 0) == 0:
                errors.append("두통 강도를 선택해주세요.")

        if not freq_valid:
            errors.append("빈도 항목을 입력하거나 선택해주세요.")
        if not time_valid:
            errors.append("시간대 항목을 입력하거나 선택해주세요.")

        selected_times = [opt['label'] for opt in time_options if st.session_state.get(f"time_{opt['key']}", False)]
        st.session_state["selected_times"] = ", ".join(selected_times)

        return True if not errors else (False, errors)

    create_navigation_buttons(prev_step=2, next_step=7, validation_func=_validate)
