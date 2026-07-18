markdown_content = """# EngiMate Module 1: NOx Absolute Mass & Emission Calculator

## 1. 지배 방정식 및 물리적 근거 (Mathematical Formulation)

스크러버(Scrubber) 및 SCR 환경 설비 설계 시, 단순 측정 농도(ppm)만으로는 설비의 정확한 효율을 평가할 수 없습니다. 배가스의 유량과 몰 분율(Mole fraction), 그리고 샘플링 측정 시 개입되는 **희석 비율(Dilution ratio)**을 명확히 고려하여, 유체 내 대상 물질의 **절대적인 질량 흐름(Absolute Mass Flow)**을 산출하는 것이 필수적입니다.

### Step 1: 배가스 총 몰 유량 계산 (Total Molar Flow Rate)
이상기체 상태방정식($PV=nRT$)을 이용하여 현재 온도와 압력 조건에서의 총 가스 몰 유량을 산출합니다.
*   $\\dot{n}_{total} = \\frac{P \\cdot Q \\cdot 1000}{R \\cdot (T + 273.15)}$
    *   $P$: 배가스 압력 ($atm$)
    *   $Q$: 배가스 체적 유량 ($m^3/h$)
    *   $R$: 기체 상수 ($0.08206 \\, L \\cdot atm / (mol \\cdot K)$)
    *   $T$: 배가스 온도 ($\\circ C$)

### Step 2: 몰 분율 및 희석 비율 적용 (Mole Fraction with Dilution Ratio)
측정된 ppm 농도에 희석 비율을 곱하여 실제 배관 내의 정확한 몰 분율을 구합니다.
*   $y_{NOx} = C_{ppm} \\times 10^{-6} \\times D_R$
    *   $C_{ppm}$: 측정된 NOx 농도
    *   $D_R$: 희석 비율 (Dilution Ratio)

### Step 3: 절대 질량 유량 산출 (Absolute Mass Flow)
*   $\\dot{m}_{NOx} = \\dot{n}_{total} \\times y_{NOx} \\times M_{NOx}$
    *   $M_{NOx}$: NOx 분자량 (대기환경보전법 등 규제 기준에 따라 통상 $NO_2$ 기준 $46.0055 \\, g/mol$ 적용)

---

## 2. Streamlit 웹 애플리케이션 소스 코드 (`app.py`)

아래의 파이썬 코드를 복사하여 GitHub 저장소에 `app.py`라는 이름으로 저장하시면 됩니다.

```python
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | NOx Calculator", page_icon="⚙️", layout="centered")

# 헤더 영역
st.title("NOx Absolute Mass Calculator")
st.markdown(\"""
배가스의 유량, 측정 농도(ppm), 그리고 **희석 비율(Dilution Ratio)**을 기반으로 
정확한 절대 질량 흐름($kg/h$)과 표준 상태 환산 농도($mg/Sm^3$)를 계산합니다.
\""")

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
