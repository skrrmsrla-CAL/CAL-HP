import streamlit as st
import math

st.set_page_config(page_title="EngiMate | Statics", page_icon="📐", layout="centered")

st.title("📐 정역학 통합 계산기")
st.markdown("힘과 모멘트의 평형, 지점 반력, 마찰 및 무게중심을 계산하는 10대 수식입니다.")
st.divider()

calc_menu = st.selectbox("실행할 계산기를 선택하세요:", [
    "1. 2D 벡터 합성 (Vector Addition)",
    "2. 모멘트 계산 (Moment of a Force)",
    "3. 단순보 지점 반력 (Beam Reactions)",
    "4. 분포 하중의 등가 변환",
    "5. 무게중심 좌표 (Centroid)",
    "6. 평면 마찰력 (Static Friction)",
    "7. 빗면에서의 블록 평형 (Inclined Plane)",
    "8. 2-케이블 장력 평형 (Cable Tension)",
    "9. 복합 도르래 기계적 이점 (Mechanical Advantage)",
    "10. 단순 트러스 절점법 (Method of Joints)"
])

st.write("---")

# 1. 2D 벡터 합성
if "벡터 합성" in calc_menu:
    st.subheader("1. 2D 벡터 합성")
    col1, col2 = st.columns(2)
    with col1:
        F1 = st.number_input("힘 1 크기 (N)", value=100.0)
        a1 = st.number_input("힘 1 각도 (도, x축 기준)", value=30.0)
    with col2:
        F2 = st.number_input("힘 2 크기 (N)", value=150.0)
        a2 = st.number_input("힘 2 각도 (도, x축 기준)", value=120.0)
        
    Rx = F1*math.cos(math.radians(a1)) + F2*math.cos(math.radians(a2))
    Ry = F1*math.sin(math.radians(a1)) + F2*math.sin(math.radians(a2))
    R_mag = math.sqrt(Rx**2 + Ry**2)
    R_ang = math.degrees(math.atan2(Ry, Rx))
    
    st.info(f"합력 크기: **{R_mag:.2f} N** | 합력 각도: **{R_ang:.2f} °**")

# 2. 모멘트 계산
elif "모멘트 계산" in calc_menu:
    st.subheader("2. 2D 모멘트 (M = F × d)")
    F = st.number_input("작용하는 힘 (N)", value=500.0)
    d = st.number_input("회전축으로부터의 수직 거리 (m)", value=2.5)
    st.info(f"발생 모멘트: **{F * d:,.2f} N·m**")

# 3. 단순보 지점 반력
elif "단순보" in calc_menu:
    st.subheader("3. 단순보 지점 반력 (집중 하중)")
    L = st.number_input("보의 전체 길이, L (m)", value=10.0)
    F = st.number_input("집중 하중 크기, P (N)", value=1000.0)
    a = st.number_input("왼쪽 지점(A)에서 하중까지의 거리, a (m)", value=3.0)
    
    if L > 0 and a <= L:
        Rb = (F * a) / L
        Ra = F - Rb
        st.info(f"좌측(A) 반력: **{Ra:.2f} N** | 우측(B) 반력: **{Rb:.2f} N**")

# 4. 분포 하중 등가 변환
elif "분포 하중" in calc_menu:
    st.subheader("4. 분포 하중 등가 변환")
    w = st.number_input("등분포 하중 밀도, w (N/m)", value=200.0)
    L = st.number_input("작용 길이, L (m)", value=5.0)
    st.info(f"등가 집중 하중: **{w*L:.2f} N** (작용점: 중심에서 **{L/2:.2f} m**)")

# 5. 무게중심 좌표
elif "무게중심" in calc_menu:
    st.subheader("5. 합성 도형의 도심 (Centroid)")
    st.markdown("두 개의 사각형이 결합된 형태의 도심을 계산합니다.")
    col1, col2 = st.columns(2)
    with col1:
        A1 = st.number_input("도형 1 면적", value=50.0)
        y1 = st.number_input("도형 1 도심 Y좌표", value=5.0)
    with col2:
        A2 = st.number_input("도형 2 면적", value=100.0)
        y2 = st.number_input("도형 2 도심 Y좌표", value=15.0)
        
    Y_bar = (A1*y1 + A2*y2) / (A1 + A2)
    st.info(f"전체 합성 도심 Y_bar: **{Y_bar:.2f}**")

# 6. 평면 마찰력
elif "마찰력" in calc_menu:
    st.subheader("6. 최대 정지 마찰력")
    mass = st.number_input("물체의 질량 (kg)", value=50.0)
    mu_s = st.number_input("정지 마찰 계수 (μs)", value=0.4)
    N = mass * 9.80665
    f_max = mu_s * N
    st.info(f"수직 항력: **{N:.2f} N** | 최대 정지 마찰력: **{f_max:.2f} N**")

# 7. 빗면 블록 평형
elif "빗면" in calc_menu:
    st.subheader("7. 빗면에서의 평형 조건")
    mass = st.number_input("질량 (kg)", value=10.0)
    angle = st.number_input("경사각 (°)", value=30.0)
    
    W = mass * 9.80665
    F_parallel = W * math.sin(math.radians(angle))
    N_force = W * math.cos(math.radians(angle))
    
    st.info(f"미끄러지려는 힘: **{F_parallel:.2f} N** | 빗면 수직 항력: **{N_force:.2f} N**")

# 8. 2-케이블 장력
elif "케이블" in calc_menu:
    st.subheader("8. 대칭 케이블 장력 평형")
    weight = st.number_input("매달린 하중 (N)", value=1000.0)
    angle = st.number_input("수평면과 케이블이 이루는 각도 (°)", value=45.0)
    
    if angle > 0 and angle < 90:
        T = (weight / 2) / math.sin(math.radians(angle))
        st.info(f"각 케이블에 걸리는 장력 (T): **{T:.2f} N**")
    else:
        st.error("각도는 0 초과 90 미만이어야 합니다.")

# 9. 복합 도르래 기계적 이점
elif "도르래" in calc_menu:
    st.subheader("9. 복합 도르래 기계적 이점")
    n = st.number_input("하중을 지탱하는 케이블 가닥 수 (n)", min_value=1, value=4, step=1)
    load = st.number_input("끌어올릴 하중 (N)", value=2000.0)
    
    pull_force = load / n
    st.info(f"기계적 이점 (MA): **{n}** | 필요 당김 힘: **{pull_force:.2f} N**")

# 10. 단순 트러스 절점법
elif "트러스" in calc_menu:
    st.subheader("10. Y자형 트러스 절점 해석")
    st.markdown("절점에 수직 하중이 작용할 때 좌우 대칭 부재력 산출")
    P = st.number_input("절점에 작용하는 수직 하중 (N)", value=5000.0)
    theta = st.number_input("부재가 수평과 이루는 각도 (°)", value=60.0)
    
    if theta > 0 and theta < 90:
        F_member = (P / 2) / math.sin(math.radians(theta))
        st.info(f"각 부재에 걸리는 힘 (압축력): **{F_member:.2f} N**")

st.divider()
st.caption("© 2026 EngiMate - The Smart Tool for Engineers")
