import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | NOx Calculator", page_icon="⚙️", layout="centered")

# 헤더 영역
st.title("NOx Absolute Mass Calculator")
st.markdown("""
배가스의 유량, 측정 농도(ppm), 그리고 **희석 비율(Dilution Ratio)**을 기반으로 
정확한 절대 질량 흐름($kg/h$)과 표준 상태 환산 농도($mg/Sm^3$)를 계산합니다.
""")

st.divider()

# 레이아웃 분할 (입력부 / 결과부)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 운전 조건 입력 (Inputs)")
    
    flow_rate = st.number_input("배가스 체적 유량 (m³/h)", value=10000.0, step=100.0)
    temp_c = st.number_input("배가스 온도 (°C)", value=150.0, step=10.0)
    pressure_atm = st.number_input("배가스 압력 (atm)", value=1.0, step=0.01)
    
    st.markdown("##### 가스 분석 데이터")
    nox_ppm = st.number_input("NOx 측정 농도 (ppm)", value=50.0, step=1.0)
    dilution_ratio = st.number_input("희석 비율 (Dilution Ratio)", value=1.0, step=0.1, help="희석되지 않은 원 가스 측정 시 1.0 입력")

# 계산 로직 (Core Engine)
def calculate_nox_mass(flow, temp, pres, ppm, dil_ratio):
    R = 0.08206      # L*atm/(mol*K)
    M_NO2 = 46.0055  # g/mol
    
    # 1. Total molar flow (mol/h)
    temp_k = temp + 273.15
    n_dot_total = (pres * flow * 1000) / (R * temp_k)
    
    # 2. Mole fraction with dilution ratio
    y_nox = (ppm * 1e-6) * dil_ratio
    
    # 3. Absolute mass flow (kg/h)
    m_dot_nox_g = n_dot_total * y_nox * M_NO2
    m_dot_nox_kg = m_dot_nox_g / 1000
    
    # 4. Standard Concentration (mg/Sm3 at 0°C, 1atm)
    # 1 mol of ideal gas at STP = 22.414 L
    c_standard = (ppm * dil_ratio) * (M_NO2 / 22.414)
    
    return m_dot_nox_kg, c_standard

# 결과 계산
mass_flow_kg, std_concentration = calculate_nox_mass(
    flow_rate, temp_c, pressure_atm, nox_ppm, dilution_ratio
)

with col2:
    st.subheader("📊 계산 결과 (Results)")
    st.info("실시간 물질 수지 (Mass Balance) 계산 완료")
    
    st.metric(
        label="NOx 절대 질량 유량", 
        value=f"{mass_flow_kg:.3f} kg/h",
        help="주어진 온도/압력 및 희석 비율이 반영된 절대적인 질량입니다."
    )
    
    st.metric(
        label="표준 상태 환산 농도 (STP)", 
        value=f"{std_concentration:.2f} mg/Sm³",
        help="0°C, 1atm 기준의 질량 농도입니다."
    )
    
st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
