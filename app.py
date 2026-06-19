import streamlit as st
import numpy as np
import os
import gdown

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Buzzer Detection",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background gradient biru gelap seperti gambar */
.stApp {
    background: linear-gradient(135deg, #0d1b3e 0%, #1a2d5a 50%, #0d1b3e 100%);
    min-height: 100vh;
}

/* Hero card */
.hero-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(100,160,255,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}
.hero-icon {
    font-size: 4rem;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #a0b8d8;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.hero-tags {
    display: inline-flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    justify-content: center;
}
.hero-tag {
    background: rgba(100,160,255,0.15);
    border: 1px solid rgba(100,160,255,0.3);
    color: #7eb8ff;
    font-size: 0.72rem;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
}

/* Section title */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Input styling */
label {
    color: #a0b8d8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
.stNumberInput input, .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(100,160,255,0.25) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
.stNumberInput input:focus {
    border-color: #4d9fff !important;
    box-shadow: 0 0 0 2px rgba(77,159,255,0.2) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4d9fff !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #1e4db7, #2563eb) !important;
    color: white !important;
    border: 1px solid rgba(100,160,255,0.4) !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(37,99,235,0.4) !important;
}

/* Result cards */
.result-mencurigakan {
    background: linear-gradient(135deg, rgba(185,28,28,0.3), rgba(239,68,68,0.15));
    border: 1px solid rgba(239,68,68,0.5);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.result-normal {
    background: linear-gradient(135deg, rgba(5,150,105,0.3), rgba(16,185,129,0.15));
    border: 1px solid rgba(16,185,129,0.5);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.result-icon-big { font-size: 2.8rem; margin-bottom: 0.5rem; }
.result-title-mencurigakan {
    font-size: 1.6rem;
    font-weight: 800;
    color: #f87171;
    margin-bottom: 0.3rem;
}
.result-title-normal {
    font-size: 1.6rem;
    font-weight: 800;
    color: #34d399;
    margin-bottom: 0.3rem;
}
.result-confidence {
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.3rem;
}
.conf-merah { color: #fca5a5; }
.conf-hijau { color: #6ee7b7; }

/* Detail hasil card */
.detail-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(100,160,255,0.15);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1.2rem;
}
.detail-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.85rem;
}
.detail-row:last-child { border-bottom: none; }
.detail-key { color: #a0b8d8; }
.detail-val { color: #ffffff; font-weight: 600; }
.detail-val-merah { color: #f87171; font-weight: 700; }
.detail-val-hijau { color: #34d399; font-weight: 700; }

/* Divider */
hr { border-color: rgba(100,160,255,0.15) !important; margin: 1.5rem 0 !important; }

/* Hide streamlit UI */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 720px; }
</style>
""", unsafe_allow_html=True)


# ─── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "model.pkl"
    if not os.path.exists(model_path):
        file_id = os.environ.get("MODEL_FILE_ID", "")
        if not file_id:
            return None, "model.pkl tidak ditemukan dan MODEL_FILE_ID belum di-set di Railway."
        try:
            with st.spinner("⏳ Mengunduh model..."):
                gdown.download(
                    f"https://drive.google.com/uc?id={file_id}",
                    model_path,
                    quiet=False
                )
        except Exception as e:
            return None, f"Gagal download model: {e}"
    try:
        import joblib
        return joblib.load(model_path), None
    except Exception as e:
        return None, f"Gagal load model: {e}"


model, load_error = load_model()


# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-card">
    <div class="hero-icon">🔍</div>
    <div class="hero-title">Buzzer Detection</div>
    <div class="hero-sub">Model Hybrid Machine Learning untuk Deteksi Perilaku Pengguna Mencurigakan di Media Sosial</div>
    <div class="hero-tags">
        <span class="hero-tag">🤖 XGBoost</span>
        <span class="hero-tag">⚖️ StandardScaler</span>
        <span class="hero-tag">🔗 Stacking Ensemble</span>
        <span class="hero-tag">🚀 Railway</span>
    </div>
</div>
""", unsafe_allow_html=True)

if load_error:
    st.error(load_error)
    st.stop()


# ─── INPUT FORM ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Input Data Akun</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    score = st.number_input(
        "Score Komentar",
        value=10,
        min_value=-100000,
        max_value=10000000,
        help="Nilai upvote dikurangi downvote pada komentar"
    )
    user_comment_karma = st.number_input(
        "Comment Karma",
        value=500,
        min_value=0,
        max_value=100000000,
        help="Total karma yang diperoleh dari komentar"
    )
    user_total_karma = st.number_input(
        "Total Karma",
        value=600,
        min_value=0,
        max_value=100000000,
        help="Akumulasi total karma akun"
    )

with col2:
    controversiality = st.selectbox(
        "Controversiality",
        options=[0, 1],
        format_func=lambda x: "Tidak Kontroversial (0)" if x == 0 else "Kontroversial (1)",
        help="Apakah komentar ini ditandai kontroversial?"
    )
    user_link_karma = st.number_input(
        "Link Karma",
        value=100,
        min_value=0,
        max_value=100000000,
        help="Total karma dari postingan/link"
    )
    account_age_days = st.number_input(
        "Umur Akun (hari)",
        value=365,
        min_value=0,
        max_value=20000,
        help="Umur akun saat komentar dibuat"
    )

comment_length = st.number_input(
    "Panjang Komentar (kata)",
    value=17,
    min_value=0,
    max_value=50000,
    help="Jumlah kata dalam komentar"
)


# ─── BUTTON & PREDICT ────────────────────────────────────────────────────────
if st.button("🔎 Deteksi Sekarang", use_container_width=True):

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
        proba  = model.predict_proba(features)[0][1]
        pred   = int(proba >= 0.50)
        pct    = proba * 100
        kode   = 1 if pred == 1 else 0

        if pred == 1:
            st.markdown(f"""
            <div class="result-mencurigakan">
                <div class="result-icon-big">🚨</div>
                <div class="result-title-mencurigakan">Akun Mencurigakan</div>
                <div class="result-confidence conf-merah">Confidence: {pct:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-normal">
                <div class="result-icon-big">✅</div>
                <div class="result-title-normal">Akun Normal</div>
                <div class="result-confidence conf-hijau">Confidence: {pct:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Detail hasil
        label_text  = "Akun Mencurigakan" if pred == 1 else "Akun Normal"
        val_class   = "detail-val-merah" if pred == 1 else "detail-val-hijau"

        st.markdown(f"""
        <div class="detail-card">
            <div class="detail-title">📊 Detail Hasil</div>
            <div class="detail-row">
                <span class="detail-key">Prediksi</span>
                <span class="{val_class}">{label_text}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Confidence</span>
                <span class="{val_class}">{pct:.2f}%</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Kode</span>
                <span class="detail-val">{kode}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Score Komentar</span>
                <span class="detail-val">{score}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Controversiality</span>
                <span class="detail-val">{controversiality}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Comment Karma</span>
                <span class="detail-val">{user_comment_karma:,}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Link Karma</span>
                <span class="detail-val">{user_link_karma:,}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Total Karma</span>
                <span class="detail-val">{user_total_karma:,}</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Umur Akun</span>
                <span class="detail-val">{account_age_days} hari</span>
            </div>
            <div class="detail-row">
                <span class="detail-key">Panjang Komentar</span>
                <span class="detail-val">{comment_length} kata</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Prediksi gagal: {e}")
        st.info("Pastikan model.pkl di-export dari scikit-learn versi yang kompatibel.")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#4a6080;font-size:0.75rem;padding-bottom:2rem;">
    Model Hybrid Machine Learning · Deteksi Perilaku Pengguna Mencurigakan di Media Sosial<br>
    RF + ExtraTrees + XGBoost → Logistic Regression · SMOTE-Tomek · Railway
</div>
""", unsafe_allow_html=True)
