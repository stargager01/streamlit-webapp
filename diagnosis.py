# diagnosis.py

from typing import List, Dict

def compute_diagnoses(state: Dict[str, str]) -> List[str]:
    """사용자 상태를 기반으로 진단 결과 리스트를 반환합니다."""
    diagnoses = []

    def is_yes(val: str) -> bool:
        return val == "예"

    def is_no(val: str) -> bool:
        return val == "아니오"

    # 1. 국소 근육통 (Local Myalgia)
    if (
        is_yes(state.get("muscle_pressure_2s_value")) and
        is_yes(state.get("muscle_referred_pain_value")) and
        is_no(state.get("muscle_referred_remote_pain_value"))
    ):
        diagnoses.append("국소 근육통 (Local Myalgia)")

    # 2. 방사성 근막통 (Myofascial Pain with Referral)
    if (
        is_yes(state.get("muscle_pressure_2s_value")) and
        is_yes(state.get("muscle_referred_pain_value")) and
        is_yes(state.get("muscle_referred_remote_pain_value"))
    ):
        diagnoses.append("방사성 근막통 (Myofascial Pain with Referral)")

    # 3. 근육통 (Myalgia) — 국소/방사성이 없을 때만
    if (
        "국소 근육통 (Local Myalgia)" not in diagnoses and
        "방사성 근막통 (Myofascial Pain with Referral)" not in diagnoses
    ):
        if is_no(state.get("muscle_pressure_2s_value")):
            diagnoses.append("근육통 (Myalgia)")
        elif (
            is_yes(state.get("muscle_pressure_2s_value")) and
            is_no(state.get("muscle_referred_pain_value"))
        ):
            diagnoses.append("근육통 (Myalgia)")

    # 4. 관절통 (Arthralgia)
    if is_yes(state.get("tmj_press_pain_value")):
        diagnoses.append("관절통 (Arthralgia)")

    # 5. TMD에 기인한 두통
    if (
        state.get("headache_with_jaw_value") == "예" and
        all(is_yes(state.get(k)) for k in [
            "headache_temples_value",
            "headache_reproduce_by_pressure_value",
            "headache_not_elsewhere_value",
            "headache_with_jaw_value"
        ])
    ) or (
        state.get("headache_with_jaw_value") == "아니오" and
        is_yes(state.get("headache_temples_value")) and
        is_yes(state.get("headache_reproduce_by_pressure_value"))
    ):
        diagnoses.append("TMD에 기인한 두통 (Headache attributed to TMD)")

    # 6. 퇴행성 관절 질환
    if is_yes(state.get("crepitus_confirmed_value")):
        diagnoses.append("퇴행성 관절 질환 (Degenerative Joint Disease)")

    # 7. 비정복성 관절원판 변위, 개구 제한 없음
    if is_yes(state.get("mao_fits_3fingers_value")):
        diagnoses.append("비정복성 관절원판 변위, 개구 제한 없음 (Disc Displacement without Reduction)")

    # 8. 비정복성 관절원판 변위, 개구 제한 동반
    if (
        is_no(state.get("mao_fits_3fingers_value")) or
        is_no(state.get("jaw_unlock_possible_value"))
    ):
        diagnoses.append("비정복성 관절원판 변위, 개구 제한 동반 (Disc Displacement without Reduction with Limited opening)")

    # 9. 정복성 관절원판 변위, 간헐적 개구 장애 동반
    if (
        is_yes(state.get("jaw_locked_now_value")) and
        is_yes(state.get("jaw_unlock_possible_value"))
    ):
        diagnoses.append("정복성 관절원판 변위, 간헐적 개구 장애 동반 (Disc Displacement with reduction, with intermittent locking)")

    # 10. 정복성 관절원판 변위 (딸깍 소리 있을 경우)
    if state.get("tmj_sound_value") and "딸깍" in state.get("tmj_sound_value"):
        diagnoses.append("정복성 관절원판 변위 (Disc Displacement with Reduction)")

    return diagnoses
