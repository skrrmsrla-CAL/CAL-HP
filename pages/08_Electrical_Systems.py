import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Electrical", page_icon="⚡", layout="wide")

st.title("⚡ 전기전자 통합 계산기")
st.markdown("회로 분석, 전력 소비, 변압기 및 배선 설계용 핵심 10대 계산 툴셋입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 옴의 법칙 및 전력 ($P=VI$)",
    "2. 저항 합성 (직렬/병렬)",
    "3. RC 회로 시정수",
    "4. 교류 임피던스 ($R-L-C$)",
    "5. 변압기 권수비 및 전압",
    "6. 전압 분배기 (Voltage Divider)",
    "7. 도체 저항 (온도 영향 포함)",
    "8. LED 보호 저항",
    "9. 3상 전력 및 역률",
    "10. 배터리 런타임"
])

st.write("---")

# 1. 옴의 법칙 및 전력
if "옴의 법칙" in calc_menu:
    st.subheader("1. 옴의 법칙 및 전력")
    col1, col2, col3 = st.columns(3)
    V = col1.number_input("전압, V (V)", value=12.0)
    I = col2.number_input("전류, I (A)", value=1.0)
    R = col3.number_input("저항, R (Ω)", value=12.0)
    st.info(f"전력 (P): {V*I:.2f} W | 계산값 R={V/I if I!=0 else 0}Ω, I={V/R if R!=0 else 0}A")

# 2. 저항 합성
elif "저항 합성" in calc_menu:
    st.subheader("2. 저항 합성")
    mode = st.radio("모드", ["직렬 (Series)", "병렬 (Parallel)"])
    r_list = st.text_input("저항 값들을 쉼표로 구분하여 입력 (예: 10, 20, 30)", "10, 20")
    try:
        rs = [float(x.strip()) for x in r_list.split(",")]
        if mode == "직렬 (Series)":
            st.success(f"합성 저항: {sum(rs):.2f} Ω")
        else:
            st.success(f"합성 저항: {1/sum([1/r for r in rs if r!=0]):.2f} Ω")
    except: st.error("올바른 숫자를 입력하세요.")

# 3. RC 시정수
elif "RC 회로 시정수" in calc_menu:
    st.subheader("3. RC 회로 시정수 (τ = RC)")
    R = st.number_input("저항, R (Ω)", value=1000.0)
    C = st.number_input("커패시터, C (F)", value=0.000001, format="%f")
    st.info(f"시정수 (τ): {R*C:.4f} s | 5τ 도달 시간: {5*R*C:.4f} s")

# 4. 교류 임피던스
elif "교류 임피던스" in calc_menu:
    st.subheader("4. 교류 임피던스 (R-L-C)")
    R = st.number_input("저항, R (Ω)", value=10.0)
    L = st.number_input("인덕턴스, L (H)", value=0.1)
    C = st.number_input("커패시턴스, C (F)", value=0.0001, format="%f")
    f = st.number_input("주파수, f (Hz)", value=60.0)
    w = 2 * math.pi * f
    Z = math.sqrt(R**2 + (w*L - 1/(w*C))**2)
    st.info(f"임피던스 (Z): {Z:.2f} Ω")

# 5. 변압기 권수비
elif "변압기" in calc_menu:
    st.subheader("5. 변압기 권수비 ($N_1/N_2 = V_1/V_2$)")
    N1 = st.number_input("1차 권수 (N1)", value=1000)
    N2 = st.number_input("2차 권수 (N2)", value=100)
    V1 = st.number_input("1차 전압 (V1)", value=220.0)
    st.info(f"2차 전압 (V2): {(V1 * N2 / N1):.2f} V")

# 6. 전압 분배기
elif "전압 분배기" in calc_menu:
    st.subheader("6. 전압 분배기")
    Vin = st.number_input("입력 전압 (Vin)", value=12.0)
    R1 = st.number_input("R1 (Ω)", value=1000.0)
    R2 = st.number_input("R2 (Ω)", value=1000.0)
    st.info(f"출력 전압 (Vout): {Vin * R2 / (R1 + R2):.2f} V")

# 7. 도체 저항
elif "도체 저항" in calc_menu:
    st.subheader("7. 도체 저항 ($R = \rho L / A$)")
    rho = st.number_input("비저항 (Ω·m)", value=1.72e-8, format="%e")
    L = st.number_input("길이 (m)", value=10.0)
    A = st.number_input("단면적 (m²)", value=1e-6, format="%e")
    st.info(f"저항: {rho * L / A:.4f} Ω")

# 8. LED 보호 저항
elif "LED" in calc_menu:
    st.subheader("8. LED 보호 저항")
    Vs = st.number_input("공급 전압 (V)", value=5.0)
    Vf = st.number_input("LED 순방향 전압 (V)", value=2.0)
    I = st.number_input("전류 (A)", value=0.02)
    st.info(f"필요 저항: {(Vs - Vf) / I:.1f} Ω")

# 9. 3상 전력
elif "3상 전력" in calc_menu:
    st.subheader("9. 3상 전력 ($P = \sqrt{3} V I \cos\theta$)")
    V = st.number_input("전압 (V)", value=380.0)
    I = st.number_input("전류 (A)", value=10.0)
    pf = st.number_input("역률 (0~1)", value=0.9)
    st.info(f"유효 전력 (P): {math.sqrt(3) * V * I * pf:.2f} W")

# 10. 배터리 런타임
elif "배터리" in calc_menu:
    st.subheader("10. 배터리 런타임")
    cap = st.number_input("배터리 용량 (mAh)", value=3000.0)
    load = st.number_input("부하 전류 (mA)", value=500.0)
    eff = st.number_input("효율 (%)", value=80.0) / 100
    st.info(f"예상 런타임: {(cap * eff) / load:.2f} 시간")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Engineers")
