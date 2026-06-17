import streamlit as st
import numpy as np
import os
import gdown

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Buzzer Detector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0a0f; color: #e8e8f0; }

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #818cf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f0f0ff;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.hero-title span {
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub { color: #6b7280; font-size: 0.85rem; }
.model-tag {
    display: inline-block;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 0.25rem 0.8rem;
    border-radius: 4px;
    margin-top: 0.6rem;
}
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: #4b5563;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    margin-top: 1.5rem;
}
.result-buzzer {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin-top: 1rem;
}
.result-normal {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin-top: 1rem;
}
.result-icon { font-size: 2.5rem; margin-bottom: 0.4rem; }
.result-label { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.2rem; }
.result-label.buzzer { color: #f87171; }
.result-label.normal { color: #34d399; }
.result-prob {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #6b7280;
    margin-top: 0.3rem;
}
.prob-track {
    background: #1e1e30;
    border-radius: 6px;
    height: 8px;
    margin: 1rem 0 0.4rem;
    overflow: hidden;
}
.prob-fill-red {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #ef4444, #dc2626);
}
.prob-fill-green {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #10b981, #059669);
}
.divider { border-color: #1e1e30 !important; margin: 1.2rem 0 !important; }
.footer {
    text-align: center;
    color: #374151;
    font-size: 0.72rem;
    padding: 1.5rem 0 2rem;
}
.footer code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #4b5563;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 680px; }
</style>
""", unsafe_allow_html=True)


# ─── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load model.pkl dari:
    1. File lokal (jika ada di folder yang sama)
    2. Google Drive (jika MODEL_FILE_ID di-set di environment variable Railway)
    """
    model_path = "model.pkl"

    if not os.path.exists(model_path):
        file_id = os.environ.get("MODEL_FILE_ID", "")
        if not file_id:
            return None, "❌ `model.pkl` tidak ditemukan dan `MODEL_FILE_ID` belum di-set di Railway."
        try:
            with st.spinner("⏳ Mengunduh model dari Google Drive..."):
                gdown.download(
                    f"https://drive.google.com/uc?id={file_id}",
                    model_path,
                    quiet=False
                )
        except Exception as e:
            return None, f"❌ Gagal mengunduh model: {e}"

    try:
        import joblib
        mdl = joblib.load(model_path)
        return mdl, None
    except Exception as e:
        return None, f"❌ Gagal load model: {e}"


model, load_error = load_model()


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">SKRIPSI — DETEKSI BUZZER MEDIA SOSIAL</div>
    <div class="hero-title">Apakah akun ini<br><span>seorang buzzer?</span></div>
    <div class="hero-sub">Analisis berbasis metadata & pola interaksi akun Reddit</div>
    <div class="model-tag">Realistic Hybrid Stacking Ensemble · RF + ExtraTrees + XGBoost → LR</div>
</div>
""", unsafe_allow_html=True)

if load_error:
    st.error(load_error)
    st.info("💡 Cara fix: Upload `model.pkl` ke Google Drive → Share → Copy File ID → masukkan ke Railway Environment Variables sebagai `MODEL_FILE_ID`")
    st.stop()

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─── INPUT FORM ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📊 Data Metadata Akun</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    score = st.number_input(
        "Score Komentar",
        value=10,
        min_value=-10000,
        max_value=1000000,
        help="Nilai upvote dikurangi downvote pada komentar"
    )
    user_comment_karma = st.number_input(
        "Comment Karma",
        value=500,
        min_value=0,
        max_value=10000000,
        help="Total karma yang diperoleh dari komentar"
    )
    user_total_karma = st.number_input(
        "Total Karma",
        value=600,
        min_value=0,
        max_value=10000000,
        help="Akumulasi total karma akun (comment + link karma)"
    )

with col2:
    controversiality = st.selectbox(
        "Kontroversi Komentar",
        options=[0, 1],
        format_func=lambda x: "0 — Tidak kontroversial" if x == 0 else "1 — Kontroversial",
        help="Apakah komentar ini ditandai kontroversial oleh Reddit?"
    )
    user_link_karma = st.number_input(
        "Link Karma",
        value=100,
        min_value=0,
        max_value=10000000,
        help="Total karma dari postingan/link yang dibuat"
    )
    account_age_days = st.number_input(
        "Umur Akun (hari)",
        value=365,
        min_value=0,
        max_value=20000,
        help="Selisih hari antara pembuatan akun dan saat komentar dibuat"
    )

comment_length = st.number_input(
    "Panjang Komentar (jumlah kata)",
    value=50,
    min_value=0,
    max_value=50000,
    help="Total jumlah kata dalam komentar"
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─── PREDICT ─────────────────────────────────────────────────────────────────
if st.button("🔎 Analisis Akun Sekarang", use_container_width=True):

    features = np.array([[
        score,
        controversiality,
        user_comment_karma,
        user_link_karma,
        user_total_karma,
        account_age_days,
        comment_length
    ]], dtype=float)

    try:
        proba = model.predict_proba(features)[0][1]
        pred  = int(proba >= 0.50)
        pct   = proba * 100

        if pred == 1:
            st.markdown(f"""
            <div class="result-buzzer">
                <div class="result-icon">⚠️</div>
                <div class="result-label buzzer">Terindikasi BUZZER</div>
                <div class="prob-track">
                    <div class="prob-fill-red" style="width:{pct:.1f}%"></div>
                </div>
                <div class="result-prob">Probabilitas buzzer: <strong>{pct:.1f}%</strong></div>
                <div class="result-prob" style="margin-top:.6rem;font-size:.78rem;">
                    Akun ini menunjukkan pola yang konsisten dengan perilaku buzzer berdasarkan metadata.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            norm_pct = (1 - proba) * 100
            st.markdown(f"""
            <div class="result-normal">
                <div class="result-icon">✅</div>
                <div class="result-label normal">Pengguna Normal</div>
                <div class="prob-track">
                    <div class="prob-fill-green" style="width:{norm_pct:.1f}%"></div>
                </div>
                <div class="result-prob">Probabilitas buzzer: <strong>{pct:.1f}%</strong></div>
                <div class="result-prob" style="margin-top:.6rem;font-size:.78rem;">
                    Tidak ditemukan pola mencurigakan yang signifikan pada metadata akun ini.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Detail tabel
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 Lihat Detail Nilai Input & Hasil"):
            st.markdown(f"""
| Fitur | Nilai |
|---|---|
| Score Komentar | `{score}` |
| Kontroversi | `{controversiality}` |
| Comment Karma | `{user_comment_karma:,}` |
| Link Karma | `{user_link_karma:,}` |
| Total Karma | `{user_total_karma:,}` |
| Umur Akun | `{account_age_days} hari` |
| Panjang Komentar | `{comment_length} kata` |
| **Probabilitas Buzzer** | **`{pct:.2f}%`** |
| **Hasil Prediksi** | **`{"⚠️ BUZZER" if pred == 1 else "✅ Normal"}`** |
""")

    except Exception as e:
        st.error(f"❌ Prediksi gagal: {e}")
        st.info("Pastikan model.pkl di-export dari scikit-learn versi yang kompatibel (1.4.x). Lihat README untuk panduan re-export.")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Realistic Hybrid Stacking Ensemble · Skripsi Deteksi Buzzer Media Sosial<br>
    <code>RF + ExtraTrees + XGBoost → Logistic Regression (meta-learner) · SMOTE-Tomek</code>
</div>
""", unsafe_allow_html=True)
