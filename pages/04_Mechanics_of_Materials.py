import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Mechanics of Materials", page_icon="🏗️", layout="centered")

st.title("🏗️ 재료역학 통합 계산기")
st.markdown("구조물의 응력, 변형률, 그리고 파손 이론을 평가하는 10대 핵심 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 후크의 법칙 (Hooke's Law)",
    "2. 탄성계수 및 푸아송 비 변환",
    "3. 열응력 (Thermal Stress)",
    "4. 모어의 원 (Mohr's Circle - 2D)",
    "5. 원형 축의 비틀림 (Torsion)",
    "6. 단면 2차 모멘트 (Area Moment of Inertia)",
    "7. 보의 굽힘 응력 (Bending Stress)",
    "8. 박판 압력 용기 (Thin-Walled Pressure Vessel)",
    "9. 안전율 (Factor of Safety)",
    "10. 폰 미세스 등가 응력 (Von Mises Stress)"
])

st.write("---")

# ---------------------------------------------------------
# 1. 후크의 법칙
# ---------------------------------------------------------
if "후크" in calc_menu:
    st.subheader("1. 후크의 법칙 (1D)")
    st.latex(r"\sigma = E \cdot \epsilon")
    
    col1, col2 = st.columns(2)
    with col1:
        E = st.number_input("탄성계수, E (GPa)", value=210.0, help="강철 기준 약 210 GPa")
    with col2:
        strain = st.number_input("변형률, ε (μe, 마이크로스트레인)", value=1000.0)
        
    stress = (E * 1e9) * (strain * 1e-6)
    st.info(f"**수직 응력 (σ): {stress / 1e6:,.2f} MPa**")

# ---------------------------------------------------------
# 2. 탄성계수 변환
# ---------------------------------------------------------
elif "탄성계수" in calc_menu:
    st.subheader("2. 탄성계수 및 푸아송 비 변환")
    st.latex(r"G = \frac{E}{2(1+\nu)}, \quad K = \frac{E}{3(1-2\nu)}")
    
    col1, col2 = st.columns(2)
    with col1:
        E = st.number_input("세로탄성계수, E (GPa)", value=210.0)
    with col2:
        nu = st.number_input("푸아송 비, ν", value=0.3, max_value=0.499)
        
    G = E / (2 * (1 + nu))
    K = E / (3 * (1 - 2 * nu))
    
    st.info(f"**전단탄성계수 (G): {G:,.2f} GPa**")
    st.success(f"**체적탄성계수 (K): {K:,.2f} GPa**")

# ---------------------------------------------------------
# 3. 열응력
# ---------------------------------------------------------
elif "열응력" in calc_menu:
    st.subheader("3. 열응력 (양단 구속시)")
    st.latex(r"\sigma_{th} = E \alpha \Delta T")
    
    col1, col2 = st.columns(2)
    with col1:
        E = st.number_input("탄성계수, E (GPa)", value=210.0)
        alpha = st.number_input("열팽창계수, α (1e-6 /°C)", value=12.0, help="강철: 12, 알루미늄: 23")
    with col2:
        dT = st.number_input("온도 변화, ΔT (°C)", value=50.0)
        
    stress_th = (E * 1e9) * (alpha * 1e-6) * dT
    st.info(f"**발생 열응력: {stress_th / 1e6:,.2f} MPa**")

