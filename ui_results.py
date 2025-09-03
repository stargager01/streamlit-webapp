 # ui_results.py

import streamlit as st
from diagnosis import compute_diagnoses

def render_step_19_results():
    st.title("📊 예비 진단 결과 요약")
    st.markdown("---")

    # 진단 결과 생성
    results = compute_diagnoses(st.session_state)
    st.session_state["diagnosis_result"] = ", ".join(results) if results else "진단 없음"

    # 각 진단에 대한 설명 맵
    dc_tmd_explanations = {
        "근육통 (Myalgia)": "근육 주변에서 발생하는 통증으로, 턱을 움직이거나 압박 시 통증이 심해집니다.",
        "국소 근육통 (Local Myalgia)": "특정 근육 부위에만 국한된 통증으로, 다른 부위로는 전이되지 않습니다.",
        "방사통 근육통 (Myofascial Pain with Referral)": "특정 근육을 누를 때 통증이 다른 부위로 퍼지는 증상입니다.",
        "관절통 (Arthralgia)": "턱관절 자체에서 발생하는 통증으로, 움직이거나 누를 때 악화됩니다.",
        "퇴행성 관절 질환 (Degenerative Joint Disease)": "관절 연골이나 뼈가 마모·손상되어 통증과 기능 제한이 동반됩니다.",
        "비정복성 관절원판 변위 (Disc Displacement without Reduction)": "턱관절 원판이 제자리로 복귀되지 않아 입 벌림이 제한됩니다."
    }

    # 요약 결과 표시
    st.subheader("❗ 진단 결과")
    st.write(st.session_state["diagnosis_result"])
    st.markdown("---")

    # 상세 설명
    for diag in results:
        explanation = dc_tmd_explanations.get(diag)
        if explanation:
            st.markdown(f"**{diag}**: {explanation}")

    st.markdown("---")

    # 다시 시작 / 보고서 생성 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 시작하기"):
            st.session_state.clear()
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("📄 보고서 생성하기"):
            st.session_state.report_ready = True
            st.success("보고서 생성이 완료되었습니다. 다운로드 버튼을 통해 확인해주세요.")

    st.markdown("---")
    st.caption(
        "※ 본 결과는 예비 진단입니다. 정확한 진단 및 치료는 전문 의료진과의 상담을 통해 이루어져야 합니다."
    )
