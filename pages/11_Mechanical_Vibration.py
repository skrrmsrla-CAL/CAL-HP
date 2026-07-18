import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Vibration", page_icon="🔊", layout="wide")

st.title("🔊 기계진동 통합 계산기")
st.markdown("구조물의 공진 설계, 회전기계 진동 절연, 진동 진폭 및 주파수 분석용 10대 핵심 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 1자유도 감쇠 진동수 (Damped Natural Frequency)",
    "2. 대수 감쇠율 및 감쇠비 (Logarithmic Decrement)",
    "3. 조화 가전력에 의한 정적/동적 확대율 (Magnification Factor)",
    "4. 진동 절연율 및 투과율 (Transmissibility)",
    "5. 회전 불평형 힘 (Rotational Unbalance Force)",
    "6. 진동 감쇠 오버슈트(%) 기반 감쇠비 역산",
    "7. 변위-속도-가속도 진폭 상호 변환",
    "8. 베어링 결함 주파수 (BPFI, BPFO, BSF, FTF)",
    "9. 비틀림 진동 고유진동수 (Torsional Vibration)",
    "10. 다자유도(2-DOF) 모드 해석 강성 행렬 기초"
])

st.write("---")

# 1. 감쇠 고유 진동수
if "감쇠 진동수" in calc_menu:
    st.subheader("1. 1자유도 감쇠 고유 진동수")
    st.latex(r"f_d = f_n \sqrt{1 - \zeta^2}")
    
    col1, col2 = st.columns(2)
    with col1:
        m = st.number_input("질량, m (kg)", value=10.0)
        k = st.number_input("강성, k (N/m)", value=40000.0)
    with col2:
        zeta = st.number_input("감쇠비, ζ (0 ~ 1)", value=0.05, min_value=0.0, max_value=0.99, format="%f")
        
    if m > 0 and k > 0:
        wn = math.sqrt(k / m)
        fn = wn / (2 * math.pi)
        fd = fn * math.sqrt(1 - zeta**2)
        st.info(f"비감쇠 고유진동수 (fn): **{fn:.2f} Hz**")
        st.success(f"감쇠 고유진동수 (fd): **{fd:.2f} Hz**")

# 2. 대수 감쇠율 및 감쇠비
elif "대수 감쇠율" in calc_menu:
    st.subheader("2. 대수 감쇠율(δ)을 이용한 감쇠비(ζ) 산출")
    st.markdown("자유진동 실험에서 인접한 두 진폭($X_1, X_2$)을 측정하여 시스템의 감쇠 특성을 파악합니다.")
    st.latex(r"\delta = \ln\left(\frac{X_1}{X_2}\right) = \frac{2\pi\zeta}{\sqrt{1-\zeta^2}}")
    
    col1, col2 = st.columns(2)
    with col1:
        x1 = st.number_input("첫 번째 피크 진폭, X1", value=10.0)
    with col2:
        x2 = st.number_input("다음 주기 피크 진폭, X2", value=7.0)
        
    if x1 > 0 and x2 > 0 and x1 > x2:
        delta = math.log(x1 / x2)
        zeta = delta / math.sqrt(4 * math.pi**2 + delta**2)
        st.info(f"대수 감쇠율 (δ): **{delta:.4f}**")
        st.success(f"산출된 시스템 감쇠비 (ζ): **{zeta:.4f}**")
    else:
        st.error("X1은 X2보다 커야 전형적인 감쇠 거동 계산이 가능합니다.")

# 3. 정적/동적 확대율
elif "확대율" in calc_menu:
    st.subheader("3. 조화 가전력에 의한 동적 확대율 (Magnification Factor, M)")
    st.latex(r"M = \frac{1}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}")
    
    col1, col2 = st.columns(2)
    with col1:
        r = st.number_input("진동수비, r (w / wn)", value=0.9, help="가진주파수와 고유진동수의 비")
    with col2:
        zeta = st.number_input("감쇠비, ζ", value=0.05, format="%f")
        
    M = 1 / math.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)
    st.info(f"**동적 응답 확대율 (M): {M:.2f} 배**")
    if 0.9 <= r <= 1.1:
        st.warning("⚠️ 현재 가진 주파수가 고유 진동수에 근접하여 '공진(Resonance)' 위험 영역에 있습니다.")

