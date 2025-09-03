# utils.py

import streamlit as st
from typing import Callable, Iterable, Tuple, Union, Optional

def create_navigation_buttons(
    prev_step: int,
    next_step: int,
    validation_func: Optional[Callable[[], Union[bool, Tuple[bool, Iterable[str]]]]] = None,
) -> None:
    """
    공통 네비게이션 버튼(이전/다음)을 렌더링하고 단계 전환을 처리합니다.

    Parameters
    ----------
    prev_step : int
        '이전 단계' 버튼 클릭 시 이동할 단계 번호.
    next_step : int
        '다음 단계로 이동' 버튼 클릭 시 이동할 단계 번호.
    validation_func : Optional[Callable[[], Union[bool, Tuple[bool, Iterable[str]]]]]
        (선택) 유효성 검사 콜백.
        - 반환값이 bool 인 경우: True 면 다음 단계로 이동, False 면 이동하지 않음.
        - 반환값이 (is_valid, messages) 튜플인 경우:
            * is_valid: bool
            * messages: Iterable[str] — 유효성 실패 시 경고로 표시할 메시지들.

    Notes
    -----
    - 이 함수는 내부에서 st.rerun() 을 호출하여 즉시 UI 를 갱신합니다.
    - validation_func 내부에서 직접 경고/오류 표시를 수행해도 됩니다.
      이 함수는 (bool, messages) 형태를 추가로 지원하여 메시지를 자동 표시할 수 있습니다.
    """
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("이전 단계"):
            st.session_state.step = prev_step
            st.rerun()

    with col_next:
        if st.button("다음 단계로 이동 👉"):
            is_valid = True
            messages = None

            if validation_func is not None:
                result = validation_func()
                if isinstance(result, tuple) and len(result) >= 1:
                    # (bool, messages) 형태 지원
                    is_valid = bool(result[0])
                    if len(result) > 1:
                        messages = result[1]
                else:
                    is_valid = bool(result)

            if is_valid:
                st.session_state.step = next_step
                st.rerun()
            else:
                # 메시지가 제공되면 경고로 출력
                if messages:
                    for msg in messages:
                        st.warning(msg)


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

