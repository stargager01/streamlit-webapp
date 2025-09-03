# pdf_generator.py

import os
import fitz  # PyMuPDF
import streamlit as st
import textwrap
from io import BytesIO

# 📁 현재 스크립트 경로 기준 폰트 파일 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(script_dir, "NanumGothic.ttf")

def generate_filled_pdf():
    """세션 상태 데이터를 기반으로 PDF 템플릿을 채워 반환합니다."""
    template_path = "template5.pdf"
    doc = fitz.open(template_path)

    # ✅ 리스트/딕셔너리 형태의 값들을 문자열로 변환
    def convert_list_to_string(key):
        val = st.session_state.get(key, [])
        if isinstance(val, list):
            st.session_state[key] = ", ".join(val)

    def convert_dict_to_string(key):
        val = st.session_state.get(key, {})
        if isinstance(val, dict):
            selected = [k for k, v in val.items() if v]
            st.session_state[key] = ", ".join(selected) if selected else "없음"

    convert_dict_to_string("neck_shoulder_symptoms")
    convert_dict_to_string("additional_symptoms")
    for k in ["headache_areas", "headache_triggers", "headache_reliefs", "headache_frequency", "selected_ear_symptoms"]:
        convert_list_to_string(k)

    # ✅ PDF에 삽입할 키 목록
    keys = [
        "name", "birthdate", "gender", "email", "address", "phone", "occupation", "visit_reason",
        "chief_complaint", "chief_complaint_other", "onset", "jaw_aggravation", "pain_quality", "pain_quality_other",
        "muscle_movement_pain_value", "muscle_pressure_2s_value", "muscle_referred_pain_value", "muscle_referred_remote_pain_value",
        "tmj_movement_pain_value", "tmj_press_pain_value", "headache_temples_value", "headache_reproduce_by_pressure_value",
        "headache_with_jaw_value", "headache_not_elsewhere_value", "tmj_sound_value", "tmj_click_summary",
        "crepitus_confirmed_value", "jaw_locked_now_value", "jaw_unlock_possible_value", "jaw_locked_past_value",
        "mao_fits_3fingers_value", "frequency_choice", "pain_level", "selected_times", "has_headache_now",
        "headache_areas", "headache_severity", "headache_frequency", "headache_triggers", "headache_reliefs",
        "habit_summary", "additional_habits", "active_opening", "active_pain", "passive_opening", "passive_pain",
        "deviation", "deviation2", "deflection", "protrusion", "protrusion_pain", "latero_right", "latero_right_pain",
        "latero_left", "latero_left_pain", "occlusion", "occlusion_shift", "tmj_noise_right_open", "tmj_noise_left_open",
        "tmj_noise_right_close", "tmj_noise_left_close", "palpation_temporalis", "palpation_medial_pterygoid",
        "palpation_lateral_pterygoid", "pain_mapping", "selected_ear_symptoms", "neck_shoulder_symptoms",
        "additional_symptoms", "neck_trauma_radio", "stress_radio", "stress_detail", "ortho_exp", "ortho_detail",
        "prosth_exp", "prosth_detail", "other_dental", "tmd_treatment_history", "tmd_treatment_detail",
        "tmd_treatment_response", "tmd_current_medications", "past_history", "current_medications",
        "bite_right", "bite_left", "loading_test", "resistance_test", "attrition", "impact_daily",
        "impact_work", "impact_quality_of_life", "sleep_quality", "sleep_tmd_relation", "diagnosis_result"
    ]

    # ✅ 세션 상태에서 값 추출 및 전처리
    values = {k: str(st.session_state.get(k, "")) for k in keys}
    values = {k: ("" if v == "선택 안 함" else v) for k, v in values.items()}

    # ✅ 긴 텍스트 줄바꿈 처리
    for long_key in ["additional_habits", "past_history", "current_medications"]:
        if long_key in values:
            values[long_key] = "\n".join(textwrap.wrap(values[long_key], width=70))

    # ✅ 템플릿 내 플레이스홀더 검색 및 텍스트 삽입
    for page in doc:
        placeholders_to_insert = {}
        for key, val in values.items():
            placeholder = f"{{{key}}}"
            rects = page.search_for(placeholder)
            if rects:
                placeholders_to_insert[key] = {'value': val, 'rects': rects}
                for rect in rects:
                    page.add_redact_annot(rect)
        page.apply_redactions()

        for key, data in placeholders_to_insert.items():
            val = data['value']
            rects = data['rects']
            for rect in rects:
                x, y = rect.tl
                for i, line in enumerate(val.split("\n")):
                    page.insert_text((x, y + 8 + i * 12), line, fontname="nan", fontfile=FONT_FILE, fontsize=10)

    # ✅ PDF 버퍼 반환
    pdf_buffer = BytesIO()
    doc.save(pdf_buffer)
    doc.close()
    pdf_buffer.seek(0)
    return pdf_buffer
