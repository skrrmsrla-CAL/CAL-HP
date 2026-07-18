import streamlit as st
import math

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | Dimensionless Numbers", page_icon="🔢", layout="centered")

st.title("유체 및 열역학 무차원 수 (Dimensionless Numbers)")
st.markdown("유체 유동, 열전달, 물질 전달 현상의 지배적인 물리력을 비교하고 상사성(Similarity)을 평가하기 위한 무차원 수 계산기입니다.")
st.divider()

# 무차원 수 목록
dim_numbers = [
    "레이놀즈 수 (Reynolds Number, Re) - 유동 특성",
    "프라우드 수 (Froude Number, Fr) - 자유 표면 유동",
    "프란틀 수 (Prandtl Number, Pr) - 열전달",
    "마하 수 (Mach Number, Ma) - 압축성 유동",
    "웨버 수 (Weber Number, We) - 다상 유동/표면장력",
    "오일러 수 (Euler Number, Eu) - 압력 강하",
    "누셀트 수 (Nusselt Number, Nu) - 대류 열전달",
    "그라스호프 수 (Grashof Number, Gr) - 자연 대류",
    "페클레 수 (Peclet Number, Pe) - 이류 vs 확산",
    "슈미트 수 (Schmidt Number, Sc) - 물질 전달",
    "스트로할 수 (Strouhal Number, St) - 진동/와류"
]

selected_num = st.selectbox("계산할 무차원 수를 선택하세요:", dim_numbers)
st.write("") # 여백

# ---------------------------------------------------------
# 1. 레이놀즈 수 (Re)
# ---------------------------------------------------------
if "Reynolds" in selected_num:
    st.subheader("레이놀즈 수 (Reynolds Number)")
    st.markdown("**관성력 (Inertial force) / 점성력 (Viscous force)**")
    st.latex(r"Re = \frac{\rho V L}{\mu} = \frac{V L}{\nu}")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
        vel = st.number_input("유속, V (m/s)", value=2.0)
    with col2:
        length = st.number_input("특성 길이, L (m)", value=0.1)
        mu = st.number_input("점성계수, μ (Pa·s)", value=0.001, format="%f")
    
    if mu > 0:
        result = (rho * vel * length) / mu
        st.success(f"**Re = {result:,.0f}**")

# ---------------------------------------------------------
# 2. 프라우드 수 (Fr)
# ---------------------------------------------------------
elif "Froude" in selected_num:
    st.subheader("프라우드 수 (Froude Number)")
    st.markdown("**관성력 (Inertial force) / 중력 (Gravitational force)** - 선박 조파 저항 및 개수로 유동에 사용")
    st.latex(r"Fr = \frac{V}{\sqrt{g L}}")
    
    col1, col2 = st.columns(2)
    with col1:
        vel = st.number_input("유속, V (m/s)", value=5.0)
        length = st.number_input("특성 길이(수심 등), L (m)", value=2.0)
    with col2:
        g = st.number_input("중력가속도, g (m/s²)", value=9.80665)
    
    if g > 0 and length > 0:
        result = vel / math.sqrt(g * length)
        st.success(f"**Fr = {result:,.3f}**")

# ---------------------------------------------------------
# 3. 프란틀 수 (Pr)
# ---------------------------------------------------------
elif "Prandtl" in selected_num:
    st.subheader("프란틀 수 (Prandtl Number)")
    st.markdown("**운동량 확산 (Momentum diffusivity) / 열 확산 (Thermal diffusivity)** - 유체 고유의 물성치")
    st.latex(r"Pr = \frac{\nu}{\alpha} = \frac{c_p \mu}{k}")
    
    col1, col2 = st.columns(2)
    with col1:
        cp = st.number_input("비열, c_p (J/kg·K)", value=4184.0)
        mu = st.number_input("점성계수, μ (Pa·s)", value=0.001, format="%f")
    with col2:
        k = st.number_input("열전도도, k (W/m·K)", value=0.6)
    
    if k > 0:
        result = (cp * mu) / k
        st.success(f"**Pr = {result:,.2f}**")

# ---------------------------------------------------------
# 4. 마하 수 (Ma)
# ---------------------------------------------------------
elif "Mach" in selected_num:
    st.subheader("마하 수 (Mach Number)")
    st.markdown("**관성력 (Inertial force) / 압축력 (Compressibility force)** - 유속과 음속의 비율")
    st.latex(r"Ma = \frac{V}{c}")
    
    col1, col2 = st.columns(2)
    with col1:
        vel = st.number_input("유속, V (m/s)", value=340.0)
    with col2:
        c = st.number_input("음속, c (m/s)", value=340.29)
    
    if c > 0:
        result = vel / c
        st.success(f"**Ma = {result:,.3f}**")

# ---------------------------------------------------------
# 5. 웨버 수 (We)
# ---------------------------------------------------------
elif "Weber" in selected_num:
    st.subheader("웨버 수 (Weber Number)")
    st.markdown("**관성력 (Inertial force) / 표면장력 (Surface tension force)** - 액적 분열, 다상 유동 해석")
    st.latex(r"We = \frac{\rho V^2 L}{\sigma}")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
        vel = st.number_input("유속, V (m/s)", value=1.0)
    with col2:
        length = st.number_input("특성 길이(액적 직경), L (m)", value=0.005, format="%f")
        sigma = st.number_input("표면장력, σ (N/m)", value=0.0728, format="%f")
    
    if sigma > 0:
        result = (rho * vel**2 * length) / sigma
        st.success(f"**We = {result:,.1f}**")

