import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Dynamics", page_icon="⚙️", layout="centered")

st.title("⚙️ 동역학 통합 계산기")
st.markdown("선형 및 회전 운동 시스템의 변위, 속도, 가속도, 그리고 작용하는 하중을 계산하는 10대 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 1차원 등가속도 운동 (1D Kinematics)",
    "2. 뉴턴 제2법칙 (Newton's 2nd Law)",
    "3. 일-에너지 정리 (Work-Energy Theorem)",
    "4. 1차원 충돌 및 반발 계수 (Restitution)",
    "5. 원운동 및 구심력 (Centripetal Force)",
    "6. 질량 관성 모멘트 (Mass Moment of Inertia)",
    "7. 강체 회전 동역학 (Rotational Dynamics)",
    "8. 역적-운동량 정리 (Impulse-Momentum)",
    "9. 단진자 주기 계산 (Simple Pendulum)",
    "10. 단순 기어 트레인 (Gear Train Ratio)"
])

st.write("---")

# ---------------------------------------------------------
# 1. 1차원 등가속도 운동
# ---------------------------------------------------------
if "등가속도" in calc_menu:
    st.subheader("1. 1차원 등가속도 운동 (Kinematics)")
    st.latex(r"v = v_0 + at, \quad s = v_0 t + \frac{1}{2} a t^2")
    
    col1, col2 = st.columns(2)
    with col1:
        v0 = st.number_input("초기 속도, v_0 (m/s)", value=0.0)
        a = st.number_input("가속도, a (m/s²)", value=9.81)
    with col2:
        t = st.number_input("시간, t (s)", value=5.0)
        
    v = v0 + (a * t)
    s = (v0 * t) + (0.5 * a * t**2)
    
    st.info(f"**{t}초 후 속도 (v): {v:,.2f} m/s**")
    st.success(f"**이동 거리 (s): {s:,.2f} m**")

