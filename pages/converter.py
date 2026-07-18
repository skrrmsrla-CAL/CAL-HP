import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | Unit Converter", page_icon="🔄", layout="centered")

# 헤더 영역
st.title("통합 공학 단위 변환기 (Pro Max)")
st.markdown("기계, 화공, 플랜트, 전기전자 및 전통 단위를 아우르는 마스터 공학 변환기입니다.")
st.divider()

# 변환 계수 딕셔너리 (각 카테고리의 기준 단위(Value=1.0)를 바탕으로 환산)
conversion_factors = {
    "길이 (Length)": {
        "m (미터)": 1.0, "cm (센티미터)": 0.01, "mm (밀리미터)": 0.001, "um (마이크로미터)": 1e-6,
        "km (킬로미터)": 1000.0, "inch (인치)": 0.0254, "ft (피트)": 0.3048, "yard (야드)": 0.9144, "mile (마일)": 1609.344,
        "해리 (Nautical mile)": 1852.0, "자 (尺)": 0.3030303, "간 (間)": 1.8181818, "정 (町)": 109.0909, "리 (里)": 392.7273
    },
    "넓이 (Area)": {
        "m² (제곱미터)": 1.0, "cm² (제곱센티미터)": 1e-4, "km² (제곱킬로미터)": 1e6,
        "a (아르)": 100.0, "ha (헥타르)": 10000.0, "평 (坪)": 3.305785,
        "sq ft (제곱피트)": 0.092903, "acre (에이커)": 4046.856
    },
    "부피 (Volume)": {
        "m³ (입방미터)": 1.0, "cm³ / cc": 1e-6, "L (리터)": 0.001, "mL (밀리리터)": 1e-6,
        "gal (미국 갤런)": 0.00378541, "bbl (배럴)": 0.158987
    },
    "시간 (Time)": {
        "s (초)": 1.0, "min (분)": 60.0, "h (시간)": 3600.0, "day (일)": 86400.0
    },
    "속도 (Velocity)": {
        "m/s (미터/초)": 1.0, "km/h (킬로미터/시)": 0.2777778, "mph (마일/시)": 0.44704,
        "knot (노트)": 0.514444, "ft/s (피트/초)": 0.3048
    },
    "가속도 (Acceleration)": {
        "m/s²": 1.0, "G (중력가속도)": 9.80665, "ft/s²": 0.3048, "Gal (갈)": 0.01
    },
    "각속도 (Angular Velocity)": {
        "rad/s": 1.0, "RPM": 0.104719755, "deg/s": 0.01745329
    },
    "질량 (Mass)": {
        "kg (킬로그램)": 1.0, "g (그램)": 0.001, "mg (밀리그램)": 1e-6,
        "ton (미터톤)": 1000.0, "lb (파운드)": 0.453592, "oz (온스)": 0.0283495
    },
    "질량유량 (Mass Flow Rate)": {
        "kg/s": 1.0, "kg/h": 0.000277778, "lb/s": 0.453592, "lb/h": 0.000125998
    },
    "체적유량 (Volumetric Flow Rate)": {
        "m³/s": 1.0, "m³/h": 0.000277778, "L/min (LPM)": 1.66667e-5, "ft³/min (CFM)": 0.000471947, "gal/min (GPM)": 6.30902e-5
    },
    "몰유량 (Molar Flow Rate)": {
        "mol/s": 1.0, "kmol/h": 0.277778, "lb-mol/h": 0.125998
    },
    "밀도 (Density)": {
        "kg/m³": 1.0, "g/cm³": 1000.0, "lb/ft³": 16.01846
    },
    "비체적 (Specific Volume)": {
        "m³/kg": 1.0, "L/kg": 0.001, "ft³/lb": 0.062428
    },
    "비중량 (Specific Weight)": {
        "N/m³": 1.0, "kgf/m³": 9.80665, "lbf/ft³": 157.087
    },
    "몰농도 (Molarity)": {
        "mol/L (M)": 1.0, "mmol/L": 0.001, "kmol/m³": 1.0
    },
    "힘 (Force)": {
        "N (뉴턴)": 1.0, "kN (킬로뉴턴)": 1000.0, "kgf (킬로그램힘)": 9.80665,
        "lbf (파운드힘)": 4.44822, "dyn (다인)": 1e-5
    },
    "압력 및 진공압 (Pressure & Vacuum)": {
        "Pa (파스칼)": 1.0, "kPa (킬로파스칼)": 1000.0, "MPa (메가파스칼)": 1000000.0,
        "bar (바)": 100000.0, "atm (기압)": 101325.0, "psi (파운드/제곱인치)": 6894.757,
        "mmHg (수은주밀리미터)": 133.3224, "mmH2O (수주밀리미터)": 9.80665,
        "Torr (토르)": 133.3224, "inHg (수은주인치)": 3386.389
    },
    "응력 및 탄성계수 (Stress & Modulus)": {
        "MPa": 1.0, "Pa": 1e-6, "GPa": 1000.0, "kgf/mm²": 9.80665, "psi": 0.00689476, "ksi": 6.89476
    },
    "토크 (Torque)": {
        "N·m": 1.0, "kgf·m": 9.80665, "lbf·ft": 1.355818
    },
    "에너지 및 엔탈피 (Energy & Enthalpy)": {
        "J (줄)": 1.0, "kJ (킬로줄)": 1000.0, "MJ (메가줄)": 1000000.0,
        "cal (칼로리)": 4.184, "kcal (킬로칼로리)": 4184.0,
        "Wh (와트시)": 3600.0, "kWh (킬로와트시)": 3600000.0,
        "BTU (영국열량단위)": 1055.06, "kJ/kg (비엔탈피)": 1000.0, "kcal/kg": 4184.0
    },
    "동력 (Power)": {
        "W (와트)": 1.0, "kW (킬로와트)": 1000.0, "HP (마력)": 745.699872, "PS (미터마력)": 735.49875
    },
    "비열 및 엔트로피 (Specific Heat & Entropy)": {
        "J/(kg·K)": 1.0, "kJ/(kg·K)": 1000.0, "kcal/(kg·°C)": 4184.0, "BTU/(lb·°F)": 4184.0
    },
    "열전도도 (Thermal Conductivity)": {
        "W/(m·K)": 1.0, "kcal/(h·m·°C)": 1.16222, "BTU/(h·ft·°F)": 1.73073
    },
    "열전달계수 (Heat Transfer Coefficient)": {
        "W/(m²·K)": 1.0, "kcal/(h·m²·°C)": 1.16222, "BTU/(h·ft²·°F)": 5.67826
    },
    "표면장력 (Surface Tension)": {
        "N/m": 1.0, "mN/m": 0.001, "dyn/cm": 0.001
    },
    "점성계수 (Dynamic Viscosity)": {
        "Pa·s": 1.0, "P (포아즈)": 0.1, "cP (센티포아즈)": 0.001
    },
    "동점성/확산계수 (Kinematic Visc. & Diffusion)": {
        "m²/s": 1.0, "cm²/s": 1e-4, "St (스토크스)": 1e-4, "cSt (센티스토크스)": 1e-6
    },
    "단면 2차 모멘트 (Area Moment of Inertia)": {
        "m⁴": 1.0, "cm⁴": 1e-8, "mm⁴": 1e-12, "in⁴": 4.16231e-7
    },
    "질량 관성 모멘트 (Mass Moment of Inertia)": {
        "kg·m²": 1.0, "g·cm²": 1e-7, "lb·ft²": 0.0421401
    },
    "전류 (Electric Current)": {
        "A (암페어)": 1.0, "mA (밀리암페어)": 0.001, "uA (마이크로암페어)": 1e-6
    },
    "전압 (Voltage)": {
        "V (볼트)": 1.0, "kV (킬로볼트)": 1000.0, "mV (밀리볼트)": 0.001
    },
    "전하량 (Electric Charge)": {
        "C (쿨롬)": 1.0, "mC (밀리쿨롬)": 0.001, "uC (마이크로쿨롬)": 1e-6, "Ah (암페어시)": 3600.0
    },
    "정전용량 (Capacitance)": {
        "F (패럿)": 1.0, "mF (밀리패럿)": 0.001, "uF (마이크로패럿)": 1e-6, "nF (나노패럿)": 1e-9, "pF (피코패럿)": 1e-12
    },
    "인덕턴스 (Inductance)": {
        "H (헨리)": 1.0, "mH (밀리헨리)": 0.001, "uH (마이크로헨리)": 1e-6
    },
    "자기장 (Magnetic Field)": {
        "T (테슬라)": 1.0, "G (가우스)": 1e-4
    },
    "자속 (Magnetic Flux)": {
        "Wb (웨버)": 1.0, "Mx (맥스웰)": 1e-8
    },
    "조도 (Illuminance)": {
        "lx (룩스)": 1.0, "fc (풋캔들)": 10.7639
    },
    "휘도 (Luminance)": {
        "cd/m²": 1.0, "fL (풋램버트)": 3.426259
    }
}

