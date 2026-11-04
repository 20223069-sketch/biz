import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

st.title("🏪 Supermarket Sales 대시보드")

@st.cache_data
def load_data():
    # Sales.xlsx 파일에서 supermarket_sales_test 시트 로드
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 사이드바 설정
    st.sidebar.header("필터 설정")
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch) 선택", branches)

    # 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # Metric 계산
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    # Metric 화면 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💵 총 매출 (Total Sales)", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="📊 평균 매출 (Average Sales)", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="⭐ 평균 평점 (Average Rating)", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 상품 카테고리(Product line)별 평균 매출 계산
    category_sales = (
        filtered_df.groupby("Product line")["Total"]
        .mean()
        .reset_index()
        .rename(columns={"Total": "Average Sales"})
    )

    # 막대그래프 생성 및 시각화
    st.subheader(f"🎬 {selected_branch} 지점 - 상품 카테고리별 평균 매출")
    fig = px.bar(
        category_sales,
        x="Product line",
        y="Average Sales",
        text_auto=".2f",
        labels={"Product line": "상품 카테고리", "Average Sales": "평균 매출 ($)"},
        color="Product line",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("Sales.xlsx 파일을 app.py와 같은 폴더에 업로드해주세요.")
except Exception as e:
    st.error(f"에러가 발생했습니다: {e}")
