import streamlit as st

st.set_page_config(page_title="EngiMate | Home", page_icon="⚙️", layout="wide")

st.title("⚙️ EngiMate Engineering Suite")
st.markdown("전 세계 엔지니어를 위한 110종의 통합 공학 계산 플랫폼입니다.")
st.divider()

# 분야별 타일형 링크 구성
cols = st.columns(3)
categories = [
    ("🔄 단위 변환기", "pages/01_Converter.py"),
    ("🔥 열역학 및 열전달", "pages/02_Thermodynamics_Heat.py"),
    ("🌊 유체역학", "pages/03_Fluid_Mechanics.py"),
    ("🏗️ 재료역학", "pages/04_Solid_Mechanics.py"),
    ("📐 정역학", "pages/05_Statics.py"),
    ("🏢 구조역학", "pages/06_Structural_Mechanics.py"),
    ("⚙️ 동역학", "pages/07_Dynamics.py"),
    ("⚡ 전기전자", "pages/08_Electrical_Systems.py"),
    ("🤖 메카트로닉스", "pages/09_Mechatronics.py"),
    ("📊 신뢰성/성능", "pages/10_Reliability.py"),
    ("🔊 기계진동", "pages/11_Mechanical_Vibration.py")
]

for i, (name, path) in enumerate(categories):
    with cols[i % 3]:
        if st.button(name, use_container_width=True):
            st.switch_page(path)

st.divider()
st.info("💡 사이드바 메뉴를 통해 모든 계산기에 직접 접근할 수 있습니다.")
