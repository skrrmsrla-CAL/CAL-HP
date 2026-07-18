import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Mechatronics", page_icon="🤖", layout="wide")

st.title("🤖 메카트로닉스 & 제어 통합 계산기")
st.markdown("모터 선정, 센서 분해능, 제어 시스템 설계용 10대 핵심 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. DC 모터 토크-속도 관계",
    "2. 볼스크류 구동 토크",
    "3. 서보 모터 관성 매칭 (Inertia Ratio)",
    "4. 엔코더 분해능 (PPR/LPR)",
    "5. 공압 실린더 추력 계산",
    "6. PID 제어 기초 (오차와 출력)",
    "7. 감쇠비와 고유진동수 관계",
    "8. 펄스 기반 이동 속도/거리",
    "9. ADC 해상도 및 분해능",
    "10. 1차 시스템 시정수(Time Constant)"
])

st.write("---")

# 1. DC 모터 토크-속도
if "DC 모터" in calc_menu:
    st.subheader("1. DC 모터 토크-속도 관계")
    V = st.number_input("입력 전압 (V)", value=24.0)
    Kv = st.number_input("모터 속도 상수 (RPM/V)", value=500.0)
    T_stall = st.number_input("정지 토크 (N·m)", value=2.0)
    speed = st.number_input("현재 속도 (RPM)", value=5000.0)
    
    # 간략 모델: T = T_stall * (1 - speed / max_speed)
    max_speed = V * Kv
    T_out = T_stall * (1 - speed / max_speed) if speed < max_speed else 0
    st.info(f"출력 토크: {max(0, T_out):.3f} N·m")

# 2. 볼스크류 구동 토크
elif "볼스크류" in calc_menu:
    st.subheader("2. 볼스크류 구동 토크 ($T = F \cdot l / (2\pi \cdot \eta)$)")
    F = st.number_input("추력 (N)", value=1000.0)
    lead = st.number_input("리드 (mm)", value=10.0)
    eta = st.number_input("효율 (%)", value=90.0) / 100
    T = (F * lead) / (2 * math.pi * 1000 * eta)
    st.info(f"필요 토크: {T:.3f} N·m")

# 3. 관성 매칭
elif "관성 매칭" in calc_menu:
    st.subheader("3. 관성 매칭비 (Inertia Ratio)")
    J_load = st.number_input("부하 관성 (kg·m²)", value=0.01)
    J_motor = st.number_input("모터 관성 (kg·m²)", value=0.001)
    st.info(f"관성비 (J_load / J_motor): {J_load/J_motor:.2f}")

# 4. 엔코더 분해능
elif "엔코더" in calc_menu:
    st.subheader("4. 엔코더 분해능 및 각도")
    ppr = st.number_input("PPR (Pulse per Revolution)", value=1024)
    st.info(f"1 펄스당 각도: {360 / (ppr * 4):.4f} 도 (4체배 시)")

# 5. 공압 실린더 추력
elif "공압" in calc_menu:
    st.subheader("5. 공압/유압 실린더 추력")
    P = st.number_input("작동 압력 (bar)", value=6.0)
    D = st.number_input("실린더 내경 (mm)", value=50.0)
    A = math.pi * (D/2000)**2
    st.info(f"전진 추력: {(P * 1e5) * A:.1f} N")

# 6. PID 기초
elif "PID" in calc_menu:
    st.subheader("6. PID 제어 출력 예시")
    e = st.number_input("현재 오차 (e)", value=10.0)
    Kp = st.number_input("Kp 게인", value=1.0)
    Ki = st.number_input("Ki 게인", value=0.1)
    # 간단한 P + I 모델
    st.info(f"출력 (u = Kp*e + Ki*∫e): {Kp*e:.2f} (P항) + Ki항 누적")

# 7. 감쇠비
elif "감쇠비" in calc_menu:
    st.subheader("7. 제2차 시스템 감쇠비 (ζ)")
    st.markdown("오버슈트(%)를 기반으로 감쇠비 산출")
    overshoot = st.number_input("오버슈트 (%)", value=10.0) / 100
    zeta = -math.log(overshoot) / math.sqrt(math.pi**2 + math.log(overshoot)**2)
    st.info(f"감쇠비 (ζ): {zeta:.3f}")

# 8. 펄스 기반 이동
elif "펄스" in calc_menu:
    st.subheader("8. 펄스 이동 거리/속도")
    freq = st.number_input("주파수 (Hz)", value=1000.0)
    step_per_mm = st.number_input("Step per mm", value=200.0)
    st.info(f"이동 속도: {freq / step_per_mm:.2f} mm/s")

# 9. ADC 분해능
elif "ADC" in calc_menu:
    st.subheader("9. ADC 분해능")
    bits = st.number_input("비트 수 (bits)", value=12)
    v_ref = st.number_input("기준 전압 (V)", value=5.0)
    st.info(f"최소 단위 (LSB): {v_ref / (2**bits):.5f} V")

# 10. 1차 시스템 시정수
elif "시정수" in calc_menu:
    st.subheader("10. 1차 시스템 시정수")
    st.markdown("응답 속도 63.2% 도달 시간")
    st.info("단순 지연 시스템에서 T = 1/a 일 때 응답 도달 시간 계산")
    a = st.number_input("극점(Pole) 위치 (a)", value=1.0)
    st.info(f"시정수 (τ): {1/a:.3f} s")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Mechatronics Engineers")