# 카테고리 선택 (온도 포함)
category_list = list(conversion_factors.keys()) + ["온도 (Temperature)"]
category = st.selectbox("측정 물리량 카테고리를 선택하세요", category_list)

st.write("") # 여백

# UI 레이아웃 분할
col1, col2, col3 = st.columns([2, 1, 2])

# 일반 물리량 변환 로직 (온도 제외)
if category != "온도 (Temperature)":
    units = list(conversion_factors[category].keys())
    
    with col1:
        from_unit = st.selectbox("변환 전 단위 (From)", units, key="from_unit")
        from_value = st.number_input("입력값", value=1.0, format="%g")
        
    with col3:
        to_unit = st.selectbox("변환 후 단위 (To)", units, key="to_unit")
        
        # 계산: (입력값 * 변환전 기준계수) / 변환후 기준계수
        base_value = from_value * conversion_factors[category][from_unit]
        result_value = base_value / conversion_factors[category][to_unit]
        
        st.text_input("결과값", value=f"{result_value:g}", disabled=True)

# 온도 특수 변환 로직 (오프셋 적용)
else:
    units = ["°C (섭씨)", "°F (화씨)", "K (켈빈)"]
    
    with col1:
        from_unit = st.selectbox("변환 전 단위 (From)", units, key="from_temp")
        from_value = st.number_input("입력값", value=0.0, format="%g")
        
    with col3:
        to_unit = st.selectbox("변환 후 단위 (To)", units, key="to_temp")
        
        # 우선 섭씨(C)로 모두 변환
        if from_unit == "°C (섭씨)":
            celsius = from_value
        elif from_unit == "°F (화씨)":
            celsius = (from_value - 32) * 5.0 / 9.0
        elif from_unit == "K (켈빈)":
            celsius = from_value - 273.15
            
        # 섭씨(C)에서 타겟 단위로 변환
        if to_unit == "°C (섭씨)":
            result_value = celsius
        elif to_unit == "°F (화씨)":
            result_value = (celsius * 9.0 / 5.0) + 32
        elif to_unit == "K (켈빈)":
            result_value = celsius + 273.15
            
        st.text_input("결과값", value=f"{result_value:g}", disabled=True)

with col2:
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>=</h2>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
