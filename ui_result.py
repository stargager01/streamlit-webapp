# ui_results.py

import streamlit as st
from diagnosis import compute_diagnoses

# ---------------------------
# STEP 19: 결과
# ---------------------------
def render_step_19_results():
    st.title("📊 턱관절 질환 예비 진단 결과")
    st.markdown("---")

    results = compute_diagnoses(st.session_state)
    st.session_state["diagnosis_result"] = ", ".join(results) if results else "진단 없음"

    dc_tmd_explanations = {
        "근육통 (Myalgia)": "턱 주변 근육에서 발생하는 통증으로, 움직임이나 압박 시 통증이 심해지는 증상입니다.",
        "국소 근육통 (Local Myalgia)": "통증이 특정 근육 부위에만 국한되어 있고, 다른 부위로 퍼지지 않는 증상입니다.",
        "방사성 근막통 (Myofascial Pain with Referral)": "특정 근육을 눌렀을 때 통증이 다른 부위로 방사되어 퍼지는 증상입니다.",
        "관절통 (Arthralgia)": "턱관절 자체에 발생하는 통증으로, 움직이거나 누를 때 통증이 유발되는 상태입니다.",
        "퇴행성 관절 질환 (Degenerative Joint Disease)": "턱관절의 연골이나 뼈가 마모되거나 손상되어 통증과 기능 제한이 동반되는 상태입니다.",
        "비정복성 관절원판 변위, 개구 제한 없음 (Disc Displacement without Reduction)": "턱관절 디스크가 비정상 위치에 있으며, 입을 벌려도 제자리로 돌아오지 않는 상태입니다.",
        "비정복성 관절원판 변위, 개구 제한 동반 (Disc Displacement without Reduction with Limited opening)": "디스크가 제자리로 돌아오지 않으며, 입 벌리기가 제한되는 상태입니다.",
        "정복성 관절원판 변위, 간헐적 개구 장애 동반 (Disc Displacement with reduction, with intermittent locking)": "디스크가 움직일 때 딸깍소리가 나며, 일시적인 입 벌리기 장애가 간헐적으로 나타나는 상태입니다.",
        "정복성 관절원판 변위 (Disc Displacement with Reduction)": "입을 벌릴 때 디스크가 제자리로 돌아오며 딸깍소리가 나는 상태이며, 기능 제한은 없는 경우입니다.",
        "TMD에 기인한 두통 (Headache attributed to TMD)": "턱관절 또는 턱 주변 근육 문제로 인해 발생하는 두통으로, 턱을 움직이거나 근육을 누르면 증상이 악화되는 경우입니다.",
    }

    if not results:
        st.success("✅ DC/TMD 기준상 명확한 진단 근거는 확인되지 않았습니다.\n\n다른 질환 가능성에 대한 조사가 필요합니다.")
    else:
        st.session_state["diagnosis_result"] = ", ".join(results)
        if len(results) == 1:
            st.error(f"**{results[0]}**이(가) 의심됩니다.")
        else:
            st.error(f"**{', '.join(results)}**이(가) 의심됩니다.")
        st.markdown("---")
        for diagnosis in results:
            st.markdown(f"### 🔹 {diagnosis}")
            st.info(dc_tmd_explanations.get(diagnosis, "설명 없음"))
            st.markdown("---")

    st.info("※ 본 결과는 예비 진단이며, 전문의 상담을 반드시 권장합니다.")
    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.step = 0
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