# ---------------------------------------------------------
# 6. 오일러 수 (Eu)
# ---------------------------------------------------------
elif "Euler" in selected_num:
    st.subheader("오일러 수 (Euler Number)")
    st.markdown("**압력차 (Pressure force) / 관성력 (Inertial force)** - 배관 및 밸브 압력 강하 평가")
    st.latex(r"Eu = \frac{\Delta p}{\rho V^2}")
    
    col1, col2 = st.columns(2)
    with col1:
        dp = st.number_input("압력 강하, Δp (Pa)", value=50000.0)
        rho = st.number_input("밀도, ρ (kg/m³)", value=1000.0)
    with col2:
        vel = st.number_input("유속, V (m/s)", value=2.0)
    
    if rho > 0 and vel > 0:
        result = dp / (rho * vel**2)
        st.success(f"**Eu = {result:,.3f}**")

# ---------------------------------------------------------
# 7. 누셀트 수 (Nu)
# ---------------------------------------------------------
elif "Nusselt" in selected_num:
    st.subheader("누셀트 수 (Nusselt Number)")
    st.markdown("**대류 열전달 (Convective heat transfer) / 전도 열전달 (Conductive heat transfer)**")
    st.latex(r"Nu = \frac{h L}{k}")
    
    col1, col2 = st.columns(2)
    with col1:
        h = st.number_input("대류 열전달 계수, h (W/m²·K)", value=50.0)
        length = st.number_input("특성 길이, L (m)", value=0.1)
    with col2:
        k = st.number_input("유체의 열전도도, k (W/m·K)", value=0.026)
    
    if k > 0:
        result = (h * length) / k
        st.success(f"**Nu = {result:,.2f}**")

# ---------------------------------------------------------
# 8. 그라스호프 수 (Gr)
# ---------------------------------------------------------
elif "Grashof" in selected_num:
    st.subheader("그라스호프 수 (Grashof Number)")
    st.markdown("**부력 (Buoyancy force) / 점성력 (Viscous force)** - 자연 대류 유동에서 레이놀즈 수를 대체")
    st.latex(r"Gr = \frac{g \beta (T_s - T_\infty) L^3}{\nu^2}")
    
    col1, col2 = st.columns(2)
    with col1:
        g = st.number_input("중력가속도, g (m/s²)", value=9.81)
        beta = st.number_input("체적 팽창 계수, β (1/K)", value=0.0034, format="%f")
        length = st.number_input("특성 길이, L (m)", value=0.5)
    with col2:
        dt = st.number_input("온도차, ΔT (K 또는 °C)", value=20.0)
        nu = st.number_input("동점성계수, ν (m²/s)", value=0.000015, format="%f")
    
    if nu > 0:
        result = (g * beta * dt * length**3) / (nu**2)
        st.success(f"**Gr = {result:.3e}**")

# ---------------------------------------------------------
# 9. 페클레 수 (Pe)
# ---------------------------------------------------------
elif "Peclet" in selected_num:
    st.subheader("페클레 수 (Peclet Number)")
    st.markdown("**이류 속도 (Advective transport rate) / 확산 속도 (Diffusive transport rate)**")
    st.latex(r"Pe = \frac{L V}{\alpha} = Re \cdot Pr")
    
    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("특성 길이, L (m)", value=0.1)
        vel = st.number_input("유속, V (m/s)", value=1.5)
    with col2:
        alpha = st.number_input("열 확산 계수, α (m²/s)", value=0.000022, format="%f")
    
    if alpha > 0:
        result = (length * vel) / alpha
        st.success(f"**Pe = {result:,.0f}**")

# ---------------------------------------------------------
# 10. 슈미트 수 (Sc)
# ---------------------------------------------------------
elif "Schmidt" in selected_num:
    st.subheader("슈미트 수 (Schmidt Number)")
    st.markdown("**운동량 확산 (Momentum diffusivity) / 질량 확산 (Mass diffusivity)** - 물질 전달 공정")
    st.latex(r"Sc = \frac{\nu}{D_m} = \frac{\mu}{\rho D_m}")
    
    col1, col2 = st.columns(2)
    with col1:
        nu = st.number_input("동점성계수, ν (m²/s)", value=0.000015, format="%f")
    with col2:
        d_m = st.number_input("질량 확산 계수, D_m (m²/s)", value=0.00002, format="%f")
    
    if d_m > 0:
        result = nu / d_m
        st.success(f"**Sc = {result:,.3f}**")

# ---------------------------------------------------------
# 11. 스트로할 수 (St)
# ---------------------------------------------------------
elif "Strouhal" in selected_num:
    st.subheader("스트로할 수 (Strouhal Number)")
    st.markdown("**유동의 진동 특성** - 카르만 와류(Karman Vortex) 등 진동하는 비정상(Unsteady) 유동")
    st.latex(r"St = \frac{f L}{V}")
    
    col1, col2 = st.columns(2)
    with col1:
        f = st.number_input("진동 주파수, f (Hz)", value=10.0)
        length = st.number_input("특성 길이(원통 직경 등), L (m)", value=0.05)
    with col2:
        vel = st.number_input("유속, V (m/s)", value=2.5)
    
    if vel > 0:
        result = (f * length) / vel
        st.success(f"**St = {result:,.3f}**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
