import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="EngiMate | Unit Converter", page_icon="🔄", layout="centered")

# 헤더 영역
st.title("통합 공학 단위 변환기")
st.markdown("기계, 화공, 플랜트 설계 등 다양한 공학 도메인에서 교차 사용되는 단위들을 빠르고 정확하게 변환합니다.")
st.divider()

# 변환 계수 딕셔너리 (각 카테고리의 기준 단위(Value=1.0)를 바탕으로 환산)
conversion_factors = {
    "길이 (Length)": {
        "m (미터)": 1.0, 
        "cm (센티미터)": 0.01, 
        "mm (밀리미터)": 0.001, 
        "um (마이크로미터)": 1e-6,
        "km (킬로미터)": 1000.0, 
        "inch (인치)": 0.0254, 
        "ft (피트)": 0.3048, 
        "yard (야드)": 0.9144, 
        "mile (마일)": 1609.344
    },
    "압력 (Pressure)": {
        "Pa (파스칼)": 1.0, 
        "kPa (킬로파스칼)": 1000.0, 
        "MPa (메가파스칼)": 1000000.0,
        "bar (바)": 100000.0, 
        "atm (기압)": 101325.0, 
        "psi (파운드/제곱인치)": 6894.757,
        "mmHg (수은주밀리미터)": 133.3224, 
        "mmH2O (수주밀리미터)": 9.80665
    },
    "부피 (Volume)": {
        "m³ (입방미터)": 1.0, 
        "cm³ / cc": 1e-6, 
        "L (리터)": 0.001, 
        "mL (밀리리터)": 1e-6,
        "gal (미국 갤런)": 0.00378541, 
        "bbl (배럴)": 0.158987
    },
    "질량 (Mass)": {
        "kg (킬로그램)": 1.0, 
        "g (그램)": 0.001, 
        "mg (밀리그램)": 1e-6,
        "ton (미터톤)": 1000.0, 
        "lb (파운드)": 0.453592, 
        "oz (온스)": 0.0283495
    },
    "에너지 (Energy)": {
        "J (줄)": 1.0, 
        "kJ (킬로줄)": 1000.0, 
        "MJ (메가줄)": 1000000.0,
        "cal (칼로리)": 4.184, 
        "kcal (킬로칼로리)": 4184.0,
        "Wh (와트시)": 3600.0, 
        "kWh (킬로와트시)": 3600000.0,
        "BTU (영국열량단위)": 1055.06
    }
}

# 카테고리 선택
category = st.selectbox("측정 물리량 카테고리를 선택하세요", list(conversion_factors.keys()) + ["온도 (Temperature)"])

st.write("") # 여백

# UI 레이아웃 분할
col1, col2, col3 = st.columns([2, 1, 2])

# 일반 물리량 변환 로직 (온도 제외)
if category != "온도 (Temperature)":
    units = list(conversion_factors[category].keys())
    
    with col1:
        from_unit = st.selectbox("변환 전 단위 (From)", units, key="from_unit")
        from_value = st.number_input("입력값", value=1.0, format="%f")
        
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
        from_value = st.number_input("입력값", value=0.0, format="%f")
        
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
