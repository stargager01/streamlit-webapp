import streamlit as st
import json
import datetime
from streamlit_local_storage import LocalStorage

# LocalStorage 인스턴스 생성
localS = LocalStorage()

def save_session():
    """
    현재 st.session_state의 모든 내용을 localStorage에 저장
    datetime.date 객체는 문자열로 변환하여 저장
    """
    try:
        # session_state를 딕셔너리로 변환
        session_data = dict(st.session_state)
        
        # datetime.date 객체를 문자열로 변환
        for key, value in session_data.items():
            if isinstance(value, datetime.date):
                session_data[key] = value.strftime("%Y-%m-%d")
        
        # JSON 문자열로 변환
        json_data = json.dumps(session_data, ensure_ascii=False)
        
        # localStorage에 저장
        localS.setItem('jaw_analysis_session', json_data)
        
        return True
    except Exception as e:
        st.error(f"세션 저장 중 오류가 발생했습니다: {str(e)}")
        return False

def load_session():
    """
    localStorage에서 저장된 세션 데이터를 불러와서 st.session_state 업데이트
    문자열로 저장된 날짜는 다시 datetime.date 객체로 복원
    """
    try:
        # localStorage에서 데이터 불러오기
        json_data = localS.getItem('jaw_analysis_session')
        
        if json_data is None or json_data == "null":
            return False
        
        # JSON 문자열을 딕셔너리로 변환
        session_data = json.loads(json_data)
        
        # 문자열로 저장된 날짜를 datetime.date 객체로 복원
        for key, value in session_data.items():
            if key == 'birthdate' and isinstance(value, str):
                try:
                    # "YYYY-MM-DD" 형식의 문자열을 datetime.date로 변환
                    session_data[key] = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    # 변환 실패 시 원래 값 유지
                    pass
        
        # st.session_state 업데이트 (기존 내용을 덮어쓰지 않고 업데이트)
        st.session_state.update(session_data)
        
        return True
    except Exception as e:
        st.error(f"세션 불러오기 중 오류가 발생했습니다: {str(e)}")
        return False

def delete_session():
    """
    localStorage에서 저장된 세션 데이터 삭제
    """
    try:
        localS.deleteItem('jaw_analysis_session')
        return True
    except Exception as e:
        st.error(f"세션 삭제 중 오류가 발생했습니다: {str(e)}")
        return False

def has_saved_session():
    """
    저장된 세션 데이터가 있는지 확인
    """
    try:
        json_data = localS.getItem('jaw_analysis_session')
        return json_data is not None and json_data != "null"
    except:
        return False