# 4. 진동 절연율 및 투과율
elif "진동 절연율" in calc_menu:
    st.subheader("4. 진동 투과율(TR) 및 절연율(I)")
    st.markdown("바닥이나 구조물로 전달되는 진동 힘의 비율을 계산합니다.")
    st.latex(r"TR = \sqrt{\frac{1 + (2\zeta r)^2}{(1-r^2)^2 + (2\zeta r)^2}}")
    
    col1, col2 = st.columns(2)
    with col1:
        r = st.number_input("진동수비, r (w / wn)", value=2.5, key="iso_r")
    with col2:
        zeta = st.number_input("감쇠비, ζ", value=0.1, key="iso_zeta")
        
    tr = math.sqrt((1 + (2*zeta*r)**2) / ((1 - r**2)**2 + (2*zeta*r)**2))
    isolation = (1 - tr) * 100
    
    st.info(f"진동 투과율 (TR): **{tr:.4f} ({tr*100:.1f}%)**")
    if r > math.sqrt(2):
        st.success(f"**진동 절연 효과 있음 (절연율: {isolation:.1f}%)**")
    else:
        st.error("❌ 진동수비(r)가 √2보다 작으면 방진패드를 깔았을 때 오히려 진동이 증폭됩니다.")

# 5. 회전 불평형 힘
elif "회전 불평형" in calc_menu:
    st.subheader("5. 회전체 언밸런스에 의한 가진력 (Rotational Unbalance)")
    st.latex(r"F = m_e \cdot e \cdot \omega^2")
    
    col1, col2 = st.columns(2)
    with col1:
        me_g = st.number_input("불평형 질량 (g)", value=5.0)
        e_mm = st.number_input("편심 거리, e (mm)", value=0.1)
    with col2:
        rpm = st.number_input("회전 속도 (RPM)", value=3600.0)
        
    omega = rpm * (2 * math.pi / 60)
    me_kg = me_g / 1000
    e_m = e_mm / 1000
    F_unbalance = me_kg * e_m * omega**2
    
    st.info(f"불평형 크기 (m·e): **{me_g * e_mm:.2f} g·mm**")
    st.success(f"**축계에 가해지는 동적 원심력 (F): {F_unbalance:.2f} N**")

# 6. 오버슈트 기반 감쇠비
elif "오버슈트" in calc_menu:
    st.subheader("6. 스텝 응답 오버슈트(OS%) 기반 감쇠비 계산")
    st.latex(r"\zeta = \frac{-\ln(OS/100)}{\sqrt{\pi^2 + \ln^2(OS/100)}}")
    
    os_pct = st.number_input("과도 응답 최대 오버슈트 비율 (%)", value=15.0, min_value=0.1, max_value=99.9)
    os_val = os_pct / 100
    zeta = -math.log(os_val) / math.sqrt(math.pi**2 + math.log(os_val)**2)
    st.success(f"**역산된 시스템 감쇠비 (ζ): {zeta:.4f}**")

# 7. 변위-속도-가속도 상호 변환
elif "변위-속도-가속도" in calc_menu:
    st.subheader("7. 정현파 진동 주파수별 진폭 변환 (D-V-A)")
    st.markdown("진동 센서 계측 데이터 분석 시 사용되는 필수 수식입니다.")
    st.latex(r"V_0 = \omega D_0, \quad A_0 = \omega^2 D_0")
    
    f = st.number_input("진동 주파수, f (Hz)", value=60.0)
    w = 2 * math.pi * f
    
    type_sel = st.radio("입력 데이터 유형 선택:", ["단일 변위 변폭, D (mm)", "속도 진폭, V (mm/s)", "가속도 진폭, A (m/s²)"], horizontal=True)
    val = st.number_input("입력값", value=0.1, format="%f")
    
    if "변위" in type_sel:
        d_m = val / 1000
        v_ms = w * d_m
        a_ms2 = (w**2) * d_m
    elif "속도" in type_sel:
        v_ms = val / 1000
        d_m = v_ms / w
        a_ms2 = w * v_ms
    else:
        a_ms2 = val
        v_ms = a_ms2 / w
        d_m = a_ms2 / (w**2)
        
    st.info("단일 진폭 환산 결과:")
    st.write(f"- 변위 (Displacement): **{d_m * 1000:.4e} mm**")
    st.write(f"- 속도 (Velocity): **{v_ms * 1000:.4f} mm/s**")
    st.write(f"- 가속도 (Acceleration): **{a_ms2:.4f} m/s² ({a_ms2 / 9.80665:.3f} G)**")

