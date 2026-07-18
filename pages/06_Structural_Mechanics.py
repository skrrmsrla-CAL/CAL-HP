import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Structural Mechanics", page_icon="🏗️", layout="centered")

st.title("🏗️ 구조역학 통합 계산기")
st.markdown("보의 처짐, 좌굴, 진동 및 연결부(볼트/용접) 강도를 평가하는 구조 해석 10대 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 외팔보 최대 처짐 (Cantilever Deflection)",
    "2. 단순 지지보 중앙 처짐 (Simply Supported Beam)",
    "3. 오일러 좌굴 하중 (Euler Buckling)",
    "4. 스프링 등가 강성 (Spring Equivalent)",
    "5. 1차 부정정 보 (양단 고정) 반력",
    "6. 1자유도 고유 진동수 (Natural Frequency)",
    "7. 낙하 충격 하중 계수 (Impact Load Factor)",
    "8. 볼트 조인트 전단 하중 (Bolt Shear)",
    "9. 필릿 용접부 전단 응력 (Fillet Weld Stress)",
    "10. 축하중 부재의 변형량 (Axial Deformation)"
])

st.write("---")

# ---------------------------------------------------------
# 1. 외팔보 최대 처짐
# ---------------------------------------------------------
if "외팔보" in calc_menu:
    st.subheader("1. 외팔보 끝단 집중하중 처짐")
    st.latex(r"\delta_{max} = \frac{P L^3}{3 E I}")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("집중 하중, P (N)", value=1000.0)
        L = st.number_input("보의 길이, L (m)", value=2.0)
    with col2:
        E = st.number_input("탄성계수, E (GPa)", value=210.0)
        I_cm4 = st.number_input("단면 2차 모멘트, I (cm⁴)", value=1000.0)
        
    I_m4 = I_cm4 * 1e-8
    if E > 0 and I_m4 > 0:
        deflection = (P * L**3) / (3 * (E * 1e9) * I_m4)
        st.info(f"**최대 처짐량: {deflection * 1000:,.2f} mm**")

# ---------------------------------------------------------
# 2. 단순 지지보 중앙 처짐
# ---------------------------------------------------------
elif "단순 지지보" in calc_menu:
    st.subheader("2. 단순 지지보 중앙 집중하중 처짐")
    st.latex(r"\delta_{max} = \frac{P L^3}{48 E I}")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("중앙 집중 하중, P (N)", value=5000.0)
        L = st.number_input("보의 전체 길이, L (m)", value=4.0)
    with col2:
        E = st.number_input("탄성계수, E (GPa)", value=210.0)
        I_cm4 = st.number_input("단면 2차 모멘트, I (cm⁴)", value=1500.0)
        
    I_m4 = I_cm4 * 1e-8
    if E > 0 and I_m4 > 0:
        deflection = (P * L**3) / (48 * (E * 1e9) * I_m4)
        st.info(f"**최대 처짐량 (중앙): {deflection * 1000:,.2f} mm**")

# ---------------------------------------------------------
# 3. 오일러 좌굴 하중
# ---------------------------------------------------------
elif "오일러" in calc_menu:
    st.subheader("3. 기둥의 오일러 임계 좌굴 하중")
    st.latex(r"P_{cr} = \frac{\pi^2 E I}{(K L)^2}")
    
    K_dict = {"양단 힌지 (K=1.0)": 1.0, "일단 고정, 일단 자유 (K=2.0)": 2.0, "양단 고정 (K=0.5)": 0.5, "일단 고정, 일단 힌지 (K=0.7)": 0.7}
    k_sel = st.selectbox("기둥 지지 조건", list(K_dict.keys()))
    K = K_dict[k_sel]
    
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("기둥 길이, L (m)", value=3.0)
        E = st.number_input("탄성계수, E (GPa)", value=210.0)
    with col2:
        I_cm4 = st.number_input("최소 단면 2차 모멘트, I (cm⁴)", value=500.0)
        
    I_m4 = I_cm4 * 1e-8
    if L > 0 and I_m4 > 0:
        P_cr = (math.pi**2 * (E * 1e9) * I_m4) / (K * L)**2
        st.info(f"**임계 좌굴 하중 (P_cr): {P_cr / 1000:,.2f} kN**")

