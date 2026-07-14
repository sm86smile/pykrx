"""PyKRX Streamlit 통합 조회 앱.

저장소 루트에서 실행하세요.
    python -m streamlit run app.py

이 앱은 로컬 저장소의 ``pykrx`` 패키지를 우선 사용합니다.
"""

from __future__ import annotations

import contextlib
import inspect
import io
import json
import os
import traceback
from datetime import date, timedelta
from typing import Any, Callable

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Streamlit / 인증 초기화
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PyKRX 통합 조회",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _load_secrets_to_environment() -> None:
    """Streamlit Secrets의 KRX 계정을 환경변수에 반영한다."""
    try:
        krx_id = st.secrets.get("KRX_ID")
        krx_pw = st.secrets.get("KRX_PW")
    except Exception:
        return

    if krx_id:
        os.environ["KRX_ID"] = str(krx_id)
    if krx_pw:
        os.environ["KRX_PW"] = str(krx_pw)


_load_secrets_to_environment()

# pykrx는 import 시 로그인 관련 메시지를 출력할 수 있으므로 UI에서는 숨긴다.
_import_log = io.StringIO()
try:
    with contextlib.redirect_stdout(_import_log), contextlib.redirect_stderr(_import_log):
        from pykrx import bond, stock
except Exception as exc:  # pragma: no cover - 실제 환경의 설치 오류 안내
    st.error("PyKRX를 불러오지 못했습니다.")
    st.code(str(exc))
    st.info("저장소 루트에서 실행했는지와 requirements.txt 설치 여부를 확인하세요.")
    st.stop()


# -----------------------------------------------------------------------------
# 상수 / 설명
# -----------------------------------------------------------------------------
MARKETS = ["KOSPI", "KOSDAQ", "KONEX", "ALL"]
INDEX_MARKETS = ["KOSPI", "KOSDAQ", "KRX", "테마"]
INVESTORS = [
    "금융투자",
    "보험",
    "투신",
    "사모",
    "은행",
    "기타금융",
    "연기금",
    "기관합계",
    "기타법인",
    "개인",
    "외국인",
    "기타외국인",
    "전체",
]
SHORTING_INCLUDE = ["주식", "ETF", "ETN", "ELW", "신주인수권증서및증권", "수익증권"]
BOND_KINDS = [
    "국고채1년",
    "국고채2년",
    "국고채3년",
    "국고채5년",
    "국고채10년",
    "국고채20년",
    "국고채30년",
    "국민주택1종5년",
    "회사채AA",
    "회사채BBB",
    "CD",
]

CATEGORY_RULES = [
    ("영업일·종목", ["business", "ticker_name", "ticker_list", "major_changes"]),
    ("주식 시세·기본지표", ["market_ohlcv", "market_cap", "market_fundamental", "price_change", "exhaustion", "sector"]),
    ("투자자 수급", ["trading_value", "trading_volume", "net_purchases"]),
    ("지수", ["index_"]),
    ("공매도", ["shorting_"]),
    ("ETF·ETN·ELW", ["etf_", "etn_", "elw_", "etx_"]),
    ("선물", ["future_"]),
    ("채권", ["treasury", "bond"]),
]


# -----------------------------------------------------------------------------
# 공통 유틸리티
# -----------------------------------------------------------------------------
def ymd(value: date) -> str:
    return value.strftime("%Y%m%d")


def get_public_functions(module: Any) -> dict[str, Callable[..., Any]]:
    functions: dict[str, Callable[..., Any]] = {}
    for name in dir(module):
        if not name.startswith("get_"):
            continue
        obj = getattr(module, name)
        if callable(obj):
            functions[name] = obj
    return dict(sorted(functions.items()))


STOCK_FUNCTIONS = get_public_functions(stock)
BOND_FUNCTIONS = get_public_functions(bond)


def category_of(function_name: str) -> str:
    for category, keywords in CATEGORY_RULES:
        if any(keyword in function_name for keyword in keywords):
            return category
    return "기타"


