# jaw_analyzer/__init__.py 파일

import os
import streamlit.components.v1 as components

# 프론트엔드 코드의 위치를 지정합니다.
_RELEASE = True
parent_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(parent_dir, "frontend")

# index.html 파일의 위치를 알려주며 컴포넌트를 선언합니다.
_component_func = components.declare_component(
    "jaw_analyzer_component",
    path=frontend_dir
)

# 컴포넌트를 호출할 파이썬 함수를 만듭니다.
def jaw_analyzer_component(key=None):
    """
    jaw_analyzer_component의 새 인스턴스를 생성합니다.
    이 함수는 자바스크립트에서 파이썬으로 데이터를 전송합니다.
    """
    component_value = _component_func(key=key, default=None)
    return component_value