# ---------------------------------------------------------
# 4. 모어의 원
# ---------------------------------------------------------
elif "모어의 원" in calc_menu:
    st.subheader("4. 모어의 원 (평면 응력)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sx = st.number_input("σ_x (MPa)", value=100.0)
    with col2:
        sy = st.number_input("σ_y (MPa)", value=50.0)
    with col3:
        txy = st.number_input("τ_xy (MPa)", value=30.0)
        
    s_avg = (sx + sy) / 2
    R = math.sqrt(((sx - sy) / 2)**2 + txy**2)
    s1 = s_avg + R
    s2 = s_avg - R
    
    st.info(f"주응력 1 (σ1): **{s1:.2f} MPa** | 주응력 2 (σ2): **{s2:.2f} MPa**")
    st.success(f"최대 전단응력 (τ_max): **{R:.2f} MPa**")

# ---------------------------------------------------------
# 5. 비틀림
# ---------------------------------------------------------
elif "비틀림" in calc_menu:
    st.subheader("5. 원형 축의 비틀림 (Torsion)")
    st.latex(r"\tau_{max} = \frac{T r}{J}, \quad \theta = \frac{T L}{J G}")
    
    col1, col2 = st.columns(2)
    with col1:
        T = st.number_input("토크, T (N·m)", value=500.0)
        D = st.number_input("축 직경, D (mm)", value=50.0)
    with col2:
        L = st.number_input("축 길이, L (m)", value=1.0)
        G = st.number_input("전단탄성계수, G (GPa)", value=80.0)
        
    if D > 0:
        r = (D / 1000) / 2
        J = (math.pi / 2) * (r**4)
        tau = (T * r) / J
        theta_rad = (T * L) / (J * G * 1e9)
        
        st.info(f"**최대 전단응력 (τ_max): {tau / 1e6:,.2f} MPa**")
        st.success(f"**비틀림 각도 (θ): {math.degrees(theta_rad):.3f} °**")

# ---------------------------------------------------------
# 6. 단면 2차 모멘트
# ---------------------------------------------------------
elif "단면 2차 모멘트" in calc_menu:
    st.subheader("6. 단면 2차 모멘트 (Area Moment of Inertia)")
    shape = st.radio("단면 형상:", ["직사각형 (Rectangle)", "원형 (Circle)"], horizontal=True)
    
    if shape == "직사각형 (Rectangle)":
        col1, col2 = st.columns(2)
        with col1:
            b = st.number_input("폭, b (mm)", value=100.0)
        with col2:
            h = st.number_input("높이, h (mm)", value=200.0)
        I = (b * h**3) / 12
        st.info(f"**I_x: {I:,.0f} mm⁴**")
    else:
        D = st.number_input("직경, D (mm)", value=100.0)
        I = (math.pi * D**4) / 64
        st.info(f"**I: {I:,.0f} mm⁴**")

# ---------------------------------------------------------
# 7. 굽힘 응력
# ---------------------------------------------------------
elif "굽힘" in calc_menu:
    st.subheader("7. 보의 최대 굽힘 응력")
    st.latex(r"\sigma_{max} = \frac{M y_{max}}{I}")
    
    col1, col2 = st.columns(2)
    with col1:
        M = st.number_input("굽힘 모멘트, M (N·m)", value=1000.0)
        y = st.number_input("중립축에서 최대 거리, y (mm)", value=50.0)
    with col2:
        I = st.number_input("단면 2차 모멘트, I (mm⁴)", value=4160000.0)
        
    if I > 0:
        stress = (M * (y / 1000)) / (I * 1e-12)
        st.info(f"**최대 굽힘 응력 (σ): {stress / 1e6:,.2f} MPa**")

# ---------------------------------------------------------
# 8. 박판 압력 용기
# ---------------------------------------------------------
elif "박판 압력" in calc_menu:
    st.subheader("8. 박판 압력 용기 (Thin-Walled Pressure Vessel)")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("내압, P (MPa)", value=5.0)
        D = st.number_input("용기 내경, D (mm)", value=1000.0)
    with col2:
        t = st.number_input("두께, t (mm)", value=10.0)
        
    if t > 0:
        hoop = (P * D) / (2 * t)
        axial = (P * D) / (4 * t)
        st.info(f"원주방향 응력 (Hoop, σ_h): **{hoop:,.2f} MPa**")
        st.success(f"축방향 응력 (Axial, σ_a): **{axial:,.2f} MPa**")

# ---------------------------------------------------------
# 9. 안전율
# ---------------------------------------------------------
elif "안전율" in calc_menu:
    st.subheader("9. 구조물 안전율 (Factor of Safety)")
    
    col1, col2 = st.columns(2)
    with col1:
        strength = st.number_input("재료의 항복 강도 (MPa)", value=250.0)
    with col2:
        stress = st.number_input("작용 최대 응력 (MPa)", value=150.0)
        
    if stress > 0:
        fs = strength / stress
        if fs >= 1.0:
            st.success(f"**안전율 (FoS): {fs:.2f}** (안전)")
        else:
            st.error(f"**안전율 (FoS): {fs:.2f}** (파손 위험)")

# ---------------------------------------------------------
# 10. 폰 미세스 등가 응력
# ---------------------------------------------------------
elif "폰 미세스" in calc_menu:
    st.subheader("10. 폰 미세스 등가 응력 (Von Mises)")
    st.markdown("복합 응력 상태를 하나의 스칼라 값으로 환산하여 항복 강도와 비교합니다.")
    st.latex(r"\sigma_{vm} = \sqrt{\sigma_x^2 - \sigma_x\sigma_y + \sigma_y^2 + 3\tau_{xy}^2}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sx = st.number_input("σ_x (MPa) ", value=120.0)
    with col2:
        sy = st.number_input("σ_y (MPa) ", value=-50.0)
    with col3:
        txy = st.number_input("τ_xy (MPa) ", value=40.0)
        
    vm = math.sqrt(sx**2 - sx*sy + sy**2 + 3*txy**2)
    st.info(f"**Von Mises 등가 응력: {vm:,.2f} MPa**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Engineers")
