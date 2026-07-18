import streamlit as st
import math

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | Fluid Mechanics", page_icon="🌊", layout="centered")

st.title("유체역학 기초 계산 (Fluid Mechanics)")
st.markdown("배관 유동 설계 및 CFD 해석 셋업 전, 유동 특성을 빠르게 파악하기 위한 기초 계산기입니다.")
st.divider()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["레이놀즈 수 (Reynolds No.)", "배관 압력 강하 (Pressure Drop)", "오리피스 유량 (Orifice Flow)"])

# ---------------------------------------------------------
# Tab 1: 레이놀즈 수 (Reynolds Number)
# ---------------------------------------------------------
with tab1:
    st.subheader("레이놀즈 수 (Reynolds Number)")
    st.markdown("유동이 층류(Laminar)인지 난류(Turbulent)인지 판별합니다.")
    st.latex(r"Re = \frac{\rho V D}{\mu}")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("유체 밀도, ρ (kg/m³)", value=1000.0, step=10.0, key="re_rho")
        vel = st.number_input("유속, V (m/s)", value=2.0, step=0.1, key="re_vel")
    with col2:
        dia = st.number_input("특성 길이 또는 직경, D (m)", value=0.1, step=0.01, key="re_dia")
        mu = st.number_input("점성계수, μ (Pa·s)", value=0.001, step=0.0001, format="%f", key="re_mu")
    
    if mu > 0:
        reynolds = (rho * vel * dia) / mu
        st.info("계산 결과")
        st.metric(label="Reynolds Number (Re)", value=f"{reynolds:,.0f}")
        
        if reynolds < 2300:
            st.success("해석: 층류 유동 (Laminar Flow)")
        elif 2300 <= reynolds <= 4000:
            st.warning("해석: 천이 영역 (Transitional Flow)")
        else:
            st.error("해석: 난류 유동 (Turbulent Flow)")
    else:
        st.error("점성계수(μ)는 0보다 커야 합니다.")

# ---------------------------------------------------------
# Tab 2: 배관 압력 강하 (Darcy-Weisbach)
# ---------------------------------------------------------
with tab2:
    st.subheader("다르시-바이스바흐 압력 강하")
    st.markdown("직관 내부 마찰로 인해 발생하는 압력 손실을 계산합니다.")
    st.latex(r"\Delta p = f \frac{L}{D} \frac{\rho V^2}{2}")
    
    col3, col4 = st.columns(2)
    with col3:
        f_factor = st.number_input("마찰 계수, f (Darcy)", value=0.02, step=0.005, format="%f")
        length = st.number_input("배관 길이, L (m)", value=10.0, step=1.0)
        dia_dw = st.number_input("배관 직경, D (m)", value=0.1, step=0.01, key="dw_dia")
    with col4:
        rho_dw = st.number_input("유체 밀도, ρ (kg/m³)", value=1000.0, step=10.0, key="dw_rho")
        vel_dw = st.number_input("유속, V (m/s)", value=2.0, step=0.1, key="dw_vel")
    
    if dia_dw > 0:
        delta_p = f_factor * (length / dia_dw) * (rho_dw * vel_dw**2) / 2
        st.info("계산 결과")
        st.metric(label="압력 강하 (Δp)", value=f"{delta_p:,.2f} Pa")
        st.caption(f"환산: {delta_p / 100000:,.4f} bar / {delta_p / 101325:,.4f} atm")
    else:
        st.error("배관 직경(D)은 0보다 커야 합니다.")

# ---------------------------------------------------------
# Tab 3: 오리피스 질량 유량 (Orifice Mass Flow Rate)
# ---------------------------------------------------------
with tab3:
    st.subheader("오리피스/노즐 질량 유량")
    st.markdown("차압(Δp)을 이용하여 밸브나 오리피스를 통과하는 유량을 산출합니다.")
    st.latex(r"\dot{m} = C_d A \sqrt{2 \rho \Delta p}")
    
    col5, col6 = st.columns(2)
    with col5:
        cd = st.number_input("유량 계수, Cd", value=0.62, step=0.01)
        area_cm2 = st.number_input("개구부 면적, A (cm²)", value=50.0, step=1.0)
        area_m2 = area_cm2 / 10000  # cm2 to m2
    with col6:
        rho_ori = st.number_input("유체 밀도, ρ (kg/m³)", value=1.225, step=0.1, help="기본값: 공기", key="ori_rho")
        dp_pa = st.number_input("차압, Δp (Pa)", value=500.0, step=10.0)
    
    if dp_pa >= 0 and rho_ori > 0:
        mass_flow = cd * area_m2 * math.sqrt(2 * rho_ori * dp_pa)
        st.info("계산 결과")
        st.metric(label="질량 유량 (ṁ)", value=f"{mass_flow:,.3f} kg/s")
        st.caption(f"환산: {mass_flow * 3600:,.1f} kg/h")
    else:
        st.error("차압(Δp)과 밀도(ρ)는 0 이상이어야 합니다.")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