# ---------------------------------------------------------
# 2. 뉴턴 제2법칙
# ---------------------------------------------------------
elif "뉴턴" in calc_menu:
    st.subheader("2. 뉴턴 제2법칙 (F = ma)")
    
    target = st.radio("계산할 미지수 선택:", ["힘 (F)", "질량 (m)", "가속도 (a)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if "F" not in target:
            F = st.number_input("작용하는 알짜힘, F (N)", value=500.0)
        if "m" not in target:
            m = st.number_input("질량, m (kg)", value=100.0)
    with col2:
        if "a" not in target:
            a = st.number_input("가속도, a (m/s²)", value=5.0)
            
    if "F" in target:
        result = m * a
        st.info(f"**필요한 알짜힘 (F): {result:,.2f} N**")
    elif "m" in target:
        if a != 0:
            result = F / a
            st.info(f"**물체의 질량 (m): {result:,.2f} kg**")
        else:
            st.error("가속도는 0이 될 수 없습니다.")
    elif "a" in target:
        if m > 0:
            result = F / m
            st.info(f"**발생 가속도 (a): {result:,.2f} m/s²**")
        else:
            st.error("질량은 0보다 커야 합니다.")

# ---------------------------------------------------------
# 3. 일-에너지 정리
# ---------------------------------------------------------
elif "일-에너지" in calc_menu:
    st.subheader("3. 일-에너지 정리 (Work-Energy Theorem)")
    st.markdown("물체에 해준 일(W)은 운동 에너지(KE)의 변화량과 같습니다.")
    st.latex(r"W = F \cdot d = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2")
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("질량, m (kg)", value=1000.0)
        vi = st.number_input("초기 속도, v_i (m/s)", value=0.0)
    with col2:
        vf = st.number_input("나중 속도, v_f (m/s)", value=20.0)
        d = st.number_input("이동 거리, d (m)", value=50.0)
        
    delta_KE = 0.5 * m * (vf**2 - vi**2)
    if d > 0:
        F_avg = delta_KE / d
        st.info(f"**운동 에너지 변화량 (방해/가속에 필요한 일): {delta_KE / 1000:,.2f} kJ**")
        st.success(f"**평균 작용 힘 (F_avg): {F_avg:,.2f} N**")

# ---------------------------------------------------------
# 4. 1차원 충돌 및 반발 계수
# ---------------------------------------------------------
elif "충돌" in calc_menu:
    st.subheader("4. 1차원 충돌 및 반발 계수 (e)")
    st.markdown("두 물체의 충돌 전 속도와 반발 계수를 기반으로 충돌 후 속도를 산출합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**물체 A**")
        mA = st.number_input("질량 m_A (kg)", value=2.0)
        uA = st.number_input("충돌 전 속도 u_A (m/s)", value=5.0)
    with col2:
        st.markdown("**물체 B**")
        mB = st.number_input("질량 m_B (kg)", value=3.0)
        uB = st.number_input("충돌 전 속도 u_B (m/s)", value=-2.0)
        
    e = st.number_input("반발 계수, e (0~1)", value=0.8, min_value=0.0, max_value=1.0)
    
    # 운동량 보존: mA*vA + mB*vB = mA*uA + mB*uB = P_total
    # 반발 계수: vB - vA = e*(uA - uB) = dV
    P_total = mA*uA + mB*uB
    dV = e * (uA - uB)
    
    vA = (P_total - mB*dV) / (mA + mB)
    vB = vA + dV
    
    st.info(f"물체 A 충돌 후 속도 (v_A): **{vA:,.2f} m/s**")
    st.success(f"물체 B 충돌 후 속도 (v_B): **{vB:,.2f} m/s**")

# ---------------------------------------------------------
# 5. 구심력
# ---------------------------------------------------------
elif "구심력" in calc_menu:
    st.subheader("5. 원운동 및 구심력 (Centripetal Force)")
    st.latex(r"F_c = m \frac{v^2}{r} = m r \omega^2")
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("질량, m (kg)", value=10.0)
        r = st.number_input("회전 반경, r (m)", value=0.5)
    with col2:
        rpm = st.number_input("회전 속도 (RPM)", value=300.0)
        
    if r > 0:
        omega = rpm * (2 * math.pi / 60)
        v = r * omega
        Fc = m * r * omega**2
        st.info(f"접선 속도 (v): **{v:,.2f} m/s**")
        st.success(f"구심력 (F_c): **{Fc:,.2f} N**")

# ---------------------------------------------------------
# 6. 질량 관성 모멘트
# ---------------------------------------------------------
elif "관성 모멘트" in calc_menu:
    st.subheader("6. 기본 도형의 질량 관성 모멘트 (Mass Moment of Inertia)")
    shape = st.radio("회전체 형상 선택:", ["원통형 솔리드 (원판)", "가느다란 막대 (중심 회전)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    if "원통형" in shape:
        with col1:
            m = st.number_input("질량, m (kg)", value=5.0, key="m1")
        with col2:
            r = st.number_input("반지름, r (m)", value=0.2, key="r1")
        I = 0.5 * m * r**2
        st.latex(r"I = \frac{1}{2} m r^2")
        st.info(f"**질량 관성 모멘트 (I): {I:,.4f} kg·m²**")
    else:
        with col1:
            m = st.number_input("질량, m (kg)", value=2.0, key="m2")
        with col2:
            L = st.number_input("막대 길이, L (m)", value=1.0, key="L2")
        I = (1/12) * m * L**2
        st.latex(r"I = \frac{1}{12} m L^2")
        st.info(f"**질량 관성 모멘트 (I): {I:,.4f} kg·m²**")

# ---------------------------------------------------------
# 7. 강체 회전 동역학
# ---------------------------------------------------------
elif "강체 회전" in calc_menu:
    st.subheader("7. 강체 회전 동역학 (T = Iα)")
    st.latex(r"\tau = I \cdot \alpha")
    
    col1, col2 = st.columns(2)
    with col1:
        I = st.number_input("질량 관성 모멘트, I (kg·m²)", value=0.1)
    with col2:
        alpha = st.number_input("각가속도, α (rad/s²)", value=50.0)
        
    T = I * alpha
    st.info(f"**필요 토크 (τ): {T:,.2f} N·m**")

# ---------------------------------------------------------
# 8. 역적-운동량 정리
# ---------------------------------------------------------
elif "역적" in calc_menu:
    st.subheader("8. 역적-운동량 정리 (Impulse-Momentum)")
    st.markdown("짧은 시간 동안 가해진 힘(충격력)이 물체의 속도(운동량)를 얼마나 변화시키는지 계산합니다.")
    st.latex(r"J = F_{avg} \cdot \Delta t = m(v_f - v_i)")
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("물체 질량, m (kg)", value=0.15, help="야구공 무게 예시")
        dt = st.number_input("접촉 시간, Δt (s)", value=0.01)
    with col2:
        vi = st.number_input("초기 속도, v_i (m/s)", value=-30.0, help="투수가 던진 속도")
        vf = st.number_input("나중 속도, v_f (m/s)", value=40.0, help="타격 후 속도")
        
    if dt > 0:
        impulse = m * (vf - vi)
        F_avg = impulse / dt
        st.info(f"**충격량 (J): {impulse:,.2f} N·s**")
        st.success(f"**평균 충격력 (F_avg): {F_avg:,.0f} N**")

# ---------------------------------------------------------
# 9. 단진자 주기 계산
# ---------------------------------------------------------
elif "단진자" in calc_menu:
    st.subheader("9. 단진자 운동 (Simple Pendulum)")
    st.markdown("소진폭(Small amplitude) 조건에서의 이상적인 진자의 진동 주기입니다.")
    st.latex(r"T = 2\pi \sqrt{\frac{L}{g}}")
    
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("진자의 줄 길이, L (m)", value=1.0)
    with col2:
        g = st.number_input("중력가속도, g (m/s²)", value=9.80665)
        
    if L > 0 and g > 0:
        period = 2 * math.pi * math.sqrt(L / g)
        freq = 1 / period
        st.info(f"**1회 왕복 주기 (T): {period:,.3f} 초**")
        st.success(f"**진동 주파수 (f): {freq:,.3f} Hz**")

# ---------------------------------------------------------
# 10. 단순 기어 트레인
# ---------------------------------------------------------
elif "기어" in calc_menu:
    st.subheader("10. 단순 기어 트레인 (Gear Ratio)")
    st.markdown("구동 기어(Driver)와 종동 기어(Driven)의 잇수(Teeth) 비에 따른 회전수와 토크를 계산합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**구동 기어 (Driver, 입력)**")
        Z1 = st.number_input("입력 잇수, Z1", value=20, min_value=1, step=1)
        N1 = st.number_input("입력 회전수 (RPM)", value=1750.0)
        T1 = st.number_input("입력 토크 (N·m)", value=10.0)
    with col2:
        st.markdown("**종동 기어 (Driven, 출력)**")
        Z2 = st.number_input("출력 잇수, Z2", value=60, min_value=1, step=1)
        eff = st.number_input("동력 전달 효율 (%)", value=95.0) / 100.0
        
    ratio = Z2 / Z1
    N2 = N1 / ratio
    T2 = (T1 * ratio) * eff
    
    st.info(f"**기어비 (Ratio, Z2/Z1): {ratio:,.2f}**")
    st.success(f"**출력 회전수: {N2:,.0f} RPM | 출력 토크: {T2:,.2f} N·m**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Engineers")
