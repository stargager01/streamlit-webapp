# utils.py

import streamlit as st

# 🔄 단계 이동 함수
def go_next():
    """다음 단계로 이동하며 에러 상태 초기화"""
    st.session_state.step += 1
    st.session_state.validation_errors = {}

def go_back():
    """이전 단계로 이동하며 에러 상태 초기화"""
    st.session_state.step -= 1
    st.session_state.validation_errors = {}

# 🔁 위젯 → 세션 상태 동기화
def sync_widget_key(widget_key, target_key):
    """특정 위젯 값을 세션 상태에 복사"""
    if widget_key in st.session_state:
        st.session_state[target_key] = st.session_state[widget_key]

def sync_multiple_keys(field_mapping):
    """여러 위젯 값을 세션 상태에 일괄 복사"""
    for widget_key, session_key in field_mapping.items():
        st.session_state[session_key] = st.session_state.get(widget_key, "")

def sync_widget_to_session(widget_key, session_key):
    """Streamlit 위젯의 현재 값을 세션 상태에 동기화하는 콜백 함수"""
    if widget_key in st.session_state:
        st.session_state[session_key] = st.session_state[widget_key]

# 📻 라디오 버튼/텍스트 입력 상태 업데이트
def update_radio_state(key):
    """라디오 버튼 선택값을 세션 상태에 반영"""
    st.session_state[key] = st.session_state.get(key)

def update_text_state(key):
    """텍스트 입력값을 세션 상태에 반영"""
    st.session_state[key] = st.session_state.get(key, "")

# 🧠 두통 관련 상태 초기화
def reset_headache_details():
    """두통이 '예'가 아닐 경우 관련 세션 키 초기화"""
    if st.session_state.get("has_headache_widget") != "예":
        keys_to_reset = [
            "headache_areas",
            "headache_severity",
            "headache_frequency",
            "headache_triggers",
            "headache_reliefs"
        ]
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]

# 🧍‍♀️ 목/어깨 증상 관련 로직
def update_neck_none():
    """'없음' 체크 시 다른 증상 해제"""
    if st.session_state.get('neck_none'):
        st.session_state['neck_pain'] = False
        st.session_state['shoulder_pain'] = False
        st.session_state['stiffness'] = False

def update_neck_symptom(key):
    """개별 증상 체크 시 '없음' 해제"""
    if st.session_state.get(key):
        st.session_state['neck_none'] = False

# utils.py 파일 맨 아래에 추가해주세요.

def update_headache_frequency():
    """두통 빈도 위젯 값을 세션 상태에 동기화"""
    if "headache_frequency_widget" in st.session_state:
        st.session_state["headache_frequency"] = st.session_state["headache_frequency_widget"]

