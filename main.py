import streamlit as st
import pandas as pd
import altair as alt

# 제목
st.title("국가별 MBTI 상위 3유형 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 국가 리스트 추출
    countries = df["Country"].tolist()

    # 국가 선택
    selected_country = st.selectbox("국가 선택", countries)

    # 해당 국가의 MBTI 데이터 추출
    country_row = df[df["Country"] == selected_country].iloc[0]

    # MBTI 데이터만 추출 (Country 제외)
    mbti_data = country_row.drop("Country")

    # 내림차순 정렬 후 상위 3개 추출
    top3 = mbti_data.sort_values(ascending=False).head(3).reset_index()
    top3.columns = ["MBTI", "비율"]

    # Altair 차트 생성
    chart = alt.Chart(top3).mark_bar().encode(
        x=alt.X("MBTI", sort="-y"),
        y=alt.Y("비율", title="비율 (%)"),
        color=alt.Color("MBTI", legend=None)
    ).properties(
        title=f"{selected_country} - 상위 3개 MBTI 유형",
        width=500,
        height=400
    )

    # 결과 출력
    st.altair_chart(chart, use_container_width=True)
    st.write(top3)
else:
    st.info("CSV 파일을 업로드해주세요.")