def first_doc_line(func: Callable[..., Any]) -> str:
    doc = inspect.getdoc(func) or ""
    for line in doc.splitlines():
        clean = line.strip()
        if clean and clean not in {"Args:", "Returns:"}:
            return clean
    return "설명이 없습니다."


def safe_signature(func: Callable[..., Any]) -> inspect.Signature | None:
    try:
        return inspect.signature(func)
    except (TypeError, ValueError):
        return None


def serializable(value: Any) -> Any:
    if isinstance(value, (date, pd.Timestamp)):
        return value.strftime("%Y%m%d")
    if isinstance(value, set):
        return sorted(value)
    return value


def result_to_dataframe(result: Any) -> pd.DataFrame | None:
    if isinstance(result, pd.DataFrame):
        return result.copy()
    if isinstance(result, pd.Series):
        return result.to_frame()
    if isinstance(result, dict):
        try:
            return pd.DataFrame(result)
        except ValueError:
            return pd.DataFrame(list(result.items()), columns=["항목", "값"])
    if isinstance(result, (list, tuple, set)):
        values = list(result)
        if not values:
            return pd.DataFrame()
        if isinstance(values[0], dict):
            return pd.DataFrame(values)
        return pd.DataFrame({"값": values})
    return None


def store_result(result: Any, title: str, call_text: str) -> None:
    st.session_state["pykrx_result"] = result
    st.session_state["pykrx_result_title"] = title
    st.session_state["pykrx_call_text"] = call_text


def run_call(
    func: Callable[..., Any],
    args: list[Any],
    kwargs: dict[str, Any],
    title: str,
) -> None:
    call_text = f"{func.__name__}(*{args!r}, **{kwargs!r})"
    try:
        with st.spinner("KRX/Naver 데이터를 조회하고 있습니다..."):
            result = func(*args, **kwargs)
        store_result(result, title, call_text)
        st.success("조회가 완료되었습니다.")
    except Exception as exc:
        st.error("조회 중 오류가 발생했습니다.")
        st.code(f"{type(exc).__name__}: {exc}")
        with st.expander("상세 오류 보기"):
            st.code(traceback.format_exc())
        st.info(
            "로그인이 필요한 API라면 `.streamlit/secrets.toml`에 KRX_ID와 KRX_PW를 설정하고, "
            "조회일이 휴일인지 또는 데이터 제공 시점이 지났는지 확인하세요."
        )


