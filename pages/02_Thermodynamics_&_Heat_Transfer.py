import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Thermo & Heat Transfer", page_icon="🔥", layout="centered")

st.title("🔥 열역학 및 열전달 계산기")
st.markdown("기계공학 기초 열역학 공식 및 열전달(전도, 대류, 복사) 시스템 설계용 계산 툴셋입니다.")
st.divider()

# 10종 계산기 메뉴 선택
calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 이상기체 상태방정식 (Ideal Gas Law)",
    "2. 1차원 평판 열전도 (Fourier's Law)",
    "3. 대류 열전달 (Newton's Law of Cooling)",
    "4. 단일 평판의 열관류율 (U-value)",
    "5. 대수평균온도차 (LMTD)",
    "6. 열교환기 유용도 (NTU-Effectiveness)",
    "7. 카르노 사이클 최대 효율 (Carnot Efficiency)",
    "8. 스테판-볼츠만 복사 열전달 (Radiation)",
    "9. 현열 및 잠열 계산 (Sensible & Latent Heat)",
    "10. 단열재 임계 반경 (Critical Radius of Insulation)"
])

st.write("---")

# ---------------------------------------------------------
# 1. 이상기체 상태방정식 (Ideal Gas Law)
# ---------------------------------------------------------
if "이상기체" in calc_menu:
    st.subheader("1. 이상기체 상태방정식 (PV = nRT)")
    st.markdown("네 가지 변수(P, V, n, T) 중 하나를 미지수로 두고 나머지 값을 통해 계산합니다.")
    
    target = st.radio("계산할 미지수 선택:", ["압력 (P)", "부피 (V)", "몰수 (n)", "온도 (T)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    R = 0.08206 # L·atm/(mol·K)
    
    with col1:
        if "P" not in target:
            P = st.number_input("압력, P (atm)", value=1.0, format="%g")
        if "V" not in target:
            V = st.number_input("부피, V (L)", value=22.4, format="%g")
    with col2:
        if "n" not in target:
            n = st.number_input("몰수, n (mol)", value=1.0, format="%g")
        if "T" not in target:
            T = st.number_input("온도, T (K)", value=273.15, format="%g")
            
    if st.button("계산하기"):
        st.success("계산 결과:")
        if "P" in target:
            result = (n * R * T) / V
            st.metric("압력 (P)", f"{result:.4g} atm")
        elif "V" in target:
            result = (n * R * T) / P
            st.metric("부피 (V)", f"{result:.4g} L")
        elif "n" in target:
            result = (P * V) / (R * T)
            st.metric("몰수 (n)", f"{result:.4g} mol")
        elif "T" in target:
            result = (P * V) / (n * R)
            st.metric("온도 (T)", f"{result:.4g} K")

# ---------------------------------------------------------
# 2. 1차원 평판 열전도 (Fourier's Law)
# ---------------------------------------------------------
elif "열전도" in calc_menu:
    st.subheader("2. 1차원 평판 열전도 (Fourier's Law)")
    st.latex(r"q = k A \frac{\Delta T}{L}")
    
    col1, col2 = st.columns(2)
    with col1:
        k = st.number_input("열전도도, k (W/m·K)", value=0.04) # 단열재 수준
        A = st.number_input("단면적, A (m²)", value=1.0)
    with col2:
        dT = st.number_input("온도차, ΔT (K 또는 °C)", value=50.0)
        L = st.number_input("두께, L (m)", value=0.1)
        
    if L > 0:
        q = (k * A * dT) / L
        st.info(f"**열전달률 (q): {q:,.2f} W**")

# ---------------------------------------------------------
# 3. 대류 열전달 (Newton's Law of Cooling)
# ---------------------------------------------------------
elif "대류 열전달" in calc_menu:
    st.subheader("3. 대류 열전달 (Newton's Law of Cooling)")
    st.latex(r"q = h A (T_s - T_\infty)")
    
    col1, col2 = st.columns(2)
    with col1:
        h = st.number_input("대류 열전달 계수, h (W/m²·K)", value=10.0)
        A = st.number_input("표면적, A (m²)", value=2.0)
    with col2:
        Ts = st.number_input("표면 온도, T_s (°C)", value=80.0)
        Tf = st.number_input("유체 온도, T_∞ (°C)", value=20.0)
        
    q = h * A * (abs(Ts - Tf))
    st.info(f"**대류 열전달률 (q): {q:,.2f} W**")

# ---------------------------------------------------------
# 4. 단일 평판의 열관류율 (U-value)
# ---------------------------------------------------------
elif "열관류율" in calc_menu:
    st.subheader("4. 단일 평판의 열관류율 (U-value)")
    st.markdown("내/외부 대류와 벽면 전도를 모두 고려한 총괄 열전달 계수입니다.")
    st.latex(r"\frac{1}{U} = \frac{1}{h_{in}} + \frac{L}{k} + \frac{1}{h_{out}}")
    
    col1, col2 = st.columns(2)
    with col1:
        h_in = st.number_input("내부 대류계수, h_in (W/m²·K)", value=10.0)
        h_out = st.number_input("외부 대류계수, h_out (W/m²·K)", value=25.0)
    with col2:
        k = st.number_input("벽면 열전도도, k (W/m·K)", value=1.5)
        L = st.number_input("벽면 두께, L (m)", value=0.2)
        
    if h_in > 0 and h_out > 0 and k > 0:
        R_total = (1/h_in) + (L/k) + (1/h_out)
        U = 1 / R_total
        st.info(f"**총 열저항 (R_total): {R_total:.4f} m²·K/W**")
        st.success(f"**열관류율 (U): {U:,.3f} W/m²·K**")

# ---------------------------------------------------------
# 5. 대수평균온도차 (LMTD)
# ---------------------------------------------------------
elif "LMTD" in calc_menu:
    st.subheader("5. 대수평균온도차 (LMTD)")
    st.markdown("열교환기(병류/향류) 양단의 온도차를 바탕으로 유효 온도차를 산출합니다.")
    
    flow_type = st.radio("유동 방식:", ["향류 (Counter-flow)", "병류 (Parallel-flow)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**고온 유체 (Hot Fluid)**")
        Thi = st.number_input("입구 온도, T_h,in (°C)", value=100.0)
        Tho = st.number_input("출구 온도, T_h,out (°C)", value=60.0)
    with col2:
        st.markdown("**저온 유체 (Cold Fluid)**")
        Tci = st.number_input("입구 온도, T_c,in (°C)", value=20.0)
        Tco = st.number_input("출구 온도, T_c,out (°C)", value=40.0)
        
    if flow_type == "향류 (Counter-flow)":
        dT1 = Thi - Tco
        dT2 = Tho - Tci
    else:
        dT1 = Thi - Tci
        dT2 = Tho - Tco
        
    if dT1 == dT2 and dT1 > 0:
        LMTD = dT1
        st.info(f"**LMTD: {LMTD:.2f} °C** (ΔT1 = ΔT2 인 경우 산술평균과 동일)")
    elif dT1 <= 0 or dT2 <= 0:
        st.error("온도 교차 발생: 입력 온도를 확인하세요. (ΔT1, ΔT2는 0보다 커야 합니다.)")
    else:
        LMTD = (dT1 - dT2) / math.log(dT1 / dT2)
        st.success(f"**LMTD: {LMTD:.2f} °C**")

# ---------------------------------------------------------
# 6. 열교환기 유용도 (NTU-Effectiveness)
# ---------------------------------------------------------
elif "NTU" in calc_menu:
    st.subheader("6. 열교환기 유용도 (NTU-Effectiveness, ε)")
    st.markdown("단순 향류(Counter-flow) 열교환기를 가정한 NTU 및 유용도 계산입니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        C_min = st.number_input("최소 열용량율, C_min (W/K)", value=1000.0)
        C_max = st.number_input("최대 열용량율, C_max (W/K)", value=2000.0)
    with col2:
        U = st.number_input("총괄 열전달계수, U (W/m²·K)", value=150.0)
        A = st.number_input("전열 면적, A (m²)", value=10.0)
        
    if C_min > 0 and C_max > 0:
        C_r = C_min / C_max
        NTU = (U * A) / C_min
        
        if C_r == 1:
            effectiveness = NTU / (1 + NTU)
        else:
            exp_term = math.exp(-NTU * (1 - C_r))
            effectiveness = (1 - exp_term) / (1 - C_r * exp_term)
            
        st.info(f"**용량비 (Cr): {C_r:.3f} | 전달단수 (NTU): {NTU:.3f}**")
        st.success(f"**유용도 (ε): {effectiveness:.2%}**")

# ---------------------------------------------------------
# 7. 카르노 사이클 최대 효율 (Carnot Efficiency)
# ---------------------------------------------------------
elif "카르노" in calc_menu:
    st.subheader("7. 카르노 사이클 이론 최대 효율")
    st.latex(r"\eta_{th} = 1 - \frac{T_L}{T_H}")
    
    col1, col2 = st.columns(2)
    with col1:
        T_H = st.number_input("고열원 온도, T_H (°C)", value=500.0)
    with col2:
        T_L = st.number_input("저열원 온도, T_L (°C)", value=25.0)
        
    Th_K = T_H + 273.15
    Tl_K = T_L + 273.15
    
    if Th_K > Tl_K:
        eff = 1 - (Tl_K / Th_K)
        st.success(f"**이론적 최대 열효율: {eff:.2%}**")
    else:
        st.error("고열원 온도가 저열원 온도보다 높아야 합니다.")

# ---------------------------------------------------------
# 8. 스테판-볼츠만 복사 열전달 (Radiation)
# ---------------------------------------------------------
elif "복사" in calc_menu:
    st.subheader("8. 스테판-볼츠만 복사 열전달")
    st.markdown("표면 방사율(ε)을 고려한 흑체 또는 회체 표면의 복사 에너지 방출량입니다.")
    st.latex(r"q = \epsilon \sigma A (T_s^4 - T_{surr}^4)")
    
    sigma = 5.67e-8 # W/m2K4
    
    col1, col2 = st.columns(2)
    with col1:
        epsilon = st.number_input("방사율, ε (0~1)", value=0.9, max_value=1.0)
        A = st.number_input("표면적, A (m²)", value=1.0, key="rad_a")
    with col2:
        Ts = st.number_input("표면 온도, T_s (°C)", value=300.0)
        Tsurr = st.number_input("주위 온도, T_surr (°C)", value=20.0)
        
    Ts_K = Ts + 273.15
    Tsurr_K = Tsurr + 273.15
    
    q_rad = epsilon * sigma * A * abs(Ts_K**4 - Tsurr_K**4)
    st.info(f"**순 복사 열전달량 (q): {q_rad:,.2f} W**")

# ---------------------------------------------------------
# 9. 현열 및 잠열 계산 (Sensible & Latent Heat)
# ---------------------------------------------------------
elif "현열 및 잠열" in calc_menu:
    st.subheader("9. 현열 및 잠열 (Sensible & Latent Heat)")
    st.markdown("온도 변화에 필요한 현열($Q = mc\Delta T$) 또는 상변화에 필요한 잠열($Q = m L_v$)을 계산합니다.")
    
    heat_type = st.radio("계산 유형:", ["현열 (온도 변화)", "잠열 (상변화)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("질량, m (kg)", value=10.0)
        
    with col2:
        if heat_type == "현열 (온도 변화)":
            c = st.number_input("비열, c (kJ/kg·K)", value=4.18) # 물 기준
            dT = st.number_input("온도 변화, ΔT (K 또는 °C)", value=50.0)
            Q = m * c * dT
            st.success(f"**필요 열량 (현열): {Q:,.2f} kJ**")
        else:
            L_v = st.number_input("잠열, L_v (kJ/kg)", value=2257.0) # 물 증발잠열 기준
            Q = m * L_v
            st.success(f"**필요 열량 (잠열): {Q:,.2f} kJ**")

# ---------------------------------------------------------
# 10. 단열재 임계 반경 (Critical Radius of Insulation)
# ---------------------------------------------------------
elif "임계 반경" in calc_menu:
    st.subheader("10. 원통형 배관의 단열재 임계 반경")
    st.markdown("단열재를 덮을 때 오히려 열손실이 최대가 되는 반경입니다. 이보다 작을 경우 단열재 두께를 늘려도 열이 더 많이 방출됩니다.")
    st.latex(r"r_{cr} = \frac{k_{ins}}{h_{out}}")
    
    col1, col2 = st.columns(2)
    with col1:
        k_ins = st.number_input("단열재 열전도도, k (W/m·K)", value=0.04)
    with col2:
        h_out = st.number_input("외부 대류 열전달계수, h (W/m²·K)", value=5.0)
        
    if h_out > 0:
        r_cr = k_ins / h_out
        st.info(f"**임계 반경 (r_cr): {r_cr:.4f} m ({r_cr*1000:.1f} mm)**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Process Engineers")
