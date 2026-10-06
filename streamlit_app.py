from datetime import date

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Streamlit 요소 체험실", page_icon="🧪", layout="wide")

st.title("Streamlit 요소 체험실")
st.markdown(
    "Streamlit은 파이썬 코드만으로 웹 앱을 만드는 도구입니다. "
    "아래 위젯을 직접 바꾸거나 눌러 보면서 화면이 어떻게 반응하는지 확인해 보세요."
)
st.caption("앱은 크게 정보를 보여주는 요소, 값을 입력받는 위젯, 화면을 정리하는 레이아웃으로 구성됩니다.")

basics_tab, data_tab, layout_tab = st.tabs(["입력과 텍스트", "표와 차트", "레이아웃과 파일"])

with basics_tab:
    st.header("입력 위젯과 텍스트")
    st.write("`st.title`, `st.header`, `st.write`는 제목과 설명을 화면에 표시합니다.")

    st.subheader("값을 입력해 보세요")
    name_col, age_col = st.columns(2)
    with name_col:
        name = st.text_input("이름", placeholder="예: 민지")
        favorite = st.selectbox("좋아하는 과목", ["수학", "과학", "역사", "미술"])
    with age_col:
        age = st.number_input("나이", min_value=1, max_value=120, value=20)
        visit_date = st.date_input("방문 날짜", value=date.today())

    mood = st.radio("오늘의 기분", ["좋음", "보통", "피곤함"], horizontal=True)
    topics = st.multiselect(
        "더 알아보고 싶은 요소",
        ["버튼", "차트", "데이터 표", "파일 업로드", "레이아웃"],
        default=["차트"],
    )
    message = st.text_area("짧은 메모", placeholder="위젯을 사용해 본 느낌을 적어 보세요.")

    left_col, right_col = st.columns(2)
    with left_col:
        score = st.slider("만족도 슬라이더", min_value=0, max_value=100, value=65)
    with right_col:
        level = st.select_slider("학습 난이도", options=["입문", "초급", "중급", "도전"], value="초급")

    show_summary = st.checkbox("입력한 내용 요약 보기", value=True)
    receive_updates = st.toggle("새 예제 알림 받기", value=False)
    if show_summary:
        st.info(
            f"{name or '방문자'}님, {age}세 · {favorite} 선호 · {visit_date} 방문 · "
            f"기분: {mood} · 만족도: {score}/100 · 난이도: {level}"
        )
        if topics:
            st.write("관심 요소:", ", ".join(topics))
        if message:
            st.caption(f"메모: {message}")
    st.write(f"알림 설정: {'켜짐' if receive_updates else '꺼짐'}")

    st.subheader("버튼과 상태")
    st.write("버튼을 누르면 앱이 다시 실행됩니다. 세션 상태에 횟수를 저장해 값이 유지되도록 했습니다.")
    if "demo_click_count" not in st.session_state:
        st.session_state.demo_click_count = 0
    if st.button("버튼 눌러 보기", type="primary"):
        st.session_state.demo_click_count += 1
    st.metric("누른 횟수", st.session_state.demo_click_count)

    st.subheader("폼으로 한 번에 제출")
    st.write("폼 안의 입력은 제출 버튼을 누를 때 한꺼번에 반영됩니다.")
    with st.form("feedback_form"):
        feedback = st.text_input("한 줄 피드백", key="feedback_input")
        submitted = st.form_submit_button("피드백 제출")
    if submitted:
        st.success(f"제출 완료: {feedback or '내용 없음'}")

with data_tab:
    st.header("데이터 표와 차트")
    st.write("표에서 숫자를 직접 고쳐 보세요. 아래 막대 차트가 편집한 값으로 다시 그려집니다.")

    sample_data = pd.DataFrame(
        {
            "활동": ["독서", "산책", "공부", "휴식", "운동"],
            "분": [30, 25, 60, 40, 35],
            "만족도": [4, 5, 3, 5, 4],
        }
    )
    edited_data = st.data_editor(
        sample_data,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "분": st.column_config.NumberColumn("분", min_value=0, max_value=240),
            "만족도": st.column_config.NumberColumn("만족도", min_value=1, max_value=5, step=1),
        },
        width="stretch",
    )
    chart_col, table_col = st.columns([3, 2])
    with chart_col:
        st.subheader("만족도 차트")
        st.bar_chart(edited_data, x="활동", y="만족도", color="#168C83")
    with table_col:
        st.subheader("요약 표")
        st.dataframe(edited_data, hide_index=True, width="stretch")

    st.subheader("시간에 따른 변화")
    days = ["월", "화", "수", "목", "금", "토", "일"]
    weekly_data = pd.DataFrame(
        {"요일": days, "방문자": [18, 24, 21, 32, 29, 45, 39], "가입자": [3, 5, 4, 8, 7, 12, 10]}
    )
    st.line_chart(weekly_data, x="요일", y=["방문자", "가입자"], color=["#168C83", "#E49B35"])
    st.caption("`st.bar_chart`와 `st.line_chart`는 DataFrame을 간단한 차트로 보여줍니다.")

with layout_tab:
    st.header("레이아웃과 파일")
    st.write("탭, 열, 컨테이너, 접기 영역을 사용하면 많은 요소를 읽기 쉽게 정리할 수 있습니다.")

    with st.container(border=True):
        st.subheader("컨테이너")
        st.write("관련된 요소를 하나의 영역에 묶습니다.")
        progress = st.slider("진행률 예시", min_value=0, max_value=100, value=40, key="progress_slider")
        st.progress(progress, text=f"학습 진행률 {progress}%")

    with st.expander("접기 / 펼치기", expanded=False):
        st.write("`st.expander`는 필요한 설명만 펼쳐 볼 수 있게 합니다.")
        st.code('st.success("완료!")', language="python")

    st.subheader("CSV 파일")
    st.write("CSV 파일을 올려 표로 확인하거나, 예제 데이터를 내려받을 수 있습니다.")
    uploaded_file = st.file_uploader("CSV 파일 선택", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_data = pd.read_csv(uploaded_file)
            st.dataframe(uploaded_data, width="stretch")
        except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
            st.error(f"CSV를 읽을 수 없습니다: {error}")

    csv_bytes = sample_data.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "예제 CSV 다운로드",
        data=csv_bytes,
        file_name="streamlit_example.csv",
        mime="text/csv",
    )

st.divider()
st.caption("더 많은 요소는 Streamlit 공식 문서의 API Reference에서 확인할 수 있습니다.")