def render_result() -> None:
    if "pykrx_result" not in st.session_state:
        return

    result = st.session_state["pykrx_result"]
    title = st.session_state.get("pykrx_result_title", "조회 결과")
    call_text = st.session_state.get("pykrx_call_text", "")

    st.divider()
    st.subheader(title)
    if call_text:
        st.caption(f"실행 함수: `{call_text}`")

    df = result_to_dataframe(result)
    if df is not None:
        metric1, metric2 = st.columns(2)
        metric1.metric("행 수", f"{len(df):,}")
        metric2.metric("열 수", f"{len(df.columns):,}")

        st.dataframe(df, use_container_width=True, height=480)

        numeric_columns = list(df.select_dtypes(include="number").columns)
        if numeric_columns and len(df) > 1:
            with st.expander("차트 보기"):
                selected = st.multiselect(
                    "차트에 표시할 숫자 열",
                    numeric_columns,
                    default=numeric_columns[: min(3, len(numeric_columns))],
                    key="result_chart_columns",
                )
                if selected:
                    st.line_chart(df[selected])

        csv = df.to_csv(index=True, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            data=csv,
            file_name="pykrx_result.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.write(result)
        json_text = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        st.download_button(
            "JSON 다운로드",
            data=json_text.encode("utf-8"),
            file_name="pykrx_result.json",
            mime="application/json",
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
# 쉬운 조회 화면
# -----------------------------------------------------------------------------
def common_date_range(prefix: str, default_days: int = 30) -> tuple[date, date]:
    c1, c2 = st.columns(2)
    start = c1.date_input(
        "시작일",
        value=date.today() - timedelta(days=default_days),
        key=f"{prefix}_from",
    )
    end = c2.date_input("종료일", value=date.today(), key=f"{prefix}_to")
    return start, end


def render_easy_query() -> None:
    category = st.selectbox(
        "기능 분류",
        ["주식", "투자자 수급", "지수", "공매도", "ETF·ETN·ELW", "선물", "채권", "영업일·종목"],
    )

    if category == "주식":
        feature = st.selectbox(
            "조회 기능",
            [
                "종목 기간별 OHLCV",
                "시장 전체 OHLCV",
                "종목 기간별 시가총액",
                "시장 전체 시가총액",
                "종목 기간별 기본지표",
                "시장 전체 기본지표",
                "기간 가격 변동",
                "외국인 보유·한도소진율",
                "시장 업종 분류",
            ],
        )
        if feature == "종목 기간별 OHLCV":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_ohlcv")
            c1, c2 = st.columns(2)
            freq = c1.selectbox("주기", ["d", "m", "y"], format_func=lambda x: {"d": "일", "m": "월", "y": "년"}[x])
            adjusted = c2.checkbox("수정주가 적용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq, "adjusted": adjusted}, feature)

        elif feature == "시장 전체 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 시가총액":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_cap")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 시가총액":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS, index=3)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_cap_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "종목 기간별 기본지표":
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("stock_fund")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)

        elif feature == "시장 전체 기본지표":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            alternative = st.checkbox("휴일이면 이전 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": alternative}, feature)

        elif feature == "기간 가격 변동":
            start, end = common_date_range("stock_change")
            market = st.selectbox("시장", MARKETS)
            c1, c2 = st.columns(2)
            adjusted = c1.checkbox("수정주가 적용", value=True)
            delist = c2.checkbox("상장폐지 종목 포함", value=False)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market, "adjusted": adjusted, "delist": delist}, feature)

        elif feature == "외국인 보유·한도소진율":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("종목코드", "005930", max_chars=6)
                start, end = common_date_range("foreign_date")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", MARKETS)
                limited = st.checkbox("외국인 보유한도 제한 종목만", value=False)
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_exhaustion_rates_of_foreign_investment_by_ticker, [ymd(target)], {"market": market, "balance_limit": limited}, feature)

        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_sector_classifications, [ymd(target), market], {}, feature)

    elif category == "투자자 수급":
        feature = st.selectbox(
            "조회 기능",
            ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량", "투자자 순매수 상위종목", "시장 종목별 수급"],
        )
        start, end = common_date_range("trading")
        if feature in ["일자별 거래대금", "일자별 거래량", "기간 투자자별 거래대금", "기간 투자자별 거래량"]:
            ticker = st.text_input("종목코드 또는 시장명", "005930", help="종목코드 대신 KOSPI/KOSDAQ/KONEX/ALL을 입력할 수도 있습니다.")
            c1, c2, c3 = st.columns(3)
            etf = c1.checkbox("ETF 포함")
            etn = c2.checkbox("ETN 포함")
            elw = c3.checkbox("ELW 포함")
            if feature in ["일자별 거래대금", "일자별 거래량"]:
                c1, c2, c3 = st.columns(3)
                on = c1.selectbox("구분", ["순매수", "매수", "매도"])
                detail = c2.checkbox("기관 상세")
                freq = c3.selectbox("주기", ["d", "m", "y"])
                func = stock.get_market_trading_value_by_date if feature == "일자별 거래대금" else stock.get_market_trading_volume_by_date
                kwargs = {"etf": etf, "etn": etn, "elw": elw, "on": on, "detail": detail, "freq": freq}
            else:
                func = stock.get_market_trading_value_by_investor if feature == "기간 투자자별 거래대금" else stock.get_market_trading_volume_by_investor
                kwargs = {"etf": etf, "etn": etn, "elw": elw}
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], kwargs, feature)
        else:
            c1, c2 = st.columns(2)
            market = c1.selectbox("시장", MARKETS)
            investor = c2.selectbox("투자자", INVESTORS, index=9)
            func = stock.get_market_net_purchases_of_equities_by_ticker if feature == "투자자 순매수 상위종목" else stock.get_market_trading_value_and_volume_by_ticker
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market, "investor": investor}, feature)

    elif category == "지수":
        feature = st.selectbox("조회 기능", ["지수 목록", "지수 구성종목", "지수 기간별 OHLCV", "시장 전체 지수 OHLCV", "지수 기본지표", "지수 상장정보", "지수 등락률"])
        if feature == "지수 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        elif feature == "지수 구성종목":
            ticker = st.text_input("지수 티커", "1028", help="예: 코스피200 = 1028")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_portfolio_deposit_file, [ticker], {"date": ymd(target), "alternative": True}, feature)
        elif feature == "지수 기간별 OHLCV":
            ticker = st.text_input("지수 티커", "1028")
            start, end = common_date_range("index_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "시장 전체 지수 OHLCV":
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_ohlcv_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 기본지표":
            mode = st.radio("조회 방식", ["종목 기간", "시장 전체"], horizontal=True)
            if mode == "종목 기간":
                ticker = st.text_input("지수 티커", "1028")
                start, end = common_date_range("index_fund")
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_date, [ymd(start), ymd(end), ticker], {}, feature)
            else:
                c1, c2 = st.columns(2)
                target = c1.date_input("조회일", value=date.today())
                market = c2.selectbox("시장", ["KOSPI", "KOSDAQ"])
                if st.button("조회", type="primary", use_container_width=True):
                    run_call(stock.get_index_fundamental_by_ticker, [ymd(target)], {"market": market, "alternative": True}, feature)
        elif feature == "지수 상장정보":
            group = st.selectbox("계열 구분", INDEX_MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_listing_date, [], {"계열구분": group}, feature)
        else:
            start, end = common_date_range("index_change")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ", "KRX"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_index_price_change_by_ticker, [ymd(start), ymd(end)], {"market": market}, feature)

    elif category == "공매도":
        feature = st.selectbox(
            "조회 기능",
            ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "시장 공매도 거래량", "시장 공매도 거래대금", "투자자별 공매도 거래량", "투자자별 공매도 거래대금", "공매도 비중 TOP50", "공매도 잔고 TOP50", "종목 공매도 잔고", "시장 공매도 잔고"],
        )
        if feature in ["종목 공매도 현황", "일자별 공매도 거래량", "일자별 공매도 거래대금", "종목 공매도 잔고"]:
            ticker = st.text_input("종목코드", "005930", max_chars=6)
            start, end = common_date_range("short_ticker")
            func = {
                "종목 공매도 현황": stock.get_shorting_status_by_date,
                "일자별 공매도 거래량": stock.get_shorting_volume_by_date,
                "일자별 공매도 거래대금": stock.get_shorting_value_by_date,
                "종목 공매도 잔고": stock.get_shorting_balance_by_date,
            }[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        elif feature in ["투자자별 공매도 거래량", "투자자별 공매도 거래대금"]:
            start, end = common_date_range("short_investor")
            market = st.selectbox("시장", ["KOSPI", "KOSDAQ"])
            func = stock.get_shorting_investor_volume_by_date if "거래량" in feature else stock.get_shorting_investor_value_by_date
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end)], {"market": market}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            market = c2.selectbox("시장", ["KOSPI", "KOSDAQ", "KONEX"])
            include: list[str] | None = None
            if feature in ["시장 공매도 거래량", "시장 공매도 거래대금"]:
                include = st.multiselect("포함 증권", SHORTING_INCLUDE, default=["주식"])
            func = {
                "시장 공매도 거래량": stock.get_shorting_volume_by_ticker,
                "시장 공매도 거래대금": stock.get_shorting_value_by_ticker,
                "공매도 비중 TOP50": stock.get_shorting_volume_top50,
                "공매도 잔고 TOP50": stock.get_shorting_balance_top50,
                "시장 공매도 잔고": stock.get_shorting_balance_by_ticker,
            }[feature]
            kwargs: dict[str, Any] = {"market": market}
            if include is not None:
                kwargs.update({"include": include, "alternative": True})
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(target)], kwargs, feature)

    elif category == "ETF·ETN·ELW":
        feature = st.selectbox("조회 기능", ["ETF 목록", "ETN 목록", "ELW 목록", "ETF/ETN/ELW 통합 목록", "상품명 조회", "ETF ISIN", "ETF 기간별 OHLCV", "ETF 전체 OHLCV", "ETF 기간 등락률", "ETF 구성종목(PDF)", "ETF 괴리율", "ETF 추적오차", "ETF 투자자별 거래"])
        if feature in ["ETF 목록", "ETN 목록", "ELW 목록"]:
            target = st.date_input("기준일", value=date.today())
            func = {"ETF 목록": stock.get_etf_ticker_list, "ETN 목록": stock.get_etn_ticker_list, "ELW 목록": stock.get_elw_ticker_list}[feature]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [], {"date": ymd(target)}, feature)
        elif feature == "ETF/ETN/ELW 통합 목록":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etx_ticker_list, [product], {"date": ymd(target)}, feature)
        elif feature == "상품명 조회":
            product = st.selectbox("상품 종류", ["ETF", "ETN", "ELW"])
            ticker = st.text_input("티커", "069500")
            func = {"ETF": stock.get_etf_ticker_name, "ETN": stock.get_etn_ticker_name, "ELW": stock.get_elw_ticker_name}[product]
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)
        elif feature == "ETF ISIN":
            ticker = st.text_input("ETF 티커", "069500")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_isin, [ticker], {}, feature)
        elif feature == "ETF 기간별 OHLCV":
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_ohlcv")
            freq = st.selectbox("주기", ["d", "m", "y"])
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_date, [ymd(start), ymd(end), ticker], {"freq": freq}, feature)
        elif feature == "ETF 전체 OHLCV":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_ohlcv_by_ticker, [ymd(target)], {}, feature)
        elif feature == "ETF 기간 등락률":
            start, end = common_date_range("etf_change")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_price_change_by_ticker, [ymd(start), ymd(end)], {}, feature)
        elif feature == "ETF 구성종목(PDF)":
            ticker = st.text_input("ETF 티커", "069500")
            target = st.date_input("기준일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_portfolio_deposit_file, [ticker], {"date": ymd(target)}, feature)
        elif feature in ["ETF 괴리율", "ETF 추적오차"]:
            ticker = st.text_input("ETF 티커", "069500")
            start, end = common_date_range("etf_error")
            func = stock.get_etf_price_deviation if feature == "ETF 괴리율" else stock.get_etf_tracking_error
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ymd(start), ymd(end), ticker], {}, feature)
        else:
            start, end = common_date_range("etf_trade")
            st.caption("세부 오버로드가 복잡하므로 전체 API 실행기에서 원하는 인자를 직접 입력할 수도 있습니다.")
            if st.button("전체 ETF 거래 조회", type="primary", use_container_width=True):
                run_call(stock.get_etf_trading_volume_and_value, [ymd(start), ymd(end)], {}, feature)

    elif category == "선물":
        feature = st.selectbox("조회 기능", ["선물 상품 목록", "선물 상품명", "선물 일자별 OHLCV"])
        if feature == "선물 상품 목록":
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_list, [], {}, feature)
        elif feature == "선물 상품명":
            ticker = st.text_input("선물 티커", "KRDRVFUK2I")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ticker_name, [ticker], {}, feature)
        else:
            c1, c2 = st.columns(2)
            target = c1.date_input("조회일", value=date.today())
            prod = c2.text_input("선물 상품코드", "KRDRVFUK2I")
            alternative = st.checkbox("휴일이면 인접 영업일 사용", value=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_future_ohlcv_by_ticker, [ymd(target), prod], {"alternative": alternative, "prev": True}, feature)

    elif category == "채권":
        mode = st.radio("조회 방식", ["특정일 전체 채권수익률", "특정 채권 기간 수익률"], horizontal=True)
        if mode == "특정일 전체 채권수익률":
            target = st.date_input("조회일", value=date.today())
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(target)], {}, mode)
        else:
            kind = st.selectbox("채권 종류", BOND_KINDS)
            start, end = common_date_range("bond_yield", default_days=90)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(bond.get_otc_treasury_yields, [ymd(start), ymd(end), kind], {}, mode)

    else:  # 영업일·종목
        feature = st.selectbox("조회 기능", ["인접 영업일", "기간 영업일", "월별 영업일", "시장 종목 목록", "종목명 조회", "기업 주요 변동사항"])
        if feature == "인접 영업일":
            target = st.date_input("기준일", value=date.today())
            prev = st.radio("휴일 처리", [True, False], format_func=lambda x: "이전 영업일" if x else "다음 영업일", horizontal=True)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_nearest_business_day_in_a_week, [], {"date": ymd(target), "prev": prev}, feature)
        elif feature == "기간 영업일":
            start, end = common_date_range("business_range")
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"fromdate": ymd(start), "todate": ymd(end)}, feature)
        elif feature == "월별 영업일":
            c1, c2 = st.columns(2)
            year = c1.number_input("연도", min_value=1980, max_value=2100, value=date.today().year, step=1)
            month = c2.number_input("월", min_value=1, max_value=12, value=date.today().month, step=1)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_previous_business_days, [], {"year": int(year), "month": int(month)}, feature)
        elif feature == "시장 종목 목록":
            c1, c2 = st.columns(2)
            target = c1.date_input("기준일", value=date.today())
            market = c2.selectbox("시장", MARKETS)
            if st.button("조회", type="primary", use_container_width=True):
                run_call(stock.get_market_ticker_list, [], {"date": ymd(target), "market": market}, feature)
        else:
            ticker = st.text_input("종목코드", "005930")
            func = stock.get_market_ticker_name if feature == "종목명 조회" else stock.get_stock_major_changes
            if st.button("조회", type="primary", use_container_width=True):
                run_call(func, [ticker], {}, feature)


