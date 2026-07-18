import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Reliability", page_icon="📊", layout="wide")

st.title("📊 시스템 신뢰성 및 성능 계산기")
st.markdown("부품의 고장률, 수명 분포, 시스템 가용도 등 기계 설계의 마지막 검증 단계에 사용됩니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 고장률 및 MTBF",
    "2. 직렬 시스템 신뢰도 ($R_s$)",
    "3. 병렬 시스템 신뢰도 ($R_p$)",
    "4. 시스템 가용도 (Availability)",
    "5. 베이불 분포 (Weibull Reliability)",
    "6. 지수 분포 확률 (Exponential CDF)",
    "7. 고장 빈도 (Failure Intensity)",
    "8. 안전 계수와 고장 확률",
    "9. 중복 시스템 신뢰도 ($k$-out-of-$n$)",
    "10. 수명 예측 (Arrhenius Model)"
])

st.write("---")

# 1. 고장률 및 MTBF
if "고장률" in calc_menu:
    st.subheader("1. 고장률($\lambda$) 및 평균 고장 간격(MTBF)")
    fail = st.number_input("총 고장 횟수", value=5)
    time = st.number_input("총 운전 시간 (hr)", value=50000.0)
    st.info(f"고장률 (λ): {fail/time:.2e} 회/시간 | MTBF: {time/fail:.0f} 시간")

# 2. 직렬 시스템 신뢰도
elif "직렬" in calc_menu:
    st.subheader("2. 직렬 시스템 신뢰도 ($R_s = \prod R_i$)")
    r_list = st.text_input("각 부품 신뢰도 (0~1)를 쉼표로 구분:", "0.99, 0.98, 0.95")
    rs = [float(x.strip()) for x in r_list.split(",")]
    st.info(f"시스템 신뢰도: {math.prod(rs):.4f}")

# 3. 병렬 시스템 신뢰도
elif "병렬" in calc_menu:
    st.subheader("3. 병렬 시스템 신뢰도 ($R_p = 1 - \prod (1-R_i)$)")
    r_list = st.text_input("각 부품 신뢰도 (0~1)를 쉼표로 구분:", "0.9, 0.9")
    rs = [float(x.strip()) for x in r_list.split(",")]
    st.info(f"시스템 신뢰도: {1 - math.prod([1-r for r in rs]):.4f}")

# 4. 시스템 가용도
elif "가용도" in calc_menu:
    st.subheader("4. 시스템 가용도 (Availability)")
    mtbf = st.number_input("MTBF (hr)", value=1000.0)
    mttr = st.number_input("MTTR (hr - 평균 복구 시간)", value=20.0)
    st.info(f"가용도: {mtbf / (mtbf + mttr):.4%}")

# 5. 베이불 분포
elif "베이불" in calc_menu:
    st.subheader("5. 베이불 분포 (Weibull Reliability)")
    st.latex(r"R(t) = e^{-(t/\eta)^\beta}")
    beta = st.number_input("형상 파라미터, β", value=1.5)
    eta = st.number_input("척도 파라미터(수명), η", value=5000.0)
    t = st.number_input("운전 시간, t", value=2000.0)
    st.info(f"신뢰도 R(t): {math.exp(-(t/eta)**beta):.4f}")

# 6. 지수 분포 확률
elif "지수 분포" in calc_menu:
    st.subheader("6. 지수 분포 고장 확률 (CDF)")
    lam = st.number_input("고장률, λ", value=0.001)
    t = st.number_input("시간, t", value=100.0)
    st.info(f"고장 확률 F(t): {1 - math.exp(-lam * t):.4f}")

# 7. 고장 빈도
elif "고장 빈도" in calc_menu:
    st.subheader("7. 고장 빈도 (Hazard Rate)")
    st.markdown("정비 기간 중 고장 발생 강도 계산")
    n = st.number_input("고장 발생 수", value=3)
    t = st.number_input("관측 기간 (hr)", value=1000.0)
    st.info(f"순간 고장률: {n/t:.2e} /hr")

# 8. 안전 계수와 고장 확률
elif "안전 계수" in calc_menu:
    st.subheader("8. 안전 계수 기반 고장 확률")
    mu_s = st.number_input("응력 평균값", value=100.0)
    sig_s = st.number_input("응력 표준편차", value=10.0)
    mu_r = st.number_input("강도 평균값", value=150.0)
    sig_r = st.number_input("강도 표준편차", value=15.0)
    # Z-score 간단 모델
    z = (mu_r - mu_s) / math.sqrt(sig_r**2 + sig_s**2)
    st.info(f"Z-score: {z:.2f} (Z가 클수록 고장 확률이 낮음)")

# 9. k-out-of-n 신뢰도
elif "중복 시스템" in calc_menu:
    st.subheader("9. k-out-of-n 시스템 신뢰도")
    n = st.number_input("전체 부품 수 (n)", value=3)
    k = st.number_input("정상 작동 필요 부품 수 (k)", value=2)
    r = st.number_input("부품 개별 신뢰도 (r)", value=0.9)
    # 간략 이항분포 모델
    prob = sum([math.comb(n, i) * (r**i) * ((1-r)**(n-i)) for i in range(k, n+1)])
    st.info(f"시스템 신뢰도: {prob:.4f}")

# 10. 수명 예측 (Arrhenius)
elif "수명 예측" in calc_menu:
    st.subheader("10. 아레니우스 수명 예측 (가속 시험)")
    st.latex(r"AF = e^{\frac{E_a}{k} (\frac{1}{T_{use}} - \frac{1}{T_{test}})}")
    Ea = st.number_input("활성화 에너지 (eV)", value=0.6)
    T_use = st.number_input("사용 온도 (K)", value=300.0)
    T_test = st.number_input("시험 온도 (K)", value=350.0)
    af = math.exp((Ea / 8.617e-5) * (1/T_use - 1/T_test))
    st.info(f"가속 계수 (AF): {af:.2f} (시험 시간이 실사용 시간보다 {af:.2f}배 짧음)")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Engineers")
