import os

import streamlit as st


if "KRX_ID" in st.secrets:
    os.environ["KRX_ID"] = st.secrets["KRX_ID"]

if "KRX_PW" in st.secrets:
    os.environ["KRX_PW"] = st.secrets["KRX_PW"]

from pykrx import stock
from datetime import date, timedelta

import streamlit as st
from pykrx import stock


st.set_page_config(
    page_title="PyKRX 주식 조회",
    page_icon="📈",
    layout="wide",
)

st.title("📈 PyKRX 한국 주식 조회")
st.caption("종목코드와 조회 기간을 입력해 주가 데이터를 조회합니다.")


# 입력 부분
ticker = st.text_input(
    "종목코드",
    value="005930",
    max_chars=6,
    help="삼성전자 005930 / SK하이닉스 000660 / 에이피알 278470",
)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "시작일",
        value=date.today() - timedelta(days=30),
    )

with col2:
    end_date = st.date_input(
        "종료일",
        value=date.today(),
    )


@st.cache_data(ttl=3600)
def load_data(
    ticker_code: str,
    start: date,
    end: date,
):
    start_text = start.strftime("%Y%m%d")
    end_text = end.strftime("%Y%m%d")

    return stock.get_market_ohlcv(
        start_text,
        end_text,
        ticker_code,
    )


if st.button("조회하기", type="primary"):

    ticker = ticker.strip()

    if len(ticker) != 6 or not ticker.isdigit():
        st.error("종목코드는 숫자 6자리로 입력해주세요.")

    elif start_date > end_date:
        st.error("시작일은 종료일보다 앞서야 합니다.")

    else:
        try:
            with st.spinner("KRX 데이터를 불러오는 중입니다..."):
                df = load_data(
                    ticker,
                    start_date,
                    end_date,
                )

            if df.empty:
                st.warning(
                    "조회된 데이터가 없습니다. "
                    "종목코드와 조회 기간을 확인해주세요."
                )

            else:
                stock_name = stock.get_market_ticker_name(ticker)

                if not stock_name:
                    stock_name = ticker

                st.success("조회가 완료되었습니다.")
                st.subheader(f"{stock_name} ({ticker})")

                if "종가" in df.columns:
                    latest_close = int(df["종가"].iloc[-1])
                    first_close = int(df["종가"].iloc[0])

                    if first_close != 0:
                        return_rate = (
                            latest_close / first_close - 1
                        ) * 100
                    else:
                        return_rate = 0.0

                    metric1, metric2, metric3 = st.columns(3)

                    with metric1:
                        st.metric(
                            "최근 종가",
                            f"{latest_close:,}원",
                        )

                    with metric2:
                        st.metric(
                            "조회 기간 등락률",
                            f"{return_rate:.2f}%",
                        )

                    with metric3:
                        st.metric(
                            "조회 거래일",
                            f"{len(df):,}일",
                        )

                    st.subheader("종가 차트")
                    st.line_chart(df["종가"])

                st.subheader("일자별 데이터")

                st.dataframe(
                    df,
                    use_container_width=True,
                )

                csv_data = df.to_csv(
                    encoding="utf-8-sig",
                ).encode("utf-8-sig")

                st.download_button(
                    label="CSV 파일 내려받기",
                    data=csv_data,
                    file_name=f"{ticker}_주가.csv",
                    mime="text/csv",
                )

        except Exception as error:
            st.error("데이터 조회 중 오류가 발생했습니다.")
            st.code(str(error))

            st.info(
                "인터넷 연결, 종목코드, 날짜와 "
                "PyKRX 설치 상태를 확인해주세요."
            )
