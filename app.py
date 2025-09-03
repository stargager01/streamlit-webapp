# app.py

import streamlit as st

# 새로 분리된 UI 모듈에서 각 단계 렌더 함수를 가져옵니다.
from ui_patient_info import (
    render_step_0_welcome,
    render_step_1_patient_info,
    render_step_2_chief_complaint,
)
from ui_symptom_profile import (
    render_step_3_pain_profile,
    render_step_4_pain_classification,
    render_step_5_tmj_sounds_locking,
    render_step_6_frequency_timing,
)
from ui_clinical_exam import (
    render_step_7_habits,
    render_step_8_rom_observations_1,
    render_step_9_rom_observations_2,
    render_step_10_rom_observations_3,
    render_step_11_palpation,
)
from ui_history_impact import (
    render_step_12_ear_symptoms,
    render_step_13_neck_shoulder,
    render_step_14_stress_history,
    render_step_15_past_dental_history,
    render_step_16_past_medical_history,
    render_step_17_provocation_tests,
    render_step_18_functional_impact,
)
from ui_results import render_step_19_results


# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "validation_errors" not in st.session_state:
    st.session_state.validation_errors = {}

# --- 페이지 흐름 제어 ---
step = st.session_state.step

if step == 0:
    render_step_0_welcome()
elif step == 1:
    render_step_1_patient_info()
elif step == 2:
    render_step_2_chief_complaint()
elif step == 3:
    render_step_3_pain_profile()
elif step == 4:
    render_step_4_pain_classification()
elif step == 5:
    render_step_5_tmj_sounds_locking()
elif step == 6:
    render_step_6_frequency_timing()
elif step == 7:
    render_step_7_habits()
elif step == 8:
    render_step_8_rom_observations_1()
elif step == 9:
    render_step_9_rom_observations_2()
elif step == 10:
    render_step_10_rom_observations_3()
elif step == 11:
    render_step_11_palpation()
elif step == 12:
    render_step_12_ear_symptoms()
elif step == 13:
    render_step_13_neck_shoulder()
elif step == 14:
    render_step_14_stress_history()
elif step == 15:
    render_step_15_past_dental_history()
elif step == 16:
    render_step_16_past_medical_history()
elif step == 17:
    render_step_17_provocation_tests()
elif step == 18:
    render_step_18_functional_impact()
elif step == 19:
    render_step_19_results()
else:
    # 범위를 벗어난 경우 초기 화면으로
    st.session_state.step = 0
    render_step_0_welcome()
