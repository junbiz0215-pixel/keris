"""
보육현황 대시보드 v2.0 — 유치원 | 어린이집 2탭 구조
Analytics Metric Flow Design System
출처: 데이터로 읽는 우리 교육 제6호 (교육부·KEDI, 2026.05.31) / 시각화 by KERIS
어린이집 원본 데이터: 2025년 12월말 기준 보육통계 Raw Data
"""
import json
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="보육현황 대시보드 | 제6호",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Analytics Metric Flow CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
:root{
  --bg:#F7F8F3;--sur:#FFFFFF;--soft:#F3F4F6;
  --pri:#16A34A;--dark:#14532D;
  --amb:#F59E0B;--amb-dk:#92400E;        /* 유치원 색상 */
  --txt:#111827;--mu:#6B7280;
  --bdr:#E5E7EB;--pill:#DCFCE7;
  --sha:0 18px 45px rgba(15,23,42,.04);--r:14px;
}
html,body,[data-testid="stApp"],[data-testid="stAppViewContainer"]
    {background:var(--bg)!important;}
[data-testid="stAppViewContainer"]>.main>.block-container
    {background:var(--bg)!important;max-width:1280px;padding:1.5rem 1.5rem 5rem;}
[data-testid="stHeader"]{background:var(--bg)!important;border-bottom:1px solid var(--bdr);}
[data-testid="stSidebar"]
    {background:var(--sur)!important;border-right:1px solid var(--bdr);}
[data-testid="stSidebar"] *{color:var(--txt)!important;}
[data-testid="stSidebar"] label
    {font-size:.68rem!important;font-weight:700!important;
     text-transform:uppercase!important;letter-spacing:.07em!important;color:var(--mu)!important;}
/* KPI */
.kpi{background:var(--sur);border-radius:var(--r);border:1px solid var(--bdr);
     box-shadow:var(--sha);padding:20px 18px 16px;height:100%;box-sizing:border-box;}
/* KPI 카드 5개 높이 균등 (열 stretch) */
[data-testid="stHorizontalBlock"]:has(.kpi){align-items:stretch;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]{display:flex;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]>[data-testid="stVerticalBlock"]{width:100%;}
.kpi-dk{background:var(--dark);border-radius:var(--r);padding:20px 18px 16px;}
.kpi-am{background:var(--amb-dk);border-radius:var(--r);padding:20px 18px 16px;}
.kl {font-size:.67rem;font-weight:700;text-transform:uppercase;
     letter-spacing:.07em;color:var(--mu);margin:0 0 10px;}
.klw{font-size:.67rem;font-weight:700;text-transform:uppercase;
     letter-spacing:.07em;color:rgba(255,255,255,.45);margin:0 0 10px;}
.kv {font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;
     color:var(--pri);line-height:1;letter-spacing:-.03em;margin:0 0 5px;}