# ---------------------------------------------------------
# 4. 스프링 등가 강성
# ---------------------------------------------------------
elif "스프링" in calc_menu:
    st.subheader("4. 2-스프링 시스템 등가 강성")
    conn = st.radio("연결 방식:", ["직렬 (Series)", "병렬 (Parallel)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        k1 = st.number_input("스프링 1 강성, k1 (N/mm)", value=10.0)
    with col2:
        k2 = st.number_input("스프링 2 강성, k2 (N/mm)", value=20.0)
        
    if k1 > 0 and k2 > 0:
        if "직렬" in conn:
            k_eq = 1 / ((1/k1) + (1/k2))
            st.info(f"**등가 강성 (직렬): {k_eq:,.2f} N/mm** (더 연해짐)")
        else:
            k_eq = k1 + k2
            st.info(f"**등가 강성 (병렬): {k_eq:,.2f} N/mm** (더 뻣뻣해짐)")

# ---------------------------------------------------------
# 5. 부정정 보 (양단 고정) 반력
# ---------------------------------------------------------
elif "부정정 보" in calc_menu:
    st.subheader("5. 1차 부정정 보 (양단 고정, 중앙 집중하중)")
    st.markdown("정역학적 평형 방정식만으로는 풀 수 없는 잉여 구속 구조물입니다.")
    st.latex(r"R_A = R_B = \frac{P}{2}, \quad M_A = M_B = \frac{P L}{8}")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("중앙 집중 하중, P (N)", value=10000.0)
    with col2:
        L = st.number_input("보의 길이, L (m)", value=5.0)
        
    R = P / 2
    M = (P * L) / 8
    st.info(f"**지점 반력 (R_A, R_B): {R/1000:,.1f} kN**")
    st.success(f"**고정단 모멘트 (M_A, M_B): {M:,.1f} N·m**")

# ---------------------------------------------------------
# 6. 고유 진동수
# ---------------------------------------------------------
elif "진동수" in calc_menu:
    st.subheader("6. 1자유도 비감쇠 고유 진동수")
    st.latex(r"f_n = \frac{1}{2\pi} \sqrt{\frac{k}{m}}")
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("질량, m (kg)", value=50.0)
    with col2:
        k_N_m = st.number_input("시스템 강성, k (N/m)", value=50000.0)
        
    if m > 0 and k_N_m > 0:
        omega = math.sqrt(k_N_m / m)
        f_n = omega / (2 * math.pi)
        st.info(f"**고유 각진동수 (ω_n): {omega:,.2f} rad/s**")
        st.success(f"**고유 진동수 (f_n): {f_n:,.2f} Hz**")

# ---------------------------------------------------------
# 7. 낙하 충격 하중 계수
# ---------------------------------------------------------
elif "충격" in calc_menu:
    st.subheader("7. 낙하 충격 계수 및 하중")
    st.markdown("물체가 특정 높이에서 떨어졌을 때, 정하중 대비 증폭되는 하중 비율을 계산합니다.")
    st.latex(r"n = 1 + \sqrt{1 + \frac{2h}{\delta_{st}}}")
    
    col1, col2 = st.columns(2)
    with col1:
        W = st.number_input("물체 무게 (N)", value=1000.0)
        h = st.number_input("낙하 높이, h (mm)", value=50.0)
    with col2:
        delta_st = st.number_input("정적 하중 작용 시 처짐량, δ_st (mm)", value=2.0)
        
    if delta_st > 0:
        n = 1 + math.sqrt(1 + (2 * h) / delta_st)
        P_dyn = W * n
        st.info(f"**충격 계수 (n): {n:,.2f} 배**")
        st.success(f"**동적 최대 하중 (P_dyn): {P_dyn:,.0f} N**")

# ---------------------------------------------------------
# 8. 볼트 전단 하중
# ---------------------------------------------------------
elif "볼트" in calc_menu:
    st.subheader("8. 다중 볼트 연결부 전단 하중 분배")
    st.markdown("가해진 전단 하중이 n개의 동일한 볼트에 균등 분배된다고 가정합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        F = st.number_input("전체 전단 하중, F (N)", value=25000.0)
        n = st.number_input("체결 볼트 개수, n", value=4, min_value=1)
    with col2:
        d = st.number_input("볼트 직경, d (mm)", value=12.0)
        
    if d > 0:
        F_bolt = F / n
        A_bolt = (math.pi / 4) * (d**2)
        tau = F_bolt / A_bolt
        st.info(f"**볼트 1개당 작용 하중: {F_bolt:,.0f} N**")
        st.success(f"**볼트 단면 전단 응력 (τ): {tau:,.2f} MPa**")

# ---------------------------------------------------------
# 9. 필릿 용접부 전단 응력
# ---------------------------------------------------------
elif "용접" in calc_menu:
    st.subheader("9. 필릿 용접부 (Fillet Weld) 기초 응력")
    st.markdown("가장 취약한 용접 목 두께(Throat thickness)를 기준으로 전단 응력을 산출합니다.")
    st.latex(r"\tau = \frac{P}{0.707 \cdot s \cdot L_{weld}}")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("작용 하중, P (N)", value=15000.0)
        s = st.number_input("용접 다리 길이(사이즈), s (mm)", value=5.0)
    with col2:
        L_weld = st.number_input("총 유효 용접 길이, L (mm)", value=100.0)
        
    if s > 0 and L_weld > 0:
        throat = 0.707 * s
        area = throat * L_weld
        tau = P / area
        st.info(f"**용접부 최대 전단 응력 (τ): {tau:,.2f} MPa**")

# ---------------------------------------------------------
# 10. 축하중 부재 변형량
# ---------------------------------------------------------
elif "축하중" in calc_menu:
    st.subheader("10. 1D 축하중 부재의 변형량 (프레임/트러스)")
    st.latex(r"\delta = \frac{P L}{A E}")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("축방향 인장/압축 하중, P (N)", value=10000.0)
        L = st.number_input("부재 원래 길이, L (m)", value=3.0)
    with col2:
        A_mm2 = st.number_input("단면적, A (mm²)", value=500.0)
        E = st.number_input("탄성계수, E (GPa)", value=210.0)
        
    if A_mm2 > 0 and E > 0:
        deflection = (P * L) / ((A_mm2 * 1e-6) * (E * 1e9))
        st.info(f"**부재 길이 변화량 (δ): {deflection * 1000:,.3f} mm**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