# -----------------------------------------------------------------------------
# 전체 API 자동 실행기
# -----------------------------------------------------------------------------
def render_parameter_widget(
    function_name: str,
    parameter: inspect.Parameter,
    key_prefix: str,
) -> tuple[bool, Any]:
    """서명 정보를 바탕으로 Streamlit 입력 위젯을 만든다.

    반환값의 첫 요소는 해당 인자를 실제 호출에 포함할지 여부다.
    """
    name = parameter.name
    default = parameter.default
    required = default is inspect.Parameter.empty
    label = f"{name}{' *' if required else ''}"
    key = f"{key_prefix}_{name}"

    if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
        return False, None

    # 선택적 인자는 사용 여부를 먼저 선택할 수 있다.
    use_value = True
    if not required:
        use_value = st.checkbox(f"{label} 사용", value=True, key=f"{key}_use")
        if not use_value:
            return False, None

    lower = name.lower()
    if lower in {"fromdate", "startdate", "start_dd", "startdd"}:
        return True, ymd(st.date_input(label, value=date.today() - timedelta(days=30), key=key))
    if lower in {"todate", "enddate", "end_dd", "enddd"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower in {"date", "basedate"}:
        return True, ymd(st.date_input(label, value=date.today(), key=key))
    if lower == "market":
        choices = ["ETF", "ETN", "ELW"] if function_name == "get_etx_ticker_list" else MARKETS
        default_value = default if isinstance(default, str) and default in choices else choices[0]
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower in {"계열구분"}:
        return True, st.selectbox(label, INDEX_MARKETS, key=key)
    if lower == "investor":
        default_value = default if isinstance(default, str) and default in INVESTORS else "개인"
        return True, st.selectbox(label, INVESTORS, index=INVESTORS.index(default_value), key=key)
    if lower == "freq":
        choices = ["d", "m", "y"]
        default_value = default if default in choices else "d"
        return True, st.selectbox(label, choices, index=choices.index(default_value), key=key)
    if lower == "on":
        return True, st.selectbox(label, ["순매수", "매수", "매도"], key=key)
    if lower == "include":
        return True, st.multiselect(label, SHORTING_INCLUDE, default=["주식"], key=key)
    if lower == "year":
        return True, int(st.number_input(label, 1980, 2100, date.today().year, key=key))
    if lower == "month":
        return True, int(st.number_input(label, 1, 12, date.today().month, key=key))

    annotation = parameter.annotation
    is_bool = isinstance(default, bool) or annotation is bool
    is_int = isinstance(default, int) and not isinstance(default, bool)
    if is_bool:
        return True, st.checkbox(label, value=bool(default) if default is not inspect.Parameter.empty else False, key=key)
    if is_int:
        return True, int(st.number_input(label, value=int(default), step=1, key=key))

    defaults_by_name = {
        "ticker": "005930",
        "prod": "KRDRVFUK2I",
        "bndKindTpCd": "국고채3년",
    }
    initial = defaults_by_name.get(name, "" if required else str(default))
    return True, st.text_input(label, value=initial, key=key)


def render_api_explorer() -> None:
    st.caption("`stock`와 `bond` 모듈에서 이름이 `get_`으로 시작하는 공개 함수를 자동으로 읽어 실행합니다.")
    module_name = st.radio("모듈", ["stock", "bond"], horizontal=True)
    function_map = STOCK_FUNCTIONS if module_name == "stock" else BOND_FUNCTIONS

    categories = sorted({category_of(name) for name in function_map})
    selected_category = st.selectbox("분류", ["전체"] + categories)
    filtered = {
        name: func
        for name, func in function_map.items()
        if selected_category == "전체" or category_of(name) == selected_category
    }
    function_name = st.selectbox("함수", list(filtered))
    func = filtered[function_name]
    signature = safe_signature(func)

    st.info(first_doc_line(func))
    st.code(f"{module_name}.{function_name}{signature or '(...)'}", language="python")

    doc = inspect.getdoc(func)
    if doc:
        with st.expander("함수 전체 설명"):
            st.text(doc)

    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    has_varargs = False

    if signature is not None:
        parameters = list(signature.parameters.values())
        for param in parameters:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                has_varargs = True
                continue
            include, value = render_parameter_widget(function_name, param, f"api_{module_name}_{function_name}")
            if not include:
                continue
            if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD) and param.default is inspect.Parameter.empty:
                args.append(serializable(value))
            else:
                kwargs[param.name] = serializable(value)

    if has_varargs or signature is None:
        st.warning("이 함수는 여러 호출 형식을 지원합니다. 아래 JSON에 위치 인자와 키워드 인자를 직접 입력하세요.")
        args_text = st.text_area("위치 인자 JSON 배열", value="[]", key=f"varargs_{module_name}_{function_name}")
        kwargs_text = st.text_area("키워드 인자 JSON 객체", value="{}", key=f"varkw_{module_name}_{function_name}")
        try:
            args = json.loads(args_text)
            kwargs = json.loads(kwargs_text)
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise ValueError("위치 인자는 배열, 키워드 인자는 객체여야 합니다.")
        except Exception as exc:
            st.error(f"JSON 입력 오류: {exc}")
            return

    if st.button("선택한 API 실행", type="primary", use_container_width=True):
        run_call(func, args, kwargs, f"{module_name}.{function_name}")