.kvw{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;
     color:#FCD34D;line-height:1;letter-spacing:-.03em;margin:0 0 5px;}
.kva{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;
     color:var(--amb);line-height:1;letter-spacing:-.03em;margin:0 0 5px;}
.ks {font-size:.7rem;color:var(--mu);margin:0;}
.ksw{font-size:.7rem;color:rgba(255,255,255,.45);margin:0;}
.pill  {display:inline-block;background:var(--pill);color:var(--dark);font-size:.64rem;
        font-weight:700;border-radius:9999px;padding:3px 9px;margin-top:7px;}
.pill-g{background:#BBF7D0;color:#166534;}
.pill-a{background:#FEF3C7;color:#92400E;}
.pill-w{display:inline-block;background:rgba(255,255,255,.12);color:rgba(255,255,255,.8);
        font-size:.64rem;font-weight:700;border-radius:9999px;padding:3px 9px;margin-top:7px;}
/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"]
    {background:transparent!important;border-bottom:2px solid var(--bdr)!important;gap:0!important;}
[data-testid="stTabs"] [data-baseweb="tab"]
    {font-size:.9rem!important;font-weight:500!important;color:var(--mu)!important;
     border-radius:0!important;border-bottom:2px solid transparent!important;
     padding:10px 22px!important;}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"]
    {color:var(--pri)!important;font-weight:800!important;border-bottom:2px solid var(--pri)!important;}
/* Chart title */
.ct{font-size:.68rem;font-weight:700;text-transform:uppercase;
    letter-spacing:.07em;color:var(--mu);margin:0 0 8px;}
/* Section */
.sh{font-size:1rem;font-weight:700;color:var(--txt);letter-spacing:-.02em;margin:0 0 16px;}
/* Divider */
.dv{border:none;border-top:1px solid var(--bdr);margin:22px 0 18px;}
/* Dataframe */
[data-testid="stDataFrame"] thead th
    {background:var(--soft)!important;font-size:.67rem!important;font-weight:700!important;
     text-transform:uppercase!important;letter-spacing:.04em!important;color:var(--mu)!important;}
[data-testid="stDataFrame"]
    {border-radius:var(--r)!important;border:1px solid var(--bdr)!important;overflow:hidden!important;}
/* Buttons */
.stDownloadButton>button
    {background:var(--pri)!important;color:#fff!important;border:none!important;
     border-radius:9999px!important;font-weight:600!important;font-size:.83rem!important;
     padding:10px 24px!important;box-shadow:0 2px 12px rgba(22,163,74,.28)!important;}
[data-testid="stRadio"] label{font-size:.82rem!important;color:var(--mu)!important;}
[data-testid="stRadio"] label:has(input:checked){color:var(--pri)!important;font-weight:700!important;}
/* 지표 토글(segmented control) */
[data-testid="stSegmentedControl"] button{
  border-radius:9999px!important;font-size:.8rem!important;font-weight:600!important;}
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] button[kind="segmented_controlActive"]{
  background:var(--pri)!important;color:#fff!important;border-color:var(--pri)!important;}
/* 유형 선택 박스 버튼(pills) — 선택=초록 음영, 미선택=연회색 */
[data-testid="stPills"] button{
  border-radius:9px!important;font-size:.78rem!important;font-weight:600!important;
  border:1px solid var(--bdr)!important;background:#F3F4F6!important;color:#6B7280!important;
  margin:2px!important;}
[data-testid="stPills"] button[aria-checked="true"],
[data-testid="stPills"] button[kind="pillsActive"]{
  background:var(--pri)!important;color:#fff!important;border-color:var(--pri)!important;
  box-shadow:0 2px 8px rgba(22,163,74,.28)!important;}
/* AI box */
.ai-box{background:var(--sur);border-radius:var(--r);border:1px solid var(--bdr);
        box-shadow:var(--sha);padding:18px 22px;margin-top:14px;}
/* badge data note */
.data-badge{display:inline-flex;align-items:center;gap:6px;background:#EFF6FF;
            color:#1D4ED8;font-size:.7rem;font-weight:700;border-radius:9999px;
            padding:4px 12px;margin-bottom:12px;}
/* ── 모든 차트 등장 애니메이션 ───────────────────────────────────── */
@keyframes chartIn{
  0%   {opacity:0; transform:translateY(16px) scale(.97);}
  100% {opacity:1; transform:translateY(0)    scale(1);}
}
[data-testid="stPlotlyChart"]{
  animation:chartIn .6s cubic-bezier(.22,.61,.36,1) both;
}
@keyframes kpiIn{
  0%   {opacity:0; transform:translateY(10px);}
  100% {opacity:1; transform:translateY(0);}
}
.kpi,.kpi-dk,.kpi-am{animation:kpiIn .5s ease-out both;}
/* KPI 카드 순차 등장 */
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]:nth-child(1) .kpi{animation-delay:.02s;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]:nth-child(2) .kpi{animation-delay:.07s;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]:nth-child(3) .kpi{animation-delay:.12s;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]:nth-child(4) .kpi{animation-delay:.17s;}
[data-testid="stHorizontalBlock"]:has(.kpi) [data-testid="column"]:nth-child(5) .kpi{animation-delay:.22s;}
</style>
""", unsafe_allow_html=True)

# ── Design Tokens ─────────────────────────────────────────────────────────────
PRI, DARK, AMB, AMB_DK = "#16A34A", "#14532D", "#F59E0B", "#92400E"
PAGE_BG, TXT, MU, BDR  = "#F7F8F3", "#111827", "#6B7280", "#E5E7EB"
GREENS = ["#14532D","#15803D","#16A34A","#22C55E","#4ADE80","#86EFAC","#BBF7D0"]
AMBERS = ["#78350F","#92400E","#B45309","#D97706","#F59E0B","#FCD34D","#FEF3C7"]

KINDER_COLORS = {
    "국립":       "#14532D",
    "공립(단설)": "#15803D",
    "공립(병설)": "#22C55E",
    "사립(법인)": "#B45309",
    "사립(사인)": "#F59E0B",
}
ESTAB_COLORS = {"국공립": "#16A34A", "사립": "#F59E0B"}
POSITION_COLS = ["원장","원감","수석교사","보직교사","일반교사",
                 "특수교사","보건교사","영양교사","기간제/강사","사무직원"]
NURSERY_COLORS = {
    "국공립":    "#14532D","사회복지법인":"#15803D","법인・단체등":"#16A34A",
    "민간":      "#22C55E","가정":        "#4ADE80","협동":        "#86EFAC",
    "직장":      "#BBF7D0",
}

SIDO_COORDS = {
    "서울특별시":(37.5665,126.9780),"부산광역시":(35.1796,129.0756),
    "대구광역시":(35.8722,128.6014),"인천광역시":(37.4563,126.7052),
    "광주광역시":(35.1595,126.8526),"대전광역시":(36.3504,127.3845),
    "울산광역시":(35.5384,129.3114),"세종특별자치시":(36.4801,127.2882),
    "경기도":    (37.4138,127.5183),"강원특별자치도":(37.8228,128.1555),
    "충청북도":  (36.6357,127.4914),"충청남도":(36.5185,126.8006),
    "전북특별자치도":(35.7175,127.1530),"전라남도":(34.8161,126.4630),
    "경상북도":  (36.4919,128.8889),"경상남도":(35.4606,128.2132),
    "제주특별자치도":(33.4890,126.4983),
}

# 지도 라벨용 시도 약칭
SIDO_SHORT = {
    "서울특별시":"서울","부산광역시":"부산","대구광역시":"대구","인천광역시":"인천",
    "광주광역시":"광주","대전광역시":"대전","울산광역시":"울산","세종특별자치시":"세종",
    "경기도":"경기","강원특별자치도":"강원","충청북도":"충북","충청남도":"충남",
    "전북특별자치도":"전북","전라남도":"전남","경상북도":"경북","경상남도":"경남",
    "제주특별자치도":"제주",
}

# 단계구분도 색상 스케일
SCALE_GREEN = ["#DCFCE7", "#86EFAC", "#22C55E", "#16A34A", "#14532D"]
SCALE_AMBER = ["#FEF3C7", "#FDE68A", "#FBBF24", "#F59E0B", "#92400E"]

# 지표 정의: 라벨 → (집계컬럼, 단위포맷, 설명)
METRICS = {
    "재원 아동 수":   ("child", "{:,}명",   "현원"),
    "정원 충족률":    ("util",  "{:.1f}%",  "정원 대비 현원"),
    "시설 수":        ("fac",   "{:,}개",   "기관 수"),
    "교사 1인당 아동": ("cps",   "{:.2f}명", "교직원 1인당 담당"),
}

def sido_metric_agg(df: pd.DataFrame) -> pd.DataFrame:
    """시도별 전 지표 집계 (choropleth·해석 공용)."""
    g = (df.groupby("sido_name")
         .agg(fac=("facility_count","sum"), child=("child_count","sum"),
              cap=("capacity","sum"), staff=("staff_count","sum"))
         .reset_index())
    g["util"] = (g["child"] / g["cap"].clip(lower=1) * 100).round(1)
    g["cps"]  = (g["child"] / g["staff"].clip(lower=1)).round(2)
    return g

@st.cache_data
def load_geojson() -> dict:
    with open("skorea_sido.geojson", encoding="utf-8") as f:
        return json.load(f)

def cb(**kw):
    base = dict(paper_bgcolor=PAGE_BG, plot_bgcolor=PAGE_BG,
                font=dict(family="system-ui,-apple-system,sans-serif", color=TXT, size=10),
                margin=dict(t=16,b=36,l=4,r=4), showlegend=True)
    base.update(kw); return base


# ── OpenStreetMap 버블맵 (Plotly Scattermap · 토큰/API키 불필요) ─────────────
def osm_bubble_map(map_data: list, base_color: str, dark_color: str):
    """OpenStreetMap 타일 위에 시도별 버블 마커를 그린 Plotly 지도.

    - 버블 크기 = 아동 수
    - 버블 색상 = 정원 충족률 (90% 이상이면 주황 경고색)
    - 카카오 등 외부 API 키·도메인 등록이 전혀 필요 없음
    """
    if not map_data:
        return None
    lats   = [d["lat"]   for d in map_data]
    lons   = [d["lon"]   for d in map_data]
    childs = [d["child"] for d in map_data]
    utils  = [d["util"]  for d in map_data]
    names  = [d["name"]  for d in map_data]
    facs   = [d.get("fac", 0) for d in map_data]

    max_child = max(childs) if childs else 1
    sizes = [max(14, (c / max_child) ** 0.5 * 46 + 12) for c in childs]
    # 충족률 90%↑ 경고색, 그 외 기본색
    colors = ["#F59E0B" if u >= 90 else base_color for u in utils]

    custom = list(zip(childs, utils, facs))
    fig = go.Figure(go.Scattermap(
        lat=lats, lon=lons, mode="markers",
        marker=dict(size=sizes, color=colors, opacity=0.82),
        text=names, customdata=custom,
        hovertemplate=(
            "<b>%{text}</b><br>"
            "아동 수: %{customdata[0]:,}명<br>"
            "정원 충족률: %{customdata[1]:.1f}%<br>"
            "시설 수: %{customdata[2]:,}개소<extra></extra>"
        ),
    ))
    fig.update_layout(
        map=dict(style="open-street-map", center=dict(lat=36.3, lon=127.8), zoom=5.6),
        paper_bgcolor=PAGE_BG,
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        height=310,
        font=dict(family="system-ui,-apple-system,sans-serif", color=TXT, size=11),
    )
    return fig

def sido_choropleth(agg: pd.DataFrame, metric_col: str, label: str, fmt: str,
                    geojson: dict, scale: list, selected: str | None = None,
                    zoom: float = 4.5, height: int = 340):
    """시도 단계구분도 — 선택 지표로 색칠, 호버 풍부화, 부드러운 전환.
    zoom: 슬라이더로 조절되는 지도 확대 수준 / height: 세로 높이(한반도가 세로로 길어 크게)."""
    a = agg.copy()
    a["_disp"] = a[metric_col].map(lambda v: fmt.format(v))
    fig = px.choropleth_map(
        a, geojson=geojson, locations="sido_name",
        featureidkey="properties.sido_norm",
        color=metric_col, color_continuous_scale=scale,
        map_style="white-bg",   # 영문 라벨 없는 배경 → 한글 시도명만 표시
        center={"lat": 35.7, "lon": 127.8}, zoom=zoom, opacity=0.85,
        custom_data=["sido_name", "_disp", "fac", "child", "util", "cps"],
    )
    fig.update_traces(
        marker_line_width=0.8, marker_line_color="#9CA3AF",
        hovertemplate=("<b>%{customdata[0]}</b><br>"
                       + label + ": <b>%{customdata[1]}</b><br>"
                       "시설 %{customdata[2]:,}개 · 현원 %{customdata[3]:,}명<br>"
                       "충족률 %{customdata[4]:.1f}% · 교사1인당 %{customdata[5]:.2f}명"
                       "<extra></extra>"),
    )
    # 한글 시도명 라벨 레이어
    lab_lat, lab_lon, lab_txt = [], [], []
    for s in a["sido_name"]:
        if s in SIDO_COORDS:
            lab_lat.append(SIDO_COORDS[s][0])
            lab_lon.append(SIDO_COORDS[s][1])
            lab_txt.append(SIDO_SHORT.get(s, s))
    fig.add_trace(go.Scattermap(
        lat=lab_lat, lon=lab_lon, mode="text", text=lab_txt,
        textfont=dict(size=11, color="#111827",
                      family="system-ui,-apple-system,sans-serif"),
        hoverinfo="skip", showlegend=False, name="라벨",
    ))

    # 선택 시도 외곽선 강조
    if selected and selected in a["sido_name"].values:
        sel_feats = {"type": "FeatureCollection",
                     "features": [ft for ft in geojson["features"]
                                  if ft["properties"]["sido_norm"] == selected]}
        srow = a[a["sido_name"] == selected]
        fig.add_trace(go.Choroplethmap(
            geojson=sel_feats, locations=srow["sido_name"],
            featureidkey="properties.sido_norm", z=[1],
            showscale=False, colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker=dict(line=dict(width=3, color="#111827")),
            hoverinfo="skip",
        ))
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), height=height,
        paper_bgcolor=PAGE_BG,
        # 한국 영역으로 지도 고정 (한반도 bounding box 밖으로 못 벗어남)
        map=dict(bounds=dict(west=118.0, east=137.0, south=28.0, north=43.0)),
        coloraxis_colorbar=dict(title=dict(text=label, font=dict(size=10)),
                                len=0.72, thickness=10,
                                tickfont=dict(size=9, family="JetBrains Mono, monospace")),
        font=dict(family="system-ui,-apple-system,sans-serif", color=TXT, size=11),
        uirevision=f"z{zoom:.1f}",   # 줌 변경 시 뷰 재적용(슬라이더 반영)
        transition=dict(duration=350, easing="cubic-in-out"),
    )
    return fig


def capture_click(ev, chart_id: str, label_key: str = "label"):
    """plotly on_select 이벤트 → 변경 감지 후 active_insight 갱신.
    반환: (changed: bool, label). 클릭이 '바뀐 차트'만 active_insight를 차지(충돌 방지)."""
    sel = getattr(ev, "selection", None)
    pts = None
    if sel is not None:
        pts = sel.get("points") if isinstance(sel, dict) else getattr(sel, "points", None)
    lab = None
    if pts:
        # 여러 trace(라벨·외곽선 등) 중 유효 라벨을 가진 첫 포인트 선택
        for p in pts:
            cand = p.get(label_key) or p.get("location") or p.get("x") or p.get("y")
            if cand is not None:
                lab = cand
                break
    sig_key = f"_sig_{chart_id}"
    changed = (st.session_state.get(sig_key) != lab)
    st.session_state[sig_key] = lab
    if changed and lab is not None:
        st.session_state["active_insight"] = (chart_id, lab)
        return True, lab
    return False, lab


def race_figure(cats, vals, scale, fmt="{:,.0f}", unit="", n_steps=20, height=420):
    """독립형 '바 차트 레이스' (Plotly 프레임 애니메이션).
    - 막대가 0→값으로 순차 성장하며 정렬된 순위를 드러냄
    - 클릭 이벤트·크로스필터와 무관(격리), 축 범위 고정으로 깨짐 방지
    - ▶ 재생 버튼 + 진행 슬라이더 포함"""
    cats = list(cats); vals = [float(v) for v in vals]
    if not vals:
        return None
    vmax = max(vals) or 1
    def _bar(scaled):
        return go.Bar(
            x=scaled, y=cats, orientation="h",
            marker=dict(color=scaled, colorscale=scale, cmin=0, cmax=vmax, showscale=False),
            text=["<b>" + fmt.format(v) + unit + "</b>" for v in scaled],
            textposition="outside",
            textfont=dict(size=12, family="JetBrains Mono, monospace", color="#111827"),
            cliponaxis=False,
            hovertemplate="%{y}: %{text}<extra></extra>",
        )
    frames = []
    for i in range(n_steps + 1):
        t = i / n_steps
        te = 1 - (1 - t) ** 3                # ease-out
        frames.append(go.Frame(name=str(i), data=[_bar([v * te for v in vals])]))
    fig = go.Figure(data=frames[-1].data, frames=frames)     # 초기=완성 상태
    fig.update_layout(
        paper_bgcolor=PAGE_BG, plot_bgcolor=PAGE_BG, height=height,
        font=dict(family="system-ui,-apple-system,sans-serif", color=TXT, size=10),
        margin=dict(t=30, b=20, l=72, r=70),
        xaxis=dict(range=[0, vmax * 1.20], visible=False, fixedrange=True),
        yaxis=dict(autorange="reversed", fixedrange=True,
                   tickfont=dict(size=12, color="#111827"), ticklabelposition="outside",
                   automargin=True),
        showlegend=False,
        sliders=[dict(
            active=0, x=0.1, len=0.88, y=1.06, yanchor="bottom",
            pad=dict(t=0, b=0), currentvalue=dict(visible=False),
            tickcolor="#E5E7EB", font=dict(size=8),
            steps=[dict(method="animate", label="",
                        args=[[str(i)], dict(mode="immediate",
                              frame=dict(duration=0, redraw=True),
                              transition=dict(duration=0))]) for i in range(n_steps + 1)],
        )],
    )
    return fig


def token_stream(text, delay=0.014):
    for w in text.split(" "):
        yield w + " "
        time.sleep(delay)


# ── 데이터 로드 ───────────────────────────────────────────────────────────────
EXCEL_FILE  = "812451774932644958_붙임 4. 2025년 12월말 기준 보육통계 Raw Data(수정).xlsx"
KINDER_FILE = "2026년 기준 유치원 Raw Data.xlsx"
K_TYPES = ["국립", "공립(단설)", "공립(병설)", "사립(법인)", "사립(사인)"]

@st.cache_data
def load_kinder() -> pd.DataFrame:
    """2026년 기준 유치원 Raw Data — 시도 × 유형 단위로 통합."""
    # 시트1: 유형별 시설수
    s1 = pd.read_excel(KINDER_FILE, sheet_name="1", header=2)
    s1 = s1[s1["시도"].notna() & (s1["시도"] != "합 계")]
    fac = s1.melt(id_vars="시도", value_vars=K_TYPES,
                  var_name="facility_type", value_name="facility_count")

    # 시트2: 정원/현원/이용률 (시도 ffill + 지표 분리)
    s2 = pd.read_excel(KINDER_FILE, sheet_name="2", header=2)
    s2.columns = ["_", "시도", "지표", "계"] + K_TYPES
    s2["시도"] = s2["시도"].ffill()
    s2 = s2[s2["시도"] != "계"]
    cap   = (s2[s2["지표"] == "정원"]
             .melt(id_vars="시도", value_vars=K_TYPES,
                   var_name="facility_type", value_name="capacity"))
    child = (s2[s2["지표"] == "현원"]
             .melt(id_vars="시도", value_vars=K_TYPES,
                   var_name="facility_type", value_name="child_count"))

    # 시트3: 직위별 교직원 → 시도×유형 합계('계' 컬럼)
    s3 = pd.read_excel(KINDER_FILE, sheet_name="3", header=2)
    s3 = s3.rename(columns={"구분": "시도", "Unnamed: 2": "subcat", "계": "staff_count"})
    s3["시도"] = s3["시도"].ffill()
    staff = (s3[(s3["시도"] != "합계") & (s3["subcat"].isin(K_TYPES))]
             [["시도", "subcat", "staff_count"]]
             .rename(columns={"subcat": "facility_type"}))

    # 병합
    df = (fac.merge(cap,   on=["시도", "facility_type"])
              .merge(child, on=["시도", "facility_type"])
              .merge(staff, on=["시도", "facility_type"], how="left")
              .rename(columns={"시도": "sido_name"}))
    for c in ["facility_count", "capacity", "child_count", "staff_count"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["utilization_rate"] = (df["child_count"] / df["capacity"].clip(lower=1) * 100).round(1)
    df["child_per_staff"]  = (df["child_count"] / df["staff_count"].clip(lower=1)).round(2)
    df["estab"] = df["facility_type"].map(lambda t: "사립" if t.startswith("사립") else "국공립")
    return df.reset_index(drop=True)

@st.cache_data
def load_kinder_positions() -> pd.DataFrame:
    """시트3 — 시도 × 유형별 직위(원장·일반교사 등 10종) 교직원 수."""
    s3 = pd.read_excel(KINDER_FILE, sheet_name="3", header=2)
    s3 = s3.rename(columns={"구분": "sido_name", "Unnamed: 2": "facility_type"})
    s3["sido_name"] = s3["sido_name"].ffill()
    df = s3[(s3["sido_name"] != "합계") & (s3["facility_type"].isin(K_TYPES))].copy()
    keep = ["sido_name", "facility_type"] + POSITION_COLS
    df = df[keep]
    for c in POSITION_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df.reset_index(drop=True)

@st.cache_data
def load_childcare() -> pd.DataFrame:
    """Sheet '10' — 어린이집 기본 현황_현월 (2025.12.31)"""
    df_raw = pd.read_excel(EXCEL_FILE, sheet_name="10", header=4, dtype=str)
    df_raw.columns = ["sido_name","facility_type","facility_count",
                      "staff_count","capacity","child_count","util_raw"]
    # 시도명 forward-fill (계층 구조 정리)
    df_raw["sido_name"] = df_raw["sido_name"].ffill()
    # 합계 행 및 NaN 제거
    df = df_raw[
        df_raw["facility_type"].notna() &
        (~df_raw["facility_type"].isin(["합계","합 계"]))
    ].copy()
    df = df[~df["sido_name"].isin(["합계","합 계"])]
    for col in ["facility_count","staff_count","capacity","child_count","util_raw"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["utilization_rate"] = (df["util_raw"] * 100).round(1)
    df["child_per_staff"]  = (df["child_count"] / df["staff_count"].clip(1)).round(2)
    # 법인・단체등 표기 통일
    df["facility_type"] = df["facility_type"].str.replace("법인・단체등","법인·단체등")
    return df.drop(columns=["util_raw"]).reset_index(drop=True)

try:
    dk_raw = load_kinder()
    dk_pos = load_kinder_positions()
except Exception as e:
    st.error(f"유치원 데이터 로드 실패: {e}\n'{KINDER_FILE}' 파일을 확인해 주세요.")
    st.stop()

try:
    nc_raw = load_childcare()
    excel_loaded = True
except Exception as e:
    st.warning(f"Excel 파일 로드 실패 ({e}). childcare_data.csv로 대체합니다.")
    try:
        nc_raw = pd.read_csv("childcare_data.csv")
        nc_raw["utilization_rate"] = (nc_raw["child_count"]/nc_raw["capacity"]*100).round(1)
        nc_raw["child_per_staff"]  = (nc_raw["child_count"]/nc_raw["staff_count"].clip(1)).round(2)
        nc_raw["sido_name"] = nc_raw.get("sido_name", nc_raw.get("sido",""))
        excel_loaded = False
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다.")
        st.stop()


# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-size:.95rem;font-weight:800;color:#14532D;margin:0 0 2px;"
        "letter-spacing:-.02em;'>📊 대시보드 필터</p>"
        "<p style='font-size:.69rem;color:#6B7280;margin:0 0 14px;line-height:1.5;'>"
        "데이터로 읽는 우리 교육 제6호</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:0 0 14px;'>",
                unsafe_allow_html=True)

    # 공통 시도 필터 — 드롭다운 + 지도 클릭 동기화
    all_sidos = sorted(set(dk_raw["sido_name"].unique()) | set(nc_raw["sido_name"].unique()))
    sido_opts = ["전체"] + all_sidos
    # 이전 런의 지도 클릭을 위젯 생성 前 반영 (Streamlit 상태 규칙 준수)
    if st.session_state.get("_map_click"):
        clicked = st.session_state.pop("_map_click")
        if clicked in sido_opts:
            st.session_state["sido_dd"] = clicked
    if "sido_dd" not in st.session_state:
        st.session_state["sido_dd"] = "전체"
    sel_sido = st.selectbox("📍 시도 (공통)", sido_opts, key="sido_dd")
    st.caption("지도에서 시도를 클릭해도 선택됩니다")

    st.markdown("<p style='font-size:.68rem;font-weight:700;text-transform:uppercase;"
                "letter-spacing:.06em;color:#6B7280;margin:12px 0 5px;'>🏫 유치원 유형</p>",
                unsafe_allow_html=True)
    k_types_all = [t for t in K_TYPES if t in dk_raw["facility_type"].unique()]
    sel_k_types = st.pills("유치원 유형", k_types_all, selection_mode="multi",
                           default=k_types_all, label_visibility="collapsed",
                           key="ktypes_pills")

    st.markdown("<p style='font-size:.68rem;font-weight:700;text-transform:uppercase;"
                "letter-spacing:.06em;color:#6B7280;margin:12px 0 5px;'>🏠 어린이집 유형</p>",
                unsafe_allow_html=True)
    n_types_all = sorted(nc_raw["facility_type"].unique())
    sel_n_types = st.pills("어린이집 유형", n_types_all, selection_mode="multi",
                           default=n_types_all, label_visibility="collapsed",
                           key="ntypes_pills")

    st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:14px 0 10px;'>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:.75rem;color:#6B7280;margin:0;line-height:1.7;'>"
        "🏫 유치원: 2026년 기준<br>"
        "📊 어린이집: 2025년 12월말 기준</p>",
        unsafe_allow_html=True,
    )

# 한국 시도 GeoJSON
try:
    GEOJSON = load_geojson()
except Exception:
    GEOJSON = None


# ── 데이터 필터링 ─────────────────────────────────────────────────────────────
# 유형 필터만 적용(시도 무관) — 단계구분도는 항상 전국 맥락 유지
dk_full = dk_raw[dk_raw["facility_type"].isin(sel_k_types)] if sel_k_types else dk_raw.copy()
nc_full = nc_raw[nc_raw["facility_type"].isin(sel_n_types)] if sel_n_types else nc_raw.copy()

# 시도 + 유형 필터 (KPI·하위차트 드릴다운용)
dk = dk_full.copy()
nc = nc_full.copy()
if sel_sido != "전체":
    dk = dk[dk["sido_name"] == sel_sido]
    nc = nc[nc["sido_name"] == sel_sido]

region = sel_sido if sel_sido != "전체" else "전국"


# ── 페이지 헤더 ───────────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:.69rem;font-weight:700;text-transform:uppercase;"
    "letter-spacing:.09em;color:#16A34A;margin:0 0 5px;'>"
    "데이터로 읽는 우리 교육 제6호 · 교육부·KEDI · 2026.05.31 · 시각화 by KERIS</p>"
    "<h1 style='font-size:1.55rem;font-weight:800;color:#111827;"
    "letter-spacing:-.03em;margin:0 0 4px;line-height:1.2;'>"
    "안전하고 건강한 어린이집·유치원, "
    "<span style='color:#16A34A;'>행복한 우리 아이</span></h1>"
    "<p style='font-size:.78rem;color:#6B7280;margin:0;'>"
    f"선택 지역: <strong>{region}</strong></p>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:14px 0 0;'>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 탭 렌더러 — 단계구분도 · 동적 지표 · 차트별 반응형 RAG 해석
# ══════════════════════════════════════════════════════════════════════════════
def render_tab(cfg: dict):
    key        = cfg["key"]                 # "k" | "n"
    df         = cfg["df"]                  # 시도+유형 필터
    df_full    = cfg["df_full"]             # 유형만 필터(전국)
    types      = cfg["types"]               # 유형 순서
    colors     = cfg["colors"]
    scale      = cfg["scale"]
    accent     = cfg["accent"]
    unit_fac   = cfg["unit_fac"]            # 개원 | 개소
    unit_child = cfg["unit_child"]          # 유아 | 아동
    src        = cfg["src"]
    aux_kind   = cfg["aux_kind"]            # "position" | "cps"

    # ── 크로스필터(차트 클릭 연동) 상태 ──────────────────────────────────────
    xf_key  = f"xf_type_{key}"
    xf_type = st.session_state.get(xf_key)
    if xf_type is not None and xf_type not in types:
        xf_type = None
        st.session_state[xf_key] = None
    df_base = df                            # 도넛(전체 유형 구성)용 — 시도만 필터
    if xf_type:                             # 유형 클릭 시 → 다른 차트 모두 그 유형으로
        df      = df[df["facility_type"] == xf_type]
        df_full = df_full[df_full["facility_type"] == xf_type]

    def xf_pick_sido(name):                 # 시도 클릭 → 공통 시도 선택 토글
        st.session_state["_map_click"] = ("전체" if name == sel_sido else name)

    def xf_pick_type(t):                    # 유형 클릭 → 유형 크로스필터 토글
        st.session_state[xf_key] = (None if t == xf_type else t)

    st.markdown(f"<span class='data-badge'>📂 {src}</span>", unsafe_allow_html=True)

    # ── KPI 집계 ─────────────────────────────────────────────────────────────
    if df.empty:
        t_fac=t_child=t_cap=t_staff=0; t_util=t_cps=t_pub=0.0
    else:
        t_fac   = int(df["facility_count"].sum())
        t_child = int(df["child_count"].sum())
        t_cap   = int(df["capacity"].sum())
        t_staff = int(df["staff_count"].sum())
        t_util  = round(t_child/t_cap*100,1) if t_cap else 0.0
        t_cps   = round(t_child/t_staff,2)   if t_staff else 0.0
        if "estab" in df.columns:
            pub_c = df.loc[df["estab"]=="국공립","child_count"].sum()
        else:
            pub_c = df.loc[df["facility_type"]=="국공립","child_count"].sum()
        t_pub = round(pub_c/t_child*100,1) if t_child else 0.0

    util_pill = "pill-a" if t_util>=90 else "pill"
    util_lbl  = "여유 수준" if t_util<80 else "적정 수준" if t_util<90 else "과밀 우려"
    ka,kb,kc,kd,ke = st.columns(5)
    for col,label,val,sub,pill_t,pill_c in [
        (ka,f"{cfg['name']} 수 (시설)", f"{t_fac:,}",   f"{unit_fac} (필터 기준)", cfg["year"], "pill"),
        (kb,f"재원 {unit_child}",        f"{t_child:,}", "명",                     cfg["age"],  "pill"),
        (kc,"평균 정원 충족률",          f"{t_util:.1f}%","정원 대비 현원",         util_lbl,    util_pill),
        (kd,"국공립 비중",               f"{t_pub:.1f}%", f"재원{unit_child} 기준", "국공립/사립","pill-g"),
        (ke,f"교사 1인당 {unit_child}",  f"{t_cps:.1f}",  "명",                     "평균",       "pill"),
    ]:
        with col:
            st.markdown(f"""<div class='kpi'>
              <p class='kl'>{label}</p><p class='kv'>{val}</p>
              <p class='ks'>{sub}</p><span class='{pill_c}'>{pill_t}</span>
            </div>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
        return

    # ── 지표 선택 토글 버튼 (동적 전환) ──────────────────────────────────────
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    metric_label = st.segmented_control(
        "🎛 지도·차트 지표 선택", list(METRICS.keys()),
        default=list(METRICS.keys())[0], key=f"metric_{key}")
    if metric_label is None:                       # 토글 해제 시 기본값 유지
        metric_label = list(METRICS.keys())[0]
    mcol, mfmt, mdesc = METRICS[metric_label]

    # 연동 필터 상태 표시 + 초기화
    _fil = []
    if sel_sido != "전체": _fil.append(f"시도 = <b>{sel_sido}</b>")
    if xf_type:            _fil.append(f"유형 = <b>{xf_type}</b>")
    if _fil:
        fc1, fc2 = st.columns([4, 1])
        with fc1:
            st.markdown("<div style='background:#DCFCE7;border-radius:9999px;"
                        "padding:5px 14px;font-size:.74rem;color:#14532D;display:inline-block;"
                        "margin:4px 0;'>🔗 연동 필터: " + " · ".join(_fil) + "</div>",
                        unsafe_allow_html=True)
        with fc2:
            if st.button("필터 초기화", key=f"clr_{key}"):
                st.session_state["_map_click"] = "전체"
                st.session_state[xf_key] = None
                st.rerun()

    # 시도 단위 집계 (전국 17개 — 단계구분도/해석 공용)
    agg = sido_metric_agg(df_full)
    order = agg.sort_values(mcol, ascending=False).reset_index(drop=True)
    sido_lookup = {r["sido_name"]: r for _, r in agg.iterrows()}
    gtype = df_base.groupby("facility_type")["child_count"].sum().reindex(types).fillna(0)

    # ── 해설용 통계 + 해석 함수 (패널보다 먼저 정의) ─────────────────────────
    top_t = gtype.idxmax() if gtype.sum()>0 else "-"
    top_t_pct = round(gtype.max()/gtype.sum()*100,1) if gtype.sum()>0 else 0
    top_r = order.iloc[0]; low_r = order.iloc[-1]

    def insight(chart, lab):
        if chart == "choro":
            base = (f"**[{metric_label} · 지역 분포]** 전국 {len(agg)}개 시도 중 "
                    f"**{top_r['sido_name']}**가 {mfmt.format(top_r[mcol])}로 가장 높고, "
                    f"**{low_r['sido_name']}**가 {mfmt.format(low_r[mcol])}로 가장 낮습니다. ")
            if lab and lab in sido_lookup:
                rk = int(order.index[order['sido_name']==lab][0]) + 1
                base += (f"클릭하신 **{lab}**의 {metric_label}은(는) "
                         f"**{mfmt.format(sido_lookup[lab][mcol])}**로 전국 {rk}위입니다.")
            return base
        if chart == "donut":
            base = (f"**[설립유형 구성]** {region} 재원{unit_child}는 "
                    f"**{top_t}**({top_t_pct}%)가 가장 많습니다. ")
            if lab and lab in gtype.index and gtype.sum()>0:
                base += (f"선택하신 **{lab}**는 "
                         f"{round(gtype[lab]/gtype.sum()*100,1)}%"
                         f"({int(gtype[lab]):,}명)를 차지합니다.")
            return base
        if chart == "stack":
            base = f"**[시도별 유형 분포]** 재원{unit_child} 최다 지역은 **{top_r['sido_name']}**입니다. "
            if lab and lab in sido_lookup:
                base += f"**{lab}**의 총 재원은 {int(sido_lookup[lab]['child']):,}명입니다."
            return base
        if chart == "util":
            base = "**[시도별 정원 충족률]** 충족률이 높을수록 시설 포화에 가깝습니다. "
            if lab and lab in sido_lookup:
                base += f"**{lab}**의 정원 충족률은 {sido_lookup[lab]['util']:.1f}%입니다."
            return base
        if chart == "aux":
            if aux_kind == "position":
                base = "**[직위별 교직원]** 일반교사가 보육·교육 인력의 주축을 이룹니다. "
                if lab:
                    base += f"선택하신 **{lab}** 직위의 규모를 막대에서 확인할 수 있습니다."
            else:
                base = "**[시도별 교사 1인당 아동]** 값이 낮을수록 보육 여건이 양호합니다. "
                if lab and lab in sido_lookup:
                    base += f"**{lab}**의 교사 1인당 아동은 {sido_lookup[lab]['cps']:.2f}명입니다."
            return base
        # ── 종합 분석 (최소 3문장 이상, 실시간 수치 바인딩) ──────────────────
        if t_child == 0:
            return (f"**[{region} 종합 분석]**\n\n현재 필터 조건에서는 재원{unit_child}가 "
                    f"집계되지 않습니다. 사이드바 또는 연동 필터를 조정해 주세요.\n\n"
                    f"👆 지도·도넛·막대를 클릭하면 항목별 맞춤 해석으로 전환됩니다.")
        util_eval = ("정원 대비 수요가 매우 높아 시설 포화·대기 우려가 있는" if t_util >= 90
                     else "수요와 공급이 비교적 균형을 이루는" if t_util >= 80
                     else "정원에 여유가 있는")
        cps_eval  = ("매우 양호한" if t_cps <= 4 else "양호한" if t_cps <= 6
                     else "다소 높아 교원 확충 검토가 필요한")
        pub_eval  = ("공공보육 기반이 탄탄한" if t_pub >= 45
                     else "공공보육 확충 여지가 큰" if t_pub < 30
                     else "공공보육을 점진적으로 확대 중인")
        gap = round(top_r[mcol] / max(low_r[mcol], 1e-9), 1) if low_r[mcol] else None
        gap_txt = (f"최고({top_r['sido_name']})와 최저({low_r['sido_name']}) 지역 간 약 "
                   f"**{gap:.1f}배**의 격차가 존재합니다" if gap and gap >= 1.5
                   else f"**{top_r['sido_name']}**가 가장 높고 **{low_r['sido_name']}**가 가장 낮습니다")
        return (
            f"**[{region} 종합 분석]**\n\n"
            f"① **규모** — {region}에는 총 **{t_fac:,}{unit_fac}**의 {cfg['name']}에서 "
            f"**{t_child:,}명**의 {unit_child}가 재원 중이며, 정원 충족률 **{t_util:.1f}%**로 "
            f"{util_eval} 상태입니다.\n\n"
            f"② **구성** — 설립유형 중 **{top_t}**가 재원{unit_child}의 **{top_t_pct}%**로 가장 크며, "
            f"국공립 비중은 **{t_pub:.1f}%**로 {pub_eval} 수준입니다.\n\n"
            f"③ **격차·여건** — {metric_label} 기준 {gap_txt}. 교직원 1인당 담당 {unit_child} 수는 "
            f"**{t_cps:.1f}명**으로 보육·교육 여건은 {cps_eval} 편입니다.\n\n"
            f"④ **시사점** — 수요가 집중된 지역의 정원 조정과 국공립 인프라 확충, "
            f"교원 처우·배치 개선이 균형 있는 보육 환경의 핵심 과제로 분석됩니다.\n\n"
            f"👆 지도·도넛·막대를 클릭하면 항목별 맞춤 해석으로 전환됩니다.")

    # 현재 활성 해석 결정
    ai = st.session_state.get("active_insight")
    if ai and isinstance(ai, tuple) and ai[0].startswith(key + "_"):
        chart_base, clab = ai[0][len(key)+1:], ai[1]
    else:
        chart_base, clab = "summary", None
    ins_text = insight(chart_base, clab)
    _isk = f"_ins_{key}"
    _cur = (chart_base, clab, metric_label, region)
    do_stream = (st.session_state.get(_isk) != _cur)
    st.session_state[_isk] = _cur

    # ── Row 1: 단계구분도(세로형) + 🤖 AI 해석 패널(우측 고정) ──────────────
    c1, c2 = st.columns([1.5, 1.6])

    with c1:
        # 지도 제목 + 크기 조절 슬라이더(범례 옆 bar)
        th, ts = st.columns([2.3, 1])
        with th:
            st.markdown(f"<p class='ct' style='margin-top:6px;'>"
                        f"시도별 {metric_label} — 단계구분도 (클릭 시 선택·해석)</p>",
                        unsafe_allow_html=True)
        with ts:
            map_zoom = st.slider("🔍 지도 크기", 3.0, 7.0,
                                 st.session_state.get(f"zoom_{key}", 4.5), 0.1,
                                 key=f"zoom_{key}")
        if GEOJSON is not None:
            sel = sel_sido if sel_sido != "전체" else None
            fig_choro = sido_choropleth(agg, mcol, metric_label, mfmt, GEOJSON, scale, sel,
                                        zoom=map_zoom, height=340)
            ev = st.plotly_chart(fig_choro, use_container_width=True,
                                 key=f"choro_{key}", on_select="rerun",
                                 config={"scrollZoom": False, "displayModeBar": False,
                                         "doubleClick": False, "responsive": True})
            chg, loc = capture_click(ev, f"{key}_choro", label_key="location")
            if chg and loc:
                xf_pick_sido(loc)           # 지도 클릭 → 시도 연동 필터
                st.rerun()
            st.caption(f"색상 = {metric_label} · 클릭 → 시도 연동 + 우측 해석 · 호버 → 상세")
        else:
            st.info("GeoJSON 로드 실패 — 막대 차트로 대체합니다.")
            bar = order.sort_values(mcol)
            fig_b = go.Figure(go.Bar(x=bar[mcol], y=bar["sido_name"], orientation="h",
                                     marker_color=accent))
            fig_b.update_layout(**cb(showlegend=False, height=520))
            st.plotly_chart(fig_b, use_container_width=True, key=f"choro_{key}",
                            config={"responsive": True})

    with c2:
        st.markdown("<p style='font-size:.69rem;font-weight:700;text-transform:uppercase;"
                    "letter-spacing:.08em;color:#16A34A;margin:0 0 4px;'>"
                    "🤖 AI 데이터 해석</p>", unsafe_allow_html=True)
        with st.container(height=380, border=True):
            with st.chat_message("assistant", avatar="🤖"):
                if do_stream:
                    try:    st.write_stream(token_stream(ins_text))
                    except: st.markdown(ins_text)
                else:
                    st.markdown(ins_text)

    # ── Row 2: 설립유형 도넛 + 시도별 유형별 누적막대 ───────────────────────
    st.markdown("<hr class='dv'>", unsafe_allow_html=True)
    cdn, r1 = st.columns([1.2, 2])

    with cdn:
        st.markdown("<p class='ct'>설립유형별 재원 구성 (클릭 해석)</p>",
                    unsafe_allow_html=True)
        _dn_colors = [colors.get(t,"#ccc") for t in gtype.index]
        _pull = [0.12 if (xf_type and t == xf_type) else 0 for t in gtype.index]
        fig_dn = go.Figure(go.Pie(
            labels=gtype.index, values=gtype.values, hole=0.55, sort=False,
            pull=_pull, marker_colors=_dn_colors, textinfo="percent", textfont_size=10,
            hovertemplate="<b>%{label}</b><br>%{value:,}명 (%{percent})<extra></extra>"))
        fig_dn.update_layout(
            annotations=[dict(text=f"<b>{int(gtype.sum()):,}</b><br>명",
                              x=0.5,y=0.5,font=dict(size=13,family="JetBrains Mono,monospace"),
                              showarrow=False)],
            legend=dict(orientation="h",y=-0.12,x=0.5,xanchor="center",font=dict(size=8)),
            **cb(height=320,margin=dict(t=10,b=40,l=4,r=4)),
        )
        ev_dn = st.plotly_chart(fig_dn, use_container_width=True,
                                key=f"donut_{key}", on_select="rerun",
                                config={"displayModeBar": False, "responsive": True})
        _chg, _lab = capture_click(ev_dn, f"{key}_donut", label_key="label")
        if _chg:
            if _lab in types:
                xf_pick_type(_lab)          # 유형 클릭 → 유형 연동 필터
            st.rerun()

    with r1:
        st.markdown(f"<p class='ct'>시도별 설립유형별 재원{unit_child} 수 (클릭 → 시도 연동)</p>",
                    unsafe_allow_html=True)
        piv = df_full.groupby(["sido_name","facility_type"])["child_count"].sum().reset_index()
        so_order = (piv.groupby("sido_name")["child_count"].sum()
                    .sort_values(ascending=False).index.tolist())
        fig_st = go.Figure()
        for ft in types:
            sub = piv[piv["facility_type"]==ft].set_index("sido_name")
            yv = [sub["child_count"].get(s,0) for s in so_order]
            fig_st.add_trace(go.Bar(name=ft, x=so_order, y=yv,
                marker_color=colors.get(ft,"#ccc"),
                hovertemplate=f"{ft}: %{{y:,}}명<extra></extra>"))
        fig_st.update_layout(
            barmode="stack", bargap=0.42, hovermode="x unified",
            xaxis=dict(showgrid=False,zeroline=False,tickangle=-25,tickfont=dict(size=8),
                       showspikes=True,spikethickness=1,spikecolor="#9CA3AF",spikedash="dot"),
            yaxis=dict(showgrid=False,zeroline=False,tickformat=","),
            legend=dict(orientation="h",y=1.04,x=0.5,xanchor="center",font=dict(size=8)),
            **cb(height=300,margin=dict(t=10,b=30,l=4,r=4)),
        )
        ev_st = st.plotly_chart(fig_st, use_container_width=True,
                                key=f"stack_{key}", on_select="rerun",
                                config={"displayModeBar": False, "responsive": True})
        _chg, _lab = capture_click(ev_st, f"{key}_stack", label_key="x")
        if _chg:
            if _lab in so_order:
                xf_pick_sido(_lab)          # 막대 시도 클릭 → 시도 연동
            st.rerun()

    # ── Row 3: 보조차트 + 시도별 충족률 ──────────────────────────────────────
    st.markdown("<hr class='dv'>", unsafe_allow_html=True)
    r2, r3 = st.columns([2, 2])

    with r2:
        aux_id = f"{key}_aux"
        aux_sido_cats = []                  # 시도 라벨이면 클릭 시 시도 연동
        if aux_kind == "position":
            st.markdown("<p class='ct'>직위별 교직원 구성</p>", unsafe_allow_html=True)
            dp = dk_pos.copy()
            if sel_sido != "전체": dp = dp[dp["sido_name"]==sel_sido]
            if sel_k_types:        dp = dp[dp["facility_type"].isin(sel_k_types)]
            ps = dp[POSITION_COLS].sum().sort_values()
            ps = ps[ps>0]
            fig_ax = go.Figure(go.Bar(x=ps.values, y=list(ps.index), orientation="h",
                marker=dict(color=list(ps.values), colorscale=scale, showscale=False),
                text=[f"{int(v):,}" for v in ps.values],
                textposition="outside", textfont=dict(size=8),
                hovertemplate="%{y}: %{x:,}명<extra></extra>"))
        else:  # cps — 시도별 교사 1인당
            st.markdown("<p class='ct'>시도별 교사 1인당 아동 수 (클릭 → 시도 연동)</p>",
                        unsafe_allow_html=True)
            cpsd = agg.sort_values("cps")
            aux_sido_cats = list(cpsd["sido_name"])
            fig_ax = go.Figure(go.Bar(x=cpsd["cps"], y=cpsd["sido_name"], orientation="h",
                marker=dict(color=list(cpsd["cps"]), colorscale=scale, showscale=False),
                text=[f"{v:.2f}" for v in cpsd["cps"]],
                textposition="outside", textfont=dict(size=8),
                hovertemplate="%{y}: %{x:.2f}명<extra></extra>"))
        fig_ax.update_layout(
            xaxis=dict(showgrid=False,zeroline=False,visible=False),
            yaxis=dict(showgrid=False,zeroline=False,tickfont=dict(size=8)),
            **cb(showlegend=False,height=300,margin=dict(t=6,b=10,l=4,r=55)),
        )
        ev_ax = st.plotly_chart(fig_ax, use_container_width=True,
                                key=aux_id, on_select="rerun",
                                config={"displayModeBar": False, "responsive": True})
        _chg, _lab = capture_click(ev_ax, aux_id, label_key="y")
        if _chg:
            if _lab in aux_sido_cats:
                xf_pick_sido(_lab)          # 교사1인당(시도) 클릭 → 시도 연동
            st.rerun()

    with r3:
        st.markdown("<p class='ct'>시도별 정원 충족률 (%) (클릭 → 시도 연동)</p>",
                    unsafe_allow_html=True)
        utd = agg.sort_values("util")
        util_cats = list(utd["sido_name"])
        fig_u = go.Figure(go.Bar(x=utd["util"], y=utd["sido_name"], orientation="h",
            marker=dict(color=list(utd["util"]), colorscale=scale, showscale=False),
            text=[f"{v:.1f}%" for v in utd["util"]],
            textposition="outside", textfont=dict(size=8),
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
        fig_u.update_layout(
            xaxis=dict(showgrid=False,zeroline=False,visible=False),
            yaxis=dict(showgrid=False,zeroline=False,tickfont=dict(size=8)),
            **cb(showlegend=False,height=300,margin=dict(t=6,b=10,l=4,r=50)),
        )
        _chg, _lab = capture_click(st.plotly_chart(fig_u, use_container_width=True,
                key=f"util_{key}", on_select="rerun",
                config={"displayModeBar": False, "responsive": True}),
                f"{key}_util", label_key="y")
        if _chg:
            if _lab in util_cats:
                xf_pick_sido(_lab)          # 충족률(시도) 클릭 → 시도 연동
            st.rerun()

    # ── 🎬 움직이는 차트 (바 차트 레이스 · 격리·접이식) ──────────────────────
    st.markdown("<hr class='dv'>", unsafe_allow_html=True)
    with st.expander(f"🎬 움직이는 차트 — 시도별 {metric_label} 레이스 (자동 재생·반복)",
                     expanded=True):
        n_steps = 22
        race_df = agg.sort_values(mcol, ascending=False)
        race_labels = race_df["sido_name"].map(lambda s: SIDO_SHORT.get(s, s))
        fig_race = race_figure(
            race_labels, race_df[mcol], scale,
            fmt=("{:,.0f}" if mcol in ("child", "fac") else "{:.1f}"),
            unit=("%" if mcol == "util" else ""), n_steps=n_steps, height=440)
        if fig_race is not None:
            fig_json = fig_race.to_json()
            html = (
                "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>"
                "<style>body{margin:0;background:#F7F8F3;}#r{width:100%;}</style>"
                "</head><body><div id='r'></div><script>"
                "var fig=" + fig_json + ";"
                "Plotly.newPlot('r',fig.data,fig.layout,"
                "{displayModeBar:false,responsive:true})"
                ".then(function(){return Plotly.addFrames('r',fig.frames);})"
                ".then(function(){"
                "function loop(){Plotly.animate('r',null,{frame:{duration:55,redraw:true},"
                "transition:{duration:45,easing:'cubic-out'},mode:'immediate'});}"
                "loop();setInterval(loop,4500);"
                "});"
                "</script></body></html>"
            )
            components.html(html, height=470, scrolling=False)
            st.caption("막대가 0에서 실제값까지 자동으로 성장하며(약 4.5초마다 반복) 시도 순위가 드러납니다. "
                       "상단 지표 토글로 레이스 대상을 바꿀 수 있습니다.")
        else:
            st.info("표시할 데이터가 없습니다.")

    # ── 데이터 테이블 & 다운로드 ──────────────────────────────────────────────
    st.markdown("<hr class='dv'>", unsafe_allow_html=True)
    st.markdown(f"<p class='ct'>원본 데이터 — {cfg['name']} 현황</p>", unsafe_allow_html=True)
    disp = (df[["sido_name","facility_type","facility_count","capacity",
                "child_count","staff_count","utilization_rate","child_per_staff"]]
            .rename(columns={"sido_name":"시도","facility_type":"유형",
                             "facility_count":"시설수","capacity":"정원","child_count":"현원",
                             "staff_count":"교직원","utilization_rate":"충족률(%)",
                             "child_per_staff":"교사1인당"})
            .sort_values(["시도","유형"]).reset_index(drop=True))
    st.dataframe(disp, use_container_width=True, height=260, column_config={
        "시설수":   st.column_config.NumberColumn(format=f"%d {unit_fac}"),
        "정원":     st.column_config.NumberColumn(format="%d 명"),
        "현원":     st.column_config.NumberColumn(format="%d 명"),
        "교직원":   st.column_config.NumberColumn(format="%d 명"),
        "충족률(%)":st.column_config.ProgressColumn(format="%.1f%%",min_value=0,max_value=120),
        "교사1인당":st.column_config.NumberColumn(format="%.2f 명"),
    })
    st.download_button(label=f"CSV 다운로드 — {cfg['name']} {region}",
        data=disp.to_csv(index=False,encoding="utf-8-sig"),
        file_name=f"{cfg['name']}_현황_{region}.csv", mime="text/csv", key=f"dl_{key}")


# ══════════════════════════════════════════════════════════════════════════════
# 메인 탭 — 유치원 | 어린이집
# ══════════════════════════════════════════════════════════════════════════════
tab_k, tab_n = st.tabs(["🏫  유치원 (Kindergarten)", "🏠  어린이집 (Nursery)"])

with tab_k:
    render_tab(dict(
        key="k", name="유치원", df=dk, df_full=dk_full,
        types=[t for t in K_TYPES if t in dk_full["facility_type"].unique()],
        colors=KINDER_COLORS, scale=SCALE_AMBER, accent=AMB, dark=DARK,
        unit_fac="개원", unit_child="유아", aux_kind="position",
        year="2026년 기준", age="유아기 3~5세",
        src="2026년 기준 유치원 Raw Data (실제 데이터 · 17개 시도)",
    ))

with tab_n:
    src_n = ("2025년 12월말 기준 보육통계 Raw Data (실제 데이터)"
             if excel_loaded else "childcare_data.csv (대체 데이터)")
    nz_types = [t for t in ["국공립","사회복지법인","법인·단체등","민간","가정","협동","직장"]
                if t in nc_full["facility_type"].unique()]
    render_tab(dict(
        key="n", name="어린이집", df=nc, df_full=nc_full,
        types=nz_types,
        colors=NURSERY_COLORS, scale=SCALE_GREEN, accent=PRI, dark=DARK,
        unit_fac="개소", unit_child="아동", aux_kind="cps",
        year="2025.12 기준", age="영유아 0~5세", src=src_n,
    ))
