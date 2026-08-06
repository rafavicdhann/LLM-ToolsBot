import streamlit as st

st.set_page_config(page_title="ToolFinder AI", layout="centered")

HEADER = "ToolFinder AI — Bantu kamu menemukan tools AI terbaik"

def _inject_css():
    css = """
    <style>
    .stApp {
        background: #2b0e0e; /* dark maroon */
        color: #f4e9e9;
    }
    .stButton>button {
        background-color: #6e1f1f;
        color: #fff;
        border: none;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #3a1515;
        color: #f4e9e9;
    }
    .stMarkdown, .stInfo, .stWarning, .stCaption {
        color: #f4e9e9;
    }
    /* card styles for recommendation cards */
    .card { background: #3a1515; border: 1px solid #6e1f1f; padding:14px; border-radius:10px; margin:10px 0 }
    .card h3 { margin:0 0 6px 0; color: #fff }
    .card .price { color:#f4e9e9; font-size:0.9em; margin-left:8px }
    .card p { margin:4px 0; color: #efe7e7 }
    .cards { display: grid; grid-template-columns: 1fr; gap: 10px }
    @media (min-width:800px) { .cards { grid-template-columns: 1fr 1fr } }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


_inject_css()

st.title(HEADER)
st.write("Kamu bisa menjelaskan tugas atau masalahmu secara singkat. ToolFinder akan merekomendasikan 3–5 tools AI yang cocok.")

# --- API input / settings ---
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

with st.expander("API Settings (opsional)", expanded=True):
    st.session_state['api_key'] = st.text_input("Masukkan API key (jika ada)", value=st.session_state.get('api_key',''), type="password")
    st.caption("Masukkan API key untuk rekomendasi dinamis. Kalau tidak ada, ToolFinder tetap memberikan rekomendasi dasar offline.")

if not st.session_state.get('api_key'):
    st.info("Tip: Masukkan API key di 'API Settings' sebelum bertanya untuk hasil yang lebih dinamis.")

user_input = st.text_area("Jelaskan kebutuhanmu (contoh: tool AI gratis buat bikin presentasi dari outline teks)", height=120)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform yang diutamakan?", ["Tidak penting","Desktop","Mobile","Web"])
with col2:
    budget = st.selectbox("Skema harga yang diinginkan?", ["Tidak penting","Gratis","Freemium","Berbayar"]) 

submit = st.button("Cari Tools")

# Simple helpers and knowledge base of real tools
TOOLS_DB = {
    "presentasi": [
        {"name": "Gamma.app", "price": "Freemium", "func": "Membuat presentasi AI dari teks/outline secara cepat.", "highlight": "Output slide naratif dan template modern.", "who": "Para product manager, startup founder, dan presenter cepat"},
        {"name": "Beautiful.ai", "price": "Freemium", "func": "Mendesain slide otomatis berdasarkan konten.", "highlight": "Desain slide yang konsisten dan profesional.", "who": "User yang butuh slide rapi tanpa desain manual"},
        {"name": "Canva", "price": "Freemium", "func": "Desain visual termasuk slide dengan fitur AI.", "highlight": "Banyak template, editing visual mudah.", "who": "Pengguna umum dan tim pemasaran"},
        {"name": "Tome", "price": "Freemium", "func": "Storytelling & presentasi berbasis AI untuk narasi interaktif.", "highlight": "Mendukung storytelling yang menarik dan integrasi media.", "who": "Designer, storyteller, product demos"}
    ],
    "tulis": [
        {"name": "ChatGPT (OpenAI)", "price": "Freemium / Berbayar", "func": "Menulis, menyunting, dan merangkum teks dengan AI percakapan.", "highlight": "Kemampuan bahasa alami yang kaya dan fleksibel.", "who": "Penulis, marketer, mahasiswa"},
        {"name": "Perplexity", "price": "Freemium", "func": "Menjawab pertanyaan sekaligus menyertakan sumber.", "highlight": "Jawaban yang dilengkapi referensi & browsing.", "who": "Riset cepat & pembuat konten"},
        {"name": "Copy.ai", "price": "Freemium", "func": "Membuat copy marketing dan ide konten cepat.", "highlight": "Template khusus marketing dan copywriting.", "who": "Marketer dan social media manager"}
    ],
    "gambar": [
        {"name": "Midjourney", "price": "Berbayar", "func": "Generative images/art dari prompt teks.", "highlight": "Gaya artistik kuat dan komunitas aktif.", "who": "Artis digital dan kreator visual"},
        {"name": "DALL·E (OpenAI)", "price": "Pembayaran per penggunaan", "func": "Membuat gambar dari teks dengan kontrol yang baik.", "highlight": "Integrasi mudah lewat API OpenAI.", "who": "Desainer produk dan marketer"},
        {"name": "Stable Diffusion (Stability.ai)", "price": "Gratis / Open-source", "func": "Model gambar yang dapat dijalankan lokal atau via web.", "highlight": "Banyak front-end dan mod yang tersedia.", "who": "Pengguna teknis dan eksperimen kreatif"}
    ],
    "kode": [
        {"name": "GitHub Copilot", "price": "Berbayar", "func": "Autocompletion dan asistensi coding berbasis AI.", "highlight": "Terintegrasi langsung dalam IDE (VS Code).", "who": "Developer yang ingin percepat penulisan kode"},
        {"name": "Tabnine", "price": "Freemium", "func": "AI code completion untuk berbagai IDE.", "highlight": "Dukungan multi-language dan privasi tim.", "who": "Tim engineering dan developer solo"},
        {"name": "Replit Ghostwriter", "price": "Freemium", "func": "Asisten coding di browser dengan fitur run-in-place.", "highlight": "IDE online + bantuan AI terpadu.", "who": "Learners dan developer yang ingin prototyping cepat"}
    ],
    "audio": [
        {"name": "Otter.ai", "price": "Freemium", "func": "Transkripsi meeting dan ringkasan otomatis.", "highlight": "Integrasi meeting dan speaker diarization.", "who": "Team yang sering rapat dan butuh transkrip"},
        {"name": "Descript", "price": "Berbayar", "func": "Audio/video editing berbasis transkrip.", "highlight": "Editing yang mirip dokumen, overdub suara.", "who": "Podcaster dan content creator"},
        {"name": "Fireflies.ai", "price": "Freemium", "func": "Mencatat dan merangkum percakapan meeting.", "highlight": "Integrasi kalender dan conferencing.", "who": "Sales dan tim dukungan pelanggan"}
    ]
}

OUT_OF_SCOPE_KEYWORDS = ["resep","politik","politik","masakan","makanan","jurusan","tugas sekolah"]


def detect_scope(text: str) -> bool:
    t = text.lower()
    for k in OUT_OF_SCOPE_KEYWORDS:
        if k in t:
            return False
    return True


def choose_category(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["presentasi","slide","ppt","powerpoint"]):
        return "presentasi"
    if any(w in t for w in ["ringkas","ringkasan","summar","sumar","resume","meringkas"]):
        return "tulis"
    if any(w in t for w in ["gambar","image","ilustrasi","design","illustration","generate image","image"]):
        return "gambar"
    if any(w in t for w in ["kode","program","coding","debug","developer","script"]):
        return "kode"
    if any(w in t for w in ["transkrip","transcribe","audio","rekaman","rapat","meeting"]):
        return "audio"
    # default to writing/general assistant
    return "tulis"


def format_markdown(recs):
    lines = []
    for r in recs:
        lines.append(f"* **{r['name']}** — *{r['price']}*\n  - 🎯 **Fungsi Utama:** {r['func']}\n  - ⭐ **Fitur Unggulan:** {r['highlight']}\n  - 👤 **Cocok Untuk:** {r['who']}")
    return "\n\n".join(lines)


def render_recommendations(display_recs, top):
    st.markdown("**Rekomendasi Tools (3–5 opsi)**")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="cards">', unsafe_allow_html=True)
    for r in display_recs:
        html = f"""
        <div class="card">
          <h3>{r['name']} <span class='price'>{r['price']}</span></h3>
          <p><strong>🎯 Fungsi Utama:</strong> {r['func']}</p>
          <p><strong>⭐ Kenapa pilih ini:</strong> {r['highlight']}</p>
          <p><strong>👤 Cocok Untuk:</strong> {r['who']}</p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if top:
        st.markdown(f"**Top Pick:** *{top['name']}* — {top['highlight']}\n\n")
    st.markdown("---")
    st.markdown("**Perbaiki / Spesifikkan Hasil**")
    refine_text = st.text_area("Mau rekomendasi seperti apa? (mis. hanya gratis, fokus mobile, integrasi Zapier, dll)", key='refine_input', height=80)
    if st.button('Refine'):
        base = st.session_state.get('orig_recs', [])
        q = (refine_text or '').strip().lower()
        if q:
            tokens = [t for t in q.replace(',', ' ').split() if t]
            def match(r):
                hay = ' '.join([r['name'], r['func'], r['highlight'], r['who'], r['price']]).lower()
                return all(tok in hay for tok in tokens)
            filtered = [r for r in base if match(r)]
            if filtered:
                st.session_state['current_recs'] = filtered
                # let the next rerun reflect changes
                try:
                    st.experimental_rerun()
                except Exception:
                    st.stop()
            else:
                st.warning("Tidak menemukan yang cocok berdasarkan saranmu — menampilkan rekomendasi awal.")