# 8. 베어링 결함 주파수
elif "베어링" in calc_menu:
    st.subheader("8. 구름 베어링 통계적 고장 진단 주파수 (Bearing Fault Frequencies)")
    st.markdown("FFT 진동 스펙트럼에서 결함 신호가 올라오는 위치를 예측합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("볼/롤러 개수, Z", value=9, min_value=1)
        fr = st.number_input("축 회전 주파수, fr (Hz)", value=30.0, help="1800 RPM = 30 Hz")
        d = st.number_input("転動体(볼) 직경, d (mm)", value=8.0)
    with col2:
        D = st.number_input("피치 직경, D (mm)", value=40.0)
        alpha = st.number_input("접촉각, α (도)", value=0.0)
        
    if D > 0:
        cos_a = math.cos(math.radians(alpha))
        bpfo = (n / 2) * fr * (1 - (d / D) * cos_a)
        bpfi = (n / 2) * fr * (1 + (d / D) * cos_a)
        bsf = (D / (2 * d)) * fr * (1 - (d / D)**2 * cos_a**2)
        ftf = 0.5 * fr * (1 - (d / D) * cos_a)
        
        st.info("FFT 매칭용 주요 결함 주파수 산출 결과:")
        st.write(f"- 외륜 결함 주파수 (BPFO): **{bpfo:.2f} Hz**")
        st.write(f"- 내륜 결함 주파수 (BPFI): **{bpfi:.2f} Hz**")
        st.write(f"- 전동체(볼) 결함 주파수 (BSF): **{bsf:.2f} Hz**")
        st.write(f"- 케이지 결함 주파수 (FTF): **{ftf:.2f} Hz**")

# 9. 비틀림 진동 고유진동수
elif "비틀림" in calc_menu:
    st.subheader("9. 축계 비틀림 진동 고유 진동수")
    st.latex(r"f_{nt} = \frac{1}{2\pi} \sqrt{\frac{k_t}{J}}")
    
    col1, col2 = st.columns(2)
    with col1:
        G = st.number_input("전단 탄성계수, G (GPa)", value=80.0)
        dia = st.number_input("축 직경, d (mm)", value=40.0)
        length = st.number_input("축 길이, L (m)", value=1.5)
    with col2:
        J_mass = st.number_input("회전 원판 질량 관성모멘트, J (kg·m²)", value=0.5)
        
    if length > 0 and J_mass > 0:
        r = (dia / 1000) / 2
        Ip = (math.pi / 2) * (r**4) # 극단면 2차 모멘트
        kt = (G * 1e9 * Ip) / length # 비틀림 강성
        wn_t = math.sqrt(kt / J_mass)
        st.info(f"비틀림 강성 (kt): **{kt:,.1f} N·m/rad**")
        st.success(f"비틀림 고유진동수: **{wn_t / (2 * math.pi):.2f} Hz**")

# 10. 2-DOF 모드 해석 강성 행렬
elif "다자유도" in calc_menu:
    st.subheader("10. 2자유도(2-DOF) 무감쇠 시스템 고유치 해석 고정틀 구조")
    st.markdown("질량 배치와 스프링 병렬 구조를 기반으로 강성 행렬의 기본 요소(K11, K22, K12)를 정의합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        k1 = st.number_input("스프링 1 강성 (N/m)", value=10000.0)
        k2 = st.number_input("중간 연결 스프링 2 강성 (N/m)", value=5000.0)
    with col2:
        k3 = st.number_input("스프링 3 강성 (N/m)", value=10000.0)
        
    K11 = k1 + k2
    K22 = k2 + k3
    K12 = -k2
    
    st.info("구조 해석(CAE) 행렬 입력 데이터:")
    st.latex(rf"K = \begin{{bmatrix}} {K11:,.0f} & {K12:,.0f} \\ {K12:,.0f} & {K22:,.0f} \end{{bmatrix}} \; N/m")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Vibration Engineers")
