import streamlit as st
import sys
import tempfile
from pathlib import Path

VENV_SITE_PACKAGES = (
    Path(__file__).resolve().parent
    / "venv"
    / "lib"
    / f"python{sys.version_info.major}.{sys.version_info.minor}"
    / "site-packages"
)
if VENV_SITE_PACKAGES.exists():
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

from search import AudioSearchEngine

st.set_page_config(page_title="Sample Search", page_icon="🎵", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] { background: #f5f4f0; }
[data-testid="stHeader"]           { background: transparent; display: none !important; }
[data-testid="stSidebar"]          { display: none; }
section.main > div                 { padding-top: 0 !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stRadio"] { display: none !important; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; }

html, body, [class*="css"] {
    font-family: "Inter", system-ui, sans-serif;
    color: #1a1916;
}

/* ── shell ── */
.ss-shell {
    max-width: 740px;
    margin: 0 auto;
    padding: 1.75rem 1.5rem 6rem;
}

/* ── header ── */
.ss-header { margin-bottom: 2rem; }

.ss-wave {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 28px;
    margin-bottom: 1rem;
}
.ss-bar {
    width: 4px;
    border-radius: 2px;
    background: #b07d1e;
    animation: pulse 1.6s ease-in-out infinite;
}
.ss-bar:nth-child(1)  { height: 6px;  animation-delay: 0.00s; }
.ss-bar:nth-child(2)  { height: 16px; animation-delay: 0.12s; }
.ss-bar:nth-child(3)  { height: 10px; animation-delay: 0.24s; }
.ss-bar:nth-child(4)  { height: 24px; animation-delay: 0.06s; }
.ss-bar:nth-child(5)  { height: 14px; animation-delay: 0.18s; }
.ss-bar:nth-child(6)  { height: 20px; animation-delay: 0.30s; }
.ss-bar:nth-child(7)  { height: 8px;  animation-delay: 0.10s; }
.ss-bar:nth-child(8)  { height: 18px; animation-delay: 0.22s; }
.ss-bar:nth-child(9)  { height: 12px; animation-delay: 0.04s; }
.ss-bar:nth-child(10) { height: 22px; animation-delay: 0.16s; }
.ss-bar:nth-child(11) { height: 6px;  animation-delay: 0.28s; }
.ss-bar:nth-child(12) { height: 14px; animation-delay: 0.08s; }

@keyframes pulse {
    0%, 100% { opacity: 0.25; transform: scaleY(0.6); }
    50%       { opacity: 0.9;  transform: scaleY(1.0); }
}

.ss-eyebrow {
    font-size: 10px;
    font-family: "JetBrains Mono", monospace;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b07d1e;
    margin-bottom: 0.4rem;
}
.ss-title {
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.025em;
    line-height: 1.2;
    color: #1a1916;
    margin-bottom: 0.4rem;
}
.ss-sub {
    font-size: 14px;
    color: #7a7668;
    font-weight: 400;
}

/* ── divider ── */
.ss-divider {
    height: 1px;
    background: #e2e0d8;
    margin: 1.75rem 0;
}

/* ── input card ── */
.ss-card {
    background: #ffffff;
    border: 1px solid #e2e0d8;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* ── quick tags ── */
.ss-tags-label {
    font-size: 10px;
    font-family: "JetBrains Mono", monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #b8b4a4;
    margin: 1.1rem 0 0.6rem;
}

/* ── waveform loader ── */
.ss-waveform-loader {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 2.5rem 0 2rem;
}
.ss-wl-bar {
    width: 5px;
    border-radius: 3px;
    background: #d4a843;
    animation: wl-bounce 1.1s ease-in-out infinite;
}
.ss-wl-bar:nth-child(1)  { height: 10px; animation-delay: 0.00s; }
.ss-wl-bar:nth-child(2)  { height: 20px; animation-delay: 0.08s; }
.ss-wl-bar:nth-child(3)  { height: 32px; animation-delay: 0.16s; }
.ss-wl-bar:nth-child(4)  { height: 18px; animation-delay: 0.24s; }
.ss-wl-bar:nth-child(5)  { height: 40px; animation-delay: 0.10s; }
.ss-wl-bar:nth-child(6)  { height: 24px; animation-delay: 0.18s; }
.ss-wl-bar:nth-child(7)  { height: 48px; animation-delay: 0.04s; }
.ss-wl-bar:nth-child(8)  { height: 28px; animation-delay: 0.22s; }
.ss-wl-bar:nth-child(9)  { height: 44px; animation-delay: 0.12s; }
.ss-wl-bar:nth-child(10) { height: 20px; animation-delay: 0.28s; }
.ss-wl-bar:nth-child(11) { height: 36px; animation-delay: 0.06s; }
.ss-wl-bar:nth-child(12) { height: 16px; animation-delay: 0.20s; }
.ss-wl-bar:nth-child(13) { height: 42px; animation-delay: 0.14s; }
.ss-wl-bar:nth-child(14) { height: 22px; animation-delay: 0.26s; }
.ss-wl-bar:nth-child(15) { height: 30px; animation-delay: 0.02s; }
.ss-wl-bar:nth-child(16) { height: 14px; animation-delay: 0.30s; }
.ss-wl-bar:nth-child(17) { height: 38px; animation-delay: 0.09s; }
.ss-wl-bar:nth-child(18) { height: 26px; animation-delay: 0.17s; }
.ss-wl-bar:nth-child(19) { height: 46px; animation-delay: 0.05s; }
.ss-wl-bar:nth-child(20) { height: 12px; animation-delay: 0.25s; }

@keyframes wl-bounce {
    0%, 100% { transform: scaleY(0.25); opacity: 0.3; }
    50%       { transform: scaleY(1.0);  opacity: 1.0; }
}

.ss-waveform-caption {
    text-align: center;
    font-size: 12px;
    font-family: "JetBrains Mono", monospace;
    color: #b8b4a4;
    letter-spacing: 0.08em;
    padding-bottom: 1rem;
}

/* ── results header ── */
.ss-results-hdr {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin: 2rem 0 1rem;
}
.ss-results-label {
    font-size: 10px;
    font-family: "JetBrains Mono", monospace;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b07d1e;
}
.ss-results-count {
    font-size: 11px;
    font-family: "JetBrains Mono", monospace;
    color: #b8b4a4;
}

/* ── result card ── */
.ss-result {
    position: relative;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid #e2e0d8;
    border-radius: 14px;
    padding: 1rem 1.25rem 0.85rem;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.1s, border-color 0.2s;
}
.ss-result:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.09);
    transform: translateY(-1px);
    border-color: #d0cdc3;
}
.ss-result-stripe {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.ss-result-top {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}
.ss-result-num {
    font-size: 10px;
    font-family: "JetBrains Mono", monospace;
    color: #c8c4b4;
    min-width: 18px;
    text-align: right;
    font-weight: 500;
    flex-shrink: 0;
}
.ss-result-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
    border: 1px solid rgba(0,0,0,0.06);
}
.ss-result-info { flex: 1; min-width: 0; }
.ss-result-name {
    font-size: 13.5px;
    font-weight: 500;
    color: #1a1916;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
}
.ss-result-sub {
    font-size: 11px;
    font-family: "JetBrains Mono", monospace;
    color: #a8a498;
    display: flex;
    align-items: center;
    gap: 10px;
}
.ss-score-badge { flex-shrink: 0; text-align: right; }
.ss-score-num {
    font-size: 18px;
    font-family: "JetBrains Mono", monospace;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 2px;
}
.ss-score-lbl {
    font-size: 9px;
    font-family: "JetBrains Mono", monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b8b4a4;
}

.tier-high .ss-score-num   { color: #b07d1e; }
.tier-high .ss-result-stripe { background: #d4a843; }
.tier-high { border-color: #eddfa8; background: #fdfbf4; }

.tier-med  .ss-score-num   { color: #1e8f6a; }
.tier-med  .ss-result-stripe { background: #2db58a; }
.tier-med  { border-color: #b3ddd0; background: #f4fcf9; }

.tier-low  .ss-score-num   { color: #8a8678; }
.tier-low  .ss-result-stripe { background: #c8c4b4; }

/* ── empty / error ── */
.ss-empty { text-align: center; padding: 3.5rem 0; }
.ss-empty-icon { font-size: 32px; display: block; margin-bottom: 10px; opacity: 0.25; }
.ss-empty-text { font-size: 13px; color: #b8b4a4; }

.ss-error {
    background: #fff5f5;
    border: 1px solid #f5b8b8;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    color: #b83232;
    font-size: 13px;
}

/* ── streamlit overrides ── */
[data-testid="stTextInput"] input {
    background: #f9f8f5 !important;
    border: 1px solid #e2e0d8 !important;
    border-radius: 8px !important;
    color: #1a1916 !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    font-family: "Inter", sans-serif !important;
    caret-color: #b07d1e !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #d4a843 !important;
    box-shadow: 0 0 0 3px rgba(180,130,50,0.1) !important;
    outline: none !important;
    background: #ffffff !important;
}
[data-testid="stTextInput"] input::placeholder { color: #c8c4b4 !important; }
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stFileUploaderDropzone"] {
    background: #f9f8f5 !important;
    border: 1.5px dashed #d8d4c8 !important;
    border-radius: 10px !important;
    transition: all 0.15s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #d4a843 !important;
    background: #fdf9ee !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] label,
[data-testid="stFileUploaderDropzone"] span { color: #a8a498 !important; }

[data-testid="stButton"] > button[kind="primary"] {
    background: #0a2540 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    color: #ffffff !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s !important;
    font-family: "Inter", sans-serif !important;
    box-shadow: 0 1px 3px rgba(10, 37, 64, 0.25) !important;
}
            
[data-testid="stButton"] > button[kind="primary"]:hover   { opacity: 0.88 !important; }
[data-testid="stButton"] > button[kind="primary"]:disabled { opacity: 0.35 !important; box-shadow: none !important; }

[data-testid="stButton"] > button[kind="secondary"] {
    background: #ffffff !important;
    border: 1px solid #e2e0d8 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #7a7668 !important;
    padding: 9px 18px !important;
    transition: all 0.15s !important;
    font-family: "Inter", sans-serif !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: #d4a843 !important;
    color: #b07d1e !important;
    background: #fdf9ee !important;
}

/* hide default streamlit spinner entirely — we use our own */
[data-testid="stSpinner"] { display: none !important; }

[data-testid="stAudio"] { margin-top: 6px !important; }
audio { border-radius: 8px !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)


INSTRUMENT_ICONS = {
    "bass":   ("🎸", "#ede8fc", "#5b46b8"),
    "808":    ("🔊", "#ede8fc", "#5b46b8"),
    "kick":   ("🥁", "#e4f7ef", "#1e7a54"),
    "perc":   ("🥁", "#e4f7ef", "#1e7a54"),
    "drum":   ("🥁", "#e4f7ef", "#1e7a54"),
    "snare":  ("🥁", "#e4f7ef", "#1e7a54"),
    "piano":  ("🎹", "#fdf3dc", "#9a6b10"),
    "key":    ("🎹", "#fdf3dc", "#9a6b10"),
    "synth":  ("🎛️", "#dff1f8", "#1a6e8a"),
    "pad":    ("🎛️", "#dff1f8", "#1a6e8a"),
    "vocal":  ("🎤", "#fce8e8", "#9a2020"),
    "guitar": ("🎸", "#fdf3e0", "#8a6010"),
}
DEFAULT_ICON = ("🎵", "#f0eeea", "#8a8678")

WAVEFORM_LOADER_HTML = """
<div class="ss-waveform-loader">
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
    <div class="ss-wl-bar"></div><div class="ss-wl-bar"></div>
</div>
<p class="ss-waveform-caption">scanning samples…</p>
"""


def _icon_for(instrument: str):
    inst = (instrument or "").lower()
    for key, val in INSTRUMENT_ICONS.items():
        if key in inst:
            return val
    return DEFAULT_ICON


def _tier(score: float) -> str:
    if score >= 0.85: return "tier-high"
    if score >= 0.65: return "tier-med"
    return "tier-low"


def _fmt_score(score: float) -> str:
    return f"{score:.2f}"


@st.cache_resource(show_spinner=False)
def get_engine():
    return AudioSearchEngine()


def render_header():
    st.markdown("""
    <div class="ss-header">
        <div class="ss-wave">
            <div class="ss-bar"></div><div class="ss-bar"></div>
            <div class="ss-bar"></div><div class="ss-bar"></div>
            <div class="ss-bar"></div><div class="ss-bar"></div>
            <div class="ss-bar"></div><div class="ss-bar"></div>
            <div class="ss-bar"></div><div class="ss-bar"></div>
            <div class="ss-bar"></div><div class="ss-bar"></div>
        </div>
        <p class="ss-eyebrow">Sample Search</p>
        <h1 class="ss-title">Find the sound<br>you're hearing in your head.</h1>
        <p class="ss-sub">Search by description, or drop a reference clip.</p>
    </div>
    <div class="ss-divider"></div>
    """, unsafe_allow_html=True)

def render_result_card(rank: int, result: dict):
    path = Path(result["path"])
    icon, bg, fg = _icon_for(result.get("instrument", ""))
    tier = _tier(result["score"])

    instrument_str = result.get("instrument") or ""
    duration_str   = f'{result["duration"]}s' if "duration" in result else ""
    sub_parts = []
    if instrument_str: sub_parts.append(instrument_str)
    if duration_str:   sub_parts.append(f"⏱ {duration_str}")
    sub_html = "  ·  ".join(sub_parts) if sub_parts else "&nbsp;"

    st.markdown(f"""
    <div class="ss-result {tier}">
        <div class="ss-result-stripe"></div>
        <div class="ss-result-top">
            <span class="ss-result-num">{rank:02d}</span>
            <div class="ss-result-icon" style="background:{bg};color:{fg}">{icon}</div>
            <div class="ss-result-info">
                <p class="ss-result-name">{result['filename']}</p>
                <div class="ss-result-sub">{sub_html}</div>
            </div>
            <div class="ss-score-badge">
                <div class="ss-score-num">{_fmt_score(result['score'])}</div>
                <div class="ss-score-lbl">score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if path.exists():
        st.audio(str(path))
    else:
        st.markdown(
            f'<p style="font-size:11px;color:#b8b4a4;padding:2px 0 6px 56px">'
            f'⚠ File not found: {path.name}</p>',
            unsafe_allow_html=True,
        )


def render_results(results: list):
    if not results:
        st.markdown("""
        <div class="ss-empty">
            <span class="ss-empty-icon">🔇</span>
            <p class="ss-empty-text">No matching samples found.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    count_word = f'{len(results)} sample{"s" if len(results) != 1 else ""}'
    st.markdown(f"""
    <div class="ss-divider"></div>
    <div class="ss-results-hdr">
        <span class="ss-results-label">Results</span>
        <span class="ss-results-count">{count_word}</span>
    </div>
    """, unsafe_allow_html=True)

    for rank, result in enumerate(results, start=1):
        render_result_card(rank, result)


# ── session init ──────────────────────────────────────────────────────────────

for k, v in [("mode", "text"), ("text_query", ""), ("results", None), ("searching", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── load engine ───────────────────────────────────────────────────────────────

try:
    engine = get_engine()
except Exception as exc:
    st.markdown('<div class="ss-error">⚠ Could not load the search engine.</div>',
                unsafe_allow_html=True)
    st.exception(exc)
    st.stop()


# ── layout ────────────────────────────────────────────────────────────────────

st.markdown('<div class="ss-shell">', unsafe_allow_html=True)
render_header()

col_text, col_audio, col_spacer = st.columns([1, 1, 5])
with col_text:
    if st.button(
        "🔤  Text search", key="btn_text", use_container_width=True,
        type="primary" if st.session_state["mode"] == "text" else "secondary",
    ):
        st.session_state.update({"mode": "text", "results": None, "searching": False})
        st.rerun()
with col_audio:
    if st.button(
        "🎧  Audio match", key="btn_audio", use_container_width=True,
        type="primary" if st.session_state["mode"] == "audio" else "secondary",
    ):
        st.session_state.update({"mode": "audio", "results": None, "searching": False})
        st.rerun()

if st.session_state["mode"] == "text":
    query = st.text_input(
        "query",
        value=st.session_state["text_query"],
        placeholder="e.g. short punchy electronic kick…",
        label_visibility="hidden",
        key="text_query_input",
    )
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        search_clicked = st.button(
            "Search", type="primary",
            disabled=not query.strip(),
            use_container_width=True,
        )

    if search_clicked and query.strip():
        st.session_state["searching"] = True
        st.session_state["text_query"] = query.strip()
        st.session_state["results"] = None
        st.rerun()

else:
    uploaded_file = st.file_uploader(
        "Reference audio",
        type=["wav", "mp3", "flac", "ogg", "m4a"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        st.audio(uploaded_file)
        col_btn2, _ = st.columns([1, 4])
        with col_btn2:
            audio_clicked = st.button("Find similar", type="primary", use_container_width=True)
        if audio_clicked:
            st.session_state["searching"] = True
            st.session_state["_upload_name"] = uploaded_file.name
            st.session_state["_upload_bytes"] = uploaded_file.getbuffer().tobytes()
            st.session_state["results"] = None
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── waveform loader + actual search ──────────────────────────────────────────

if st.session_state.get("searching"):
    st.markdown(WAVEFORM_LOADER_HTML, unsafe_allow_html=True)

    if st.session_state["mode"] == "text":
        results = engine.search_text(st.session_state["text_query"])
    else:
        suffix = Path(st.session_state["_upload_name"]).suffix or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(st.session_state["_upload_bytes"])
            tmp_path = tmp.name
        try:
            results = engine.search_audio(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    st.session_state["results"] = results
    st.session_state["searching"] = False
    st.rerun()

# ── results ───────────────────────────────────────────────────────────────────

if st.session_state["results"] is not None:
    render_results(st.session_state["results"])

st.markdown('</div>', unsafe_allow_html=True)