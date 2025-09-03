 # app.py

import datetime
import streamlit as st

# 각 단계별 UI 모듈에서 render 함수 가져오기
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

from pdf_generator import generate_filled_pdf


# ---------------------------
# 전체 단계 설정
# ---------------------------
total_steps = 20
final_step = total_steps - 1

# 진단 로직에 쓰일 키 기본값
diagnosis_keys = {
    "muscle_pressure_2s_value": "선택 안 함",
    "muscle_referred_pain_value": "선택 안 함",
    "muscle_referred_remote_pain_value": "선택 안 함",
    "tmj_press_pain_value": "선택 안 함",
    "headache_temples_value": "선택 안 함",
    "headache_with_jaw_value": "선택 안 함",
    "headache_reproduce_by_pressure_value": "선택 안 함",
    "headache_not_elsewhere_value": "선택 안 함",
    "crepitus_confirmed_value": "선택 안 함",
    "mao_fits_3fingers_value": "선택 안 함",
    "jaw_locked_now_value": "선택 안 함",
    "tmj_sound_value": "선택 안 함",
}

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "validation_errors" not in st.session_state:
    st.session_state.validation_errors = {}

for key, default in diagnosis_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------
# 페이지 네비게이션
# ---------------------------
if st.session_state.step == 0:
    render_step_0_welcome()

elif st.session_state.step == 1:
    render_step_1_patient_info()

elif st.session_state.step == 2:
    render_step_2_chief_complaint()

elif st.session_state.step == 3:
    render_step_3_pain_profile()

elif st.session_state.step == 4:
    render_step_4_pain_classification()

elif st.session_state.step == 5:
    render_step_5_tmj_sounds_locking()

elif st.session_state.step == 6:
    render_step_6_frequency_timing()

elif st.session_state.step == 7:
    render_step_7_habits()

elif st.session_state.step == 8:
    render_step_8_rom_observations_1()

elif st.session_state.step == 9:
    render_step_9_rom_observations_2()

elif st.session_state.step == 10:
    render_step_10_rom_observations_3()

elif st.session_state.step == 11:
    render_step_11_palpation()

elif st.session_state.step == 12:
    render_step_12_ear_symptoms()

elif st.session_state.step == 13:
    render_step_13_neck_shoulder()

elif st.session_state.step == 14:
    render_step_14_stress_history()

elif st.session_state.step == 15:
    render_step_15_past_dental_history()

elif st.session_state.step == 16:
    render_step_16_past_medical_history()

elif st.session_state.step == 17:
    render_step_17_provocation_tests()

elif st.session_state.step == 18:
    render_step_18_functional_impact()

elif st.session_state.step == 19:
    render_step_19_results()

# ---------------------------
# 최종 단계에서 PDF 다운로드 버튼
# ---------------------------
if st.session_state.step == final_step:
    st.download_button(
        label="📄 진단 결과 PDF 다운로드",
        data=generate_filled_pdf(),
        file_name=f"TMJ_진단_결과_{datetime.date.today()}.pdf",
        mime="application/pdf",
    )
