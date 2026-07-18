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
    st.info("💡 **이론적 의미:** 유동이 층류(Laminar)인지 난류(Turbulent)인지를 결정하는 가장 중요한 지표입니다. 유속이 빠르고(관성력 증가) 점성이 낮을수록(점성력 감소) Re가 커지며, 이는 유체의 흐름이 불규칙해지고 난류가 발생하기 쉽다는 것을 의미합니다.", icon="💡")
    
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
    st.markdown("**관성력 (Inertial force) / 중력 (Gravitational force)**")
    st.latex(r"Fr = \frac{V}{\sqrt{g L}}")
    st.info("💡 **이론적 의미:** 선박이 물 위를 나아갈 때 발생하는 조파 저항(Wave-making resistance)이나 댐, 하천 등의 자유 표면(Free surface) 유동을 해석할 때 핵심이 되는 수치입니다. 모형 시험 결과를 실제 크기(Scale-up)로 변환할 때 필수적으로 일치시켜야 하는 조건입니다.", icon="💡")
    
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
    st.markdown("**운동량 확산 (Momentum diffusivity) / 열 확산 (Thermal diffusivity)**")
    st.latex(r"Pr = \frac{\nu}{\alpha} = \frac{c_p \mu}{k}")
    st.info("💡 **이론적 의미:** 유속이나 기하학적 형태에 의존하지 않는 **'유체 고유의 물성치'**입니다. Pr이 1에 가까우면 속도 경계층과 온도 경계층의 두께가 비슷하게 발달함을 의미하며, 액체 금속은 Pr이 매우 작고 윤활유 등은 매우 큽니다.", icon="💡")
    
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
    st.markdown("**유속 (Flow velocity) / 음속 (Speed of sound)**")
    st.latex(r"Ma = \frac{V}{c}")
    st.info("💡 **이론적 의미:** 관성력과 압축력의 비율을 의미합니다. 통상적으로 Ma가 0.3을 초과하면 유동에 따른 밀도 변화가 커지므로, 단순 비압축성이 아닌 압축성 유동(Compressible flow) 방정식을 사용하여 해석해야 합니다.", icon="💡")
    
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
    st.markdown("**관성력 (Inertial force) / 표면장력 (Surface tension force)**")
    st.latex(r"We = \frac{\rho V^2 L}{\sigma}")
    st.info("💡 **이론적 의미:** 서로 섞이지 않는 다상 유동(Multiphase flow)에서 표면장력의 영향을 평가할 때 사용됩니다. 스프레이 노즐 분사 시 액적이 어떻게 분열되는지, 또는 얇은 막(Film) 유동이 어떻게 형성되는지를 해석할 때 중요합니다.", icon="💡")
    
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
    st.markdown("**압력차 (Pressure force) / 관성력 (Inertial force)**")
    st.latex(r"Eu = \frac{\Delta p}{\rho V^2}")
    st.info("💡 **이론적 의미:** 펌프, 송풍기, 밸브 및 배관망 등에서 발생하는 유체 저항이나 압력 분포의 상사성을 평가할 때 쓰입니다. 손실 계수(Loss coefficient)와 직접적으로 연관되어 시스템의 압력 강하를 산정하는 데 활용됩니다.", icon="💡")
    
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
    st.info("💡 **이론적 의미:** 유체의 흐름(유동)으로 인해 고체 표면에서의 열전달이 단순히 전도만 일어날 때보다 얼마나 촉진되는지를 나타내는 지표입니다. 열교환기나 방열판 설계 시, 대류 열전달 계수(h)를 구하기 위한 핵심 파라미터입니다.", icon="💡")
    
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
    st.markdown("**부력 (Buoyancy force) / 점성력 (Viscous force)**")
    st.latex(r"Gr = \frac{g \beta (T_s - T_\infty) L^3}{\nu^2}")
    st.info("💡 **이론적 의미:** 펌프 등의 외부 동력 없이, 유체 내부의 온도차로 인한 밀도 변화가 만들어내는 '자연 대류(Natural convection)'에서 강제 대류의 레이놀즈 수(Re)와 같은 역할을 합니다.", icon="💡")
    
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
    st.info("💡 **이론적 의미:** 유체의 흐름 자체에 의해 열(또는 물질)이 전달되는 속도와 분자 단위의 확산에 의해 전달되는 속도의 비입니다. 유속이 빠를수록 Pe가 커지며, 열전달 현상에서 이류(Advection)가 지배적이게 됩니다.", icon="💡")
    
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
    st.markdown("**운동량 확산 (Momentum diffusivity) / 질량 확산 (Mass diffusivity)**")
    st.latex(r"Sc = \frac{\nu}{D_m} = \frac{\mu}{\rho D_m}")
    st.info("💡 **이론적 의미:** 물질 전달(Mass transfer) 공정에서 유속에 의한 속도 경계층과 농도 차이에 의한 농도 경계층의 상대적인 두께를 나타냅니다. 열전달 현상에서의 프란틀 수(Pr)와 완전히 상응하는 화공 특화 무차원 수입니다.", icon="💡")
    
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
    st.markdown("**진동 관성력 (Oscillation inertial force) / 평균 관성력 (Mean inertial force)**")
    st.latex(r"St = \frac{f L}{V}")
    st.info("💡 **이론적 의미:** 굴뚝이나 원통 기둥 뒤에서 발생하는 카르만 와류(Karman vortex) 방출 등, 유동이 주기적으로 진동하는 비정상(Unsteady) 현상을 예측하고 구조물의 공진 여부를 평가할 때 필수적인 지표입니다.", icon="💡")
    
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
