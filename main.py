import streamlit as st
import pandas as pd
import altair as alt

# 제목
st.title("국가별 MBTI 상위 3유형 시각화")

# 파일 경로 (같은 폴더에 존재한다고 가정)
DEFAULT_CSV_PATH = "countriesMBTI_16types.csv"

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (선택)", type="csv")

# 업로드 파일이 없으면 기본 파일 사용
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv(DEFAULT_CSV_PATH)
    except FileNotFoundError:
        st.error(f"기본 데이터 파일({DEFAULT_CSV_PATH})이 없습니다. CSV를 업로드해주세요.")
        st.stop()

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

# Altair 시각화
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