# -----------------------------------------------------------------------------
# API 목록
# -----------------------------------------------------------------------------
def render_api_inventory() -> None:
    rows: list[dict[str, Any]] = []
    for module_name, function_map in [("stock", STOCK_FUNCTIONS), ("bond", BOND_FUNCTIONS)]:
        for name, func in function_map.items():
            rows.append(
                {
                    "모듈": module_name,
                    "분류": category_of(name),
                    "함수": name,
                    "호출 형식": str(safe_signature(func) or "동적 인자"),
                    "설명": first_doc_line(func),
                }
            )
    inventory = pd.DataFrame(rows)
    query = st.text_input("함수명 또는 설명 검색")
    if query:
        mask = inventory.astype(str).apply(lambda col: col.str.contains(query, case=False, na=False)).any(axis=1)
        inventory = inventory[mask]
    st.metric("노출된 공개 함수 수", len(inventory))
    st.dataframe(inventory, use_container_width=True, hide_index=True, height=650)
    st.download_button(
        "API 목록 CSV 다운로드",
        inventory.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        "pykrx_api_list.csv",
        "text/csv",
        use_container_width=True,
    )


# -----------------------------------------------------------------------------
# 메인 화면
# -----------------------------------------------------------------------------
st.title("📊 PyKRX 통합 Streamlit 앱")
st.caption("주식·투자자 수급·지수·공매도·ETF/ETN/ELW·선물·채권 기능을 한 화면에서 조회합니다.")

