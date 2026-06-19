import streamlit as st
import numpy as np
import os
import gdown

st.set_page_config(
    page_title="Buzzer Detection",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background biru navy gelap persis seperti gambar */
.stApp {
    background: #0d1433 !important;
}
section[data-testid="stMain"] {
    background: #0d1433 !important;
}

/* Hero card — border biru terang, background sangat gelap */
.hero-card {
    background: rgba(13, 25, 60, 0.7);
    border: 1.5px solid #4a90d9;
    border-radius: 18px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.hero-icon { font-size: 3.5rem; margin-bottom: 0.7rem; }
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #c8d8f0;
    letter-spacing: -0.01em;
    margin-bottom: 0.5rem;
}
.hero-sub {
    color: #7a9bc4;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}
.hero-pill {
    display: inline-block;
    background: rgba(74,144,217,0.15);
    border: 1px solid rgba(74,144,217,0.4);
    color: #7ab3e0;
    font-size: 0.72rem;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    letter-spacing: 0.03em;
}

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid rgba(74,144,217,0.2);
    margin: 1.2rem 0;
}

/* Section title */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e0eaf8;
    margin: 1.2rem 0 1rem;
}

/* Input labels */
label { color: #7a9bc4 !important; font-size: 0.82rem !important; font-weight: 500 !important; }

/* Number input */
.stNumberInput input {
    background: rgba(20,35,75,0.8) !important;
    border: 1px solid rgba(74,144,217,0.3) !important;
    color: #e0eaf8 !important;
    border-radius: 8px !important;
}
.stNumberInput input:focus {
    border-color: #4a90d9 !important;
    box-shadow: 0 0 0 2px rgba(74,144,217,0.2) !important;
}
.stNumberInput > div > div > div > button {
    background: rgba(74,144,217,0.15) !important;
    border: 1px solid rgba(74,144,217,0.25) !important;
    color: #7ab3e0 !important;
    border-radius: 6px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(20,35,75,0.8) !important;
    border: 1px solid rgba(74,144,217,0.3) !important;
    color: #e0eaf8 !important;
    border-radius: 8px !important;
}

/* Button — biru gradient dengan border biru terang */
.stButton > button {
    background: linear-gradient(180deg, #1e5bb5 0%, #1a4d9e 100%) !important;
    color: #c8d8f0 !important;
    border: 1px solid #4a90d9 !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    margin-top: 0.8rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(180deg, #2566c8 0%, #1e5bb5 100%) !important;
    box-shadow: 0 4px 20px rgba(74,144,217,0.35) !important;
}

/* Result card MENCURIGAKAN — merah gelap persis gambar */
.result-mencurigakan {
    background: linear-gradient(135deg, #6b1111 0%, #8b1a1a 60%, #7a1515 100%);
    border: 1px solid #c0392b;
    border-radius: 14px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    margin-top: 1.2rem;
}
.result-normal {
    background: linear-gradient(135deg, #0d4a2a 0%, #145c33 60%, #0d4a2a 100%);
    border: 1px solid #27ae60;
    border-radius: 14px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    margin-top: 1.2rem;
}
.result-icon-big { font-size: 2.5rem; margin-bottom: 0.4rem; }
.result-title-merah {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ff9090;
    margin-bottom: 0.2rem;
}
.result-title-hijau {
    font-size: 1.5rem;
    font-weight: 800;
    color: #6ee7b7;
    margin-bottom: 0.2rem;
}
.result-conf-merah { color: #ffb3b3; font-size: 0.9rem; font-weight: 600; }
.result-conf-hijau { color: #a7f3d0; font-size: 0.9rem; font-weight: 600; }

/* Detail Hasil — tabel 3 kolom seperti gambar */
.detail-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #e0eaf8;
    margin: 1.4rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.detail-table {
    width: 100%;
    border-collapse: collapse;
}
.detail-table th {
    color: #7a9bc4;
    font-size: 0.78rem;
    font-weight: 600;
    text-align: left;
    padding: 0.5rem 0.8rem;
    border-bottom: 1px solid rgba(74,144,217,0.15);
}
.detail-table td {
    color: #e0eaf8;
    font-size: 0.88rem;
    padding: 0.6rem 0.8rem;
    border-bottom: 1px solid rgba(74,144,217,0.08);
}
.detail-table td.merah { color: #f87171; font-weight: 600; }
.detail-table td.hijau { color: #34d399; font-weight: 600; }

/* Footer */
.footer {
    text-align: center;
    color: #2d4a7a;
    font-size: 0.72rem;
    padding: 1.5rem 0 2rem;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 740px; }
</style>
""", unsafe_allow_html=True)


# ─── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "model.pkl"
    if not os.path.exists(model_path):
        file_id = os.environ.get("MODEL_FILE_ID", "")
        if not file_id:
            return None, "model.pkl tidak ditemukan dan MODEL_FILE_ID belum di-set."
        try:
            gdown.download(f"https://drive.google.com/uc?id={file_id}", model_path, quiet=False)
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
    <div class="hero-pill">🤖 XGBoost · StandardScaler · Stacking Ensemble · Railway</div>
</div>
""", unsafe_allow_html=True)

if load_error:
    st.error(load_error)
    st.stop()

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ─── INPUT ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Input Data Akun</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    score              = st.number_input("Score Komentar", value=10, min_value=-100000, max_value=10000000)
    user_comment_karma = st.number_input("Comment Karma", value=500, min_value=0, max_value=100000000)
    user_total_karma   = st.number_input("Total Karma", value=600, min_value=0, max_value=100000000)
with col2:
    controversiality   = st.selectbox("Controversiality", [0,1], format_func=lambda x: "Tidak Kontroversial (0)" if x==0 else "Kontroversial (1)")
    user_link_karma    = st.number_input("Link Karma", value=100, min_value=0, max_value=100000000)
    account_age_days   = st.number_input("Umur Akun (hari)", value=365, min_value=0, max_value=20000)

comment_length = st.number_input("Panjang Komentar (kata)", value=17, min_value=0, max_value=50000)

# ─── PREDICT ─────────────────────────────────────────────────────────────────
if st.button("🔎 Deteksi Sekarang", use_container_width=True):
    features = np.array([[score, controversiality, user_comment_karma,
                          user_link_karma, user_total_karma,
                          account_age_days, comment_length]], dtype=float)
    try:
        proba = model.predict_proba(features)[0][1]
        pred  = int(proba >= 0.50)
        pct   = proba * 100

        if pred == 1:
            st.markdown(f"""
            <div class="result-mencurigakan">
                <div class="result-icon-big">🚨</div>
                <div class="result-title-merah">Akun Mencurigakan</div>
                <div class="result-conf-merah">Confidence: {pct:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            val_class = "merah"
            label_text = "Akun Mencurigakan"
        else:
            st.markdown(f"""
            <div class="result-normal">
                <div class="result-icon-big">✅</div>
                <div class="result-title-hijau">Akun Normal</div>
                <div class="result-conf-hijau">Confidence: {(1-proba)*100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            val_class = "hijau"
            label_text = "Akun Normal"

        st.markdown(f"""
        <div class="detail-section-title">📊 Detail Hasil</div>
        <table class="detail-table">
            <tr>
                <th>Prediksi</th>
                <th>Confidence</th>
                <th>Kode</th>
            </tr>
            <tr>
                <td class="{val_class}">{label_text}</td>
                <td class="{val_class}">{pct:.2f}%</td>
                <td>{pred}</td>
            </tr>
        </table>
        <div class="custom-divider"></div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Prediksi gagal: {e}")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Model Hybrid Machine Learning · Deteksi Perilaku Pengguna Mencurigakan di Media Sosial<br>
    RF + ExtraTrees + XGBoost → Logistic Regression · SMOTE-Tomek · Railway
</div>
""", unsafe_allow_html=True)
