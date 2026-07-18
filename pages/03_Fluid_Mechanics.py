import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Fluid Mechanics", page_icon="🌊", layout="centered")

st.title("🌊 유체역학 통합 계산기")
st.markdown("관로 마찰, 펌프 용량, 수격 현상 등 배관 유동 및 공력 설계에 필요한 10대 핵심 수식입니다.")
st.divider()

# 10종 계산기 메뉴 선택
calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 레이놀즈 수 (Reynolds Number)",
    "2. 다르시-바이스바흐 압력 강하 (Darcy-Weisbach)",
    "3. 무디 마찰 계수 근사 (Haaland Equation)",
    "4. 오리피스 및 벤투리 질량 유량",
    "5. 베르누이 정리 (Bernoulli's Equation)",
    "6. 펌프 축동력 및 효율 (Pump Power)",
    "7. 유효 흡입 수두 (NPSH available)",
    "8. 수력 직경 (Hydraulic Diameter)",
    "9. 수격 현상 최대 압력 (Water Hammer)",
    "10. 항력 및 양력 (Drag & Lift Force)"
])

st.write("---")

# ---------------------------------------------------------
# 1. 레이놀즈 수
# ---------------------------------------------------------
if "레이놀즈" in calc_menu:
    st.subheader("1. 레이놀즈 수 (Reynolds Number)")
    st.latex(r"Re = \frac{\rho V D}{\mu}")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0, step=10.0)
        vel = st.number_input("유속, V (m/s)", value=2.0, step=0.1)
    with col2:
        dia = st.number_input("배관 직경, D (m)", value=0.1, step=0.01)
        mu = st.number_input("점성계수, μ (Pa·s)", value=0.001, format="%f")
    
    if mu > 0:
        reynolds = (rho * vel * dia) / mu
        st.info(f"**Reynolds Number (Re): {reynolds:,.0f}**")

# ---------------------------------------------------------
# 2. 다르시-바이스바흐
# ---------------------------------------------------------
elif "다르시" in calc_menu:
    st.subheader("2. 다르시-바이스바흐 압력 강하")
    st.latex(r"\Delta p = f \frac{L}{D} \frac{\rho V^2}{2}")
    
    col1, col2 = st.columns(2)
    with col1:
        f = st.number_input("마찰 계수, f", value=0.02, format="%f")
        L = st.number_input("배관 길이, L (m)", value=50.0)
        D = st.number_input("배관 직경, D (m)", value=0.2)
    with col2:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
        vel = st.number_input("유속, V (m/s)", value=2.5)
        
    if D > 0:
        dp = f * (L / D) * (rho * vel**2) / 2
        st.info(f"**압력 강하 (Δp): {dp:,.2f} Pa ({dp/100000:,.3f} bar)**")

# ---------------------------------------------------------
# 3. 무디 마찰 계수 (Haaland)
# ---------------------------------------------------------
elif "무디" in calc_menu:
    st.subheader("3. 배관 마찰 계수 (Haaland Equation)")
    st.markdown("Colebrook-White 방정식의 명시적 근사식으로 난류 영역의 마찰 계수를 구합니다.")
    st.latex(r"\frac{1}{\sqrt{f}} = -1.8 \log_{10} \left[ \left(\frac{\epsilon/D}{3.7}\right)^{1.11} + \frac{6.9}{Re} \right]")
    
    col1, col2 = st.columns(2)
    with col1:
        epsilon = st.number_input("표면 조도, ε (mm)", value=0.045, help="상용 강관 기준 0.045mm")
        D_mm = st.number_input("배관 직경, D (mm)", value=100.0)
    with col2:
        Re = st.number_input("레이놀즈 수, Re", value=50000.0)
        
    if Re > 4000 and D_mm > 0:
        rel_rough = epsilon / D_mm
        term = (rel_rough / 3.7)**1.11 + (6.9 / Re)
        f = ( -1.8 * math.log10(term) )**(-2)
        st.info(f"**상대 조도 (ε/D): {rel_rough:.5f}**")
        st.success(f"**마찰 계수 (f): {f:.5f}**")
    else:
        st.warning("난류 영역(Re > 4000)에서만 유효한 근사식입니다.")

# ---------------------------------------------------------
# 4. 오리피스 질량 유량
# ---------------------------------------------------------
elif "오리피스" in calc_menu:
    st.subheader("4. 오리피스/벤투리 질량 유량")
    st.latex(r"\dot{m} = C_d A \sqrt{2 \rho \Delta p}")
    
    col1, col2 = st.columns(2)
    with col1:
        Cd = st.number_input("유량 계수, Cd", value=0.61)
        A_cm2 = st.number_input("개구 면적, A (cm²)", value=20.0)
    with col2:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
        dp = st.number_input("차압, Δp (Pa)", value=15000.0)
        
    A_m2 = A_cm2 / 10000
    if dp >= 0:
        m_dot = Cd * A_m2 * math.sqrt(2 * rho * dp)
        st.info(f"**질량 유량: {m_dot:,.2f} kg/s ({m_dot*3600:,.1f} kg/h)**")