if submit:
    if not user_input or len(user_input.strip()) < 5:
        st.info("Pertanyaanmu masih terlalu singkat. Tolong jelaskan tujuan, platform (Mobile/Desktop), atau budget secara singkat.")
    else:
        if not detect_scope(user_input):
            st.warning("Topik yang diminta tampaknya di luar konteks tools digital/AI. Saya hanya membantu menemukan tools digital/AI.")
        else:
            cat = choose_category(user_input)
            recs = TOOLS_DB.get(cat, TOOLS_DB["tulis"])[:5]
            # adjust by budget filter
            if budget == "Gratis":
                recs = [r for r in recs if "Gratis" in r['price'] or "Freemium" in r['price'] or "Open-source" in r['price']]
                if len(recs) < 3:
                    recs = TOOLS_DB.get(cat, TOOLS_DB["tulis"])[:3]
            if len(recs) < 3:
                recs = TOOLS_DB.get(cat, TOOLS_DB["tulis"])[:3]

            md = format_markdown(recs[:5])
            # save original recs so refine can use it after reruns
            st.session_state['orig_recs'] = recs[:5]
            st.session_state['current_recs'] = recs[:5]
            st.session_state['last_query'] = user_input
            st.session_state['top'] = recs[0]

            # Render immediately so user sees results without requiring experimental_rerun
            render_recommendations(recs[:5], recs[0])
            st.stop()