with st.sidebar:
    st.header("실행 상태")
    local_package_path = getattr(stock, "__file__", "확인 불가")
    st.caption(f"PyKRX 위치: `{local_package_path}`")
    has_id = bool(os.getenv("KRX_ID"))
    has_pw = bool(os.getenv("KRX_PW"))
    if has_id and has_pw:
        st.success("KRX 로그인 환경변수 설정됨")
    else:
        st.warning("KRX 로그인 환경변수 미설정")
        st.caption("일부 API는 로그인 없이도 작동하지만, 인증 필요 기능은 실패할 수 있습니다.")
    with st.expander("Secrets 설정 예시"):
        st.code('KRX_ID = "아이디"\nKRX_PW = "비밀번호"', language="toml")
    st.divider()
    st.warning("조회 버튼을 반복해서 누르지 마세요. KRX 서버에서 과도한 호출을 제한할 수 있습니다.")
    if st.button("마지막 결과 지우기", use_container_width=True):
        for key in ["pykrx_result", "pykrx_result_title", "pykrx_call_text"]:
            st.session_state.pop(key, None)
        st.rerun()

main_tab, explorer_tab, inventory_tab, help_tab = st.tabs(
    ["쉬운 조회", "전체 API 실행기", "API 목록", "실행 안내"]
)

with main_tab:
    render_easy_query()
    render_result()

with explorer_tab:
    render_api_explorer()
    render_result()

with inventory_tab:
    render_api_inventory()

with help_tab:
    st.subheader("로컬 실행")
    st.code(
        """py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py""",
        language="powershell",
    )
    st.subheader("권장 폴더 구조")
    st.code(
        """pykrx-master/
├─ app.py
├─ requirements.txt
├─ pyproject.toml
├─ README.md
└─ pykrx/
   ├─ stock/
   ├─ bond/
   └─ website/""",
        language="text",
    )
    st.subheader("로그인이 필요한 경우")
    st.write("저장소 루트에 `.streamlit/secrets.toml` 파일을 만들고 아래처럼 작성하세요.")
    st.code('KRX_ID = "본인의_KRX_아이디"\nKRX_PW = "본인의_KRX_비밀번호"', language="toml")
    st.warning("`secrets.toml`은 GitHub에 올리지 말고 `.gitignore`에 추가하세요.")