# ---------------------------------------------------------
# 5. 베르누이 정리
# ---------------------------------------------------------
elif "베르누이" in calc_menu:
    st.subheader("5. 베르누이 정리 (비압축성, 정상유동)")
    st.markdown("지점 1과 지점 2 사이의 수두(Head) 보존을 계산하여 미지수 압력(P2)을 도출합니다.")
    
    col1, col2 = st.columns(2)
    rho = st.number_input("유체 밀도, ρ (kg/m³)", value=1000.0)
    g = 9.80665
    
    with col1:
        st.markdown("**지점 1 (입구)**")
        P1 = st.number_input("압력 P1 (Pa)", value=200000.0)
        V1 = st.number_input("유속 V1 (m/s)", value=2.0)
        Z1 = st.number_input("높이 Z1 (m)", value=0.0)
    with col2:
        st.markdown("**지점 2 (출구)**")
        V2 = st.number_input("유속 V2 (m/s)", value=5.0)
        Z2 = st.number_input("높이 Z2 (m)", value=10.0)
        H_loss = st.number_input("수두 손실 (m)", value=0.0)
        
    H1 = (P1 / (rho * g)) + (V1**2 / (2 * g)) + Z1
    H2_kinetic_pot = (V2**2 / (2 * g)) + Z2
    P2 = (H1 - H2_kinetic_pot - H_loss) * rho * g
    
    st.info(f"**지점 2 예상 압력 (P2): {P2:,.0f} Pa ({P2/100000:,.3f} bar)**")

# ---------------------------------------------------------
# 6. 펌프 축동력
# ---------------------------------------------------------
elif "펌프" in calc_menu:
    st.subheader("6. 펌프 축동력 및 효율")
    st.latex(r"P = \frac{\rho g Q H}{\eta}")
    
    col1, col2 = st.columns(2)
    with col1:
        Q_lpm = st.number_input("유량, Q (L/min)", value=1200.0)
        H = st.number_input("총 양정, H (m)", value=30.0)
    with col2:
        rho = st.number_input("유체 밀도, ρ (kg/m³)", value=1000.0)
        eta = st.number_input("전효율, η (%)", value=75.0) / 100.0
        
    Q_m3s = Q_lpm / 60000
    if eta > 0:
        power_W = (rho * 9.80665 * Q_m3s * H) / eta
        st.info(f"**필요 축동력: {power_W/1000:,.2f} kW**")

# ---------------------------------------------------------
# 7. 유효 흡입 수두 (NPSHa)
# ---------------------------------------------------------
elif "NPSH" in calc_menu:
    st.subheader("7. 유효 흡입 수두 (NPSH available)")
    st.markdown("펌프 입구에서의 공동현상(Cavitation) 발생을 방지하기 위한 여유 수두입니다.")
    st.latex(r"NPSH_a = \frac{P_{atm} - P_{vapor}}{\rho g} \pm H_s - H_f")
    
    col1, col2 = st.columns(2)
    with col1:
        Patm = st.number_input("대기압 (Pa)", value=101325.0)
        Pv = st.number_input("포화증기압 (Pa)", value=2339.0, help="20°C 물 기준")
        rho = st.number_input("밀도, ρ (kg/m³)", value=998.0)
    with col2:
        Hs = st.number_input("흡입 수위 높이 (m)", value=-2.0, help="펌프 아래면 -, 위면 +")
        Hf = st.number_input("흡입관 마찰 손실 수두 (m)", value=0.5)
        
    NPSHa = ((Patm - Pv) / (rho * 9.80665)) + Hs - Hf
    st.info(f"**유효 흡입 수두 (NPSHa): {NPSHa:,.2f} m**")

# ---------------------------------------------------------
# 8. 수력 직경
# ---------------------------------------------------------
elif "수력 직경" in calc_menu:
    st.subheader("8. 수력 직경 (Hydraulic Diameter)")
    st.markdown("비원형 배관을 흐르는 유동 해석 시 사용하는 등가 직경입니다.")
    st.latex(r"D_h = \frac{4 A}{P}")
    
    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input("유로 단면적, A (m²)", value=0.05)
    with col2:
        P = st.number_input("윤변 (접수 길이), P (m)", value=0.9)
        
    if P > 0:
        Dh = (4 * A) / P
        st.info(f"**수력 직경 (Dh): {Dh:,.4f} m**")

# ---------------------------------------------------------
# 9. 수격 현상
# ---------------------------------------------------------
elif "수격" in calc_menu:
    st.subheader("9. 수격 현상 (Water Hammer - Joukowsky Eq)")
    st.markdown("밸브 급폐쇄 시 발생하는 최대 압력 상승폭을 계산합니다.")
    st.latex(r"\Delta P = \rho c \Delta V")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
        c = st.number_input("유체 내 음속, c (m/s)", value=1480.0, help="물 기준 약 1480 m/s")
    with col2:
        V = st.number_input("급폐쇄 전 유속, V (m/s)", value=3.0)
        
    dp_surge = rho * c * V
    st.info(f"**최대 서지 압력 상승 (ΔP): {dp_surge/100000:,.1f} bar**")

# ---------------------------------------------------------
# 10. 항력 및 양력
# ---------------------------------------------------------
elif "항력" in calc_menu:
    st.subheader("10. 항력 및 양력 (Drag & Lift Force)")
    st.latex(r"F = \frac{1}{2} \rho V^2 A C")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("유체 밀도, ρ (kg/m³)", value=1.225, help="대기 기준")
        V = st.number_input("상대 유속, V (m/s)", value=25.0)
        A = st.number_input("투영 면적, A (m²)", value=2.0)
    with col2:
        Cd = st.number_input("항력 계수, Cd", value=0.3)
        Cl = st.number_input("양력 계수, Cl", value=0.8)
        
    dyn_pressure = 0.5 * rho * V**2
    drag = dyn_pressure * A * Cd
    lift = dyn_pressure * A * Cl
    
    st.info(f"**항력 (Drag): {drag:,.1f} N**")
    st.success(f"**양력 (Lift): {lift:,.1f} N**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