# Outside submit: show refinable UI if we have `last_query`
if 'last_query' in st.session_state:
    display_recs = st.session_state.get('current_recs', st.session_state.get('orig_recs', []))
    top = st.session_state.get('top')

    # card CSS (ensure same style available)
    st.markdown("**Rekomendasi Tools (3–5 opsi)**")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for r in display_recs:
        html = f"""
        <div class="card">
          <h3>{r['name']} <span class='price'>{r['price']}</span></h3>
          <p><strong>🎯 Fungsi Utama:</strong> {r['func']}</p>
          <p><strong>⭐ Kenapa pilih ini:</strong> {r['highlight']}</p>
          <p><strong>👤 Cocok Untuk:</strong> {r['who']}</p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    if top:
        st.markdown(f"**Top Pick:** *{top['name']}* — {top['highlight']}\n\n")

    st.markdown("---")
    st.markdown("**Perbaiki / Spesifikkan Hasil**")
    refine_text = st.text_area("Mau rekomendasi seperti apa? (mis. hanya gratis, fokus mobile, integrasi Zapier, dll)", key='refine_input', height=80)
    if st.button('Refine'):
        base = st.session_state.get('orig_recs', [])
        q = (refine_text or '').strip().lower()
        if q:
            tokens = [t for t in q.replace(',', ' ').split() if t]
            def match(r):
                hay = ' '.join([r['name'], r['func'], r['highlight'], r['who'], r['price']]).lower()
                return all(any(tok in part for part in [hay]) for tok in tokens)
            filtered = [r for r in base if match(r)]
            if filtered:
                st.session_state['current_recs'] = filtered
                try:
                    st.experimental_rerun()
                except Exception:
                    st.stop()
            else:
                st.warning("Tidak menemukan yang cocok berdasarkan saranmu — menampilkan rekomendasi awal.")

# Small footer
st.caption("ToolFinder AI — Rekomendasi cepat 3–5 tools. Dibuat untuk demo Streamlit.")
