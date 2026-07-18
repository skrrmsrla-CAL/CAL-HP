import streamlit as st

# 페이지 구성
st.set_page_config(
    page_title="EngiMate | Engineering Hub", 
    page_icon="⚙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 헤더 영역
st.title("⚙️ EngiMate Engineering Suite")
st.markdown("### 전문 엔지니어를 위한 110종 통합 공학 계산 플랫폼")
st.write("기계, 화공, 플랜트 설계의 복잡한 수식을 손쉽게 해결하세요.")
st.divider()

# 검색창 (상단에 배치하여 110개 계산기 중 즉시 검색 가능)
search_query = st.text_input("🔍 원하는 계산기 이름을 검색하세요 (예: 레이놀즈, 처짐, 압력강하...)", "")

# 분야별 카테고리 (트리 구조)
st.subheader("📂 공학 분야별 네비게이션")

# 3열 타일 구성
col1, col2, col3 = st.columns(3)

# 분야별 매핑
categories = [
    ("🔄", "단위 변환기", "pages/01_converter.py"),
    ("🔥", "열역학 및 열전달", "pages/02_Thermodynamics_&_Heat_Transfer.py"),
    ("🌊", "유체역학", "pages/03_Fluid_Mechanics.py"),
    ("🏗️", "재료역학", "pages/04_Solid_Mechanics.py"),
    ("📐", "정역학", "pages/05_Statics.py"),
    ("🏢", "구조역학", "pages/06_Structural_Mechanics.py"),
    ("⚙️", "동역학", "pages/07_Dynamics.py"),
    ("⚡", "전기전자", "pages/08_Electrical_Systems.py"),
    ("🤖", "메카트로닉스", "pages/09_Mechatronics.py"),
    ("📊", "시스템 신뢰성", "pages/10_Reliability.py"),
    ("🔊", "기계진동", "pages/11_Mechanical_Vibration.py")
]

# 버튼 생성 로직
for i, (icon, name, path) in enumerate(categories):
    col = [col1, col2, col3][i % 3]
    if col.button(f"{icon} {name}", use_container_width=True):
        st.switch_page(path)

st.divider()

# 하단 정보 및 업데이트 로그
st.info("💡 사이드바 메뉴를 사용하면 더 빠르게 이동할 수 있습니다.")
st.caption("© 2026 EngiMate - Designed for Professional Engineers")
