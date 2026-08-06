import streamlit as st

# ToolFinder AI for Streamlit
# Implements the user's specification: diagnosis, 3-5 structured recommendations, top pick, and closing question.

st.set_page_config(page_title="ToolFinder AI", page_icon="🧭")

def is_specific(prompt: str) -> bool:
    """Heuristic to decide if the user's prompt is sufficiently specific.
    Returns True when the user provided clear goal or keywords.
    """
    if not prompt:
        return False
    p = prompt.lower()
    keywords = [
        "presentasi", "slide", "present", "gambar", "image", "video", "transcribe",
        "transkripsi", "suara", "audio", "code", "kode", "program", "skrip",
        "dokumen", "summar", "summary", "resume", "marketing", "seo", "konten",
        "chatbot", "chat", "customer", "pdf", "ocr", "design", "desain",
    ]
    # Specific if long enough or contains any keyword
    if len(p) > 50:
        return True
    for k in keywords:
        if k in p:
            return True
    return False

# Minimal database of valid, public AI tools grouped by intent
TOOL_DB = {
    "presentations": [
        {
            "name": "Canva",
            "price": "Freemium",
            "desc": "Membuat slide dan desain presentasi dari template dan AI assistant.",
            "feature": "Editor drag-and-drop + Magic Design AI untuk konversi teks jadi slide.",
            "audience": "Pengguna non-desainer yang butuh hasil cepat untuk presentasi."
        },
        {
            "name": "Beautiful.ai",
            "price": "Freemium",
            "desc": "Otomatisasi layout slide berdasarkan konten yang dimasukkan.",
            "feature": "Auto-layout yang menjaga konsistensi visual tanpa usaha desain.",
            "audience": "Profesional yang butuh presentasi rapi tanpa mendesain manual."
        },
        {
            "name": "Gamma.app",
            "price": "Freemium",
            "desc": "Membangun presentasi dan dokumen visual dari outline teks dengan AI.",
            "feature": "Transform outline teks jadi presentasi yang interaktif dan terstruktur.",
            "audience": "Orang yang punya outline/skrip dan ingin langsung jadi presentasi."
        }
    ],
    "images": [
        {
            "name": "Midjourney",
            "price": "Berbayar (credit-based)",
            "desc": "Pembuatan gambar dan ilustrasi berkualitas tinggi berbasis prompt.",
            "feature": "Gaya visual unik dan komunitas prompt yang kaya.",
            "audience": "Desainer dan kreator yang butuh hasil artistik/konseptual."
        },
        {
            "name": "DALL·E (OpenAI)",
            "price": "Freemium / Berbayar",
            "desc": "Menghasilkan gambar dari deskripsi teks dengan kontrol komposisi.",
            "feature": "Integrasi API OpenAI dan kemampuan editing inpainting.",
            "audience": "Pengguna yang butuh gambar cepat dengan opsi integrasi API."
        },
        {
            "name": "Stable Diffusion (DreamStudio)",
            "price": "Freemium / Berbayar",
            "desc": "Engine open-source yang banyak varian untuk image generation.",
            "feature": "Kontrol model dan pipeline; banyak komunitas model kustom.",
            "audience": "Pengembang dan kreator yang ingin eksperimen model."
        }
    ],
    "transcription": [
        {
            "name": "Otter.ai",
            "price": "Freemium",
            "desc": "Transkripsi percakapan dan meeting otomatis dengan speaker recognition.",
            "feature": "Realtime transcription + integrasi dengan Zoom/Google Meet.",
            "audience": "Reporter, peserta meeting, dan tim yang butuh ringkasan percakapan."
        },
        {
            "name": "Descript",
            "price": "Freemium",
            "desc": "Editor audio/video dengan transkripsi yang bisa di-edit seperti teks.",
            "feature": "Edit audio lewat pengeditan teks (overdub & clip edit).",
            "audience": "Podcaster dan pembuat konten yang mengedit audio & video."
        },
        {
            "name": "OpenAI Whisper (via API)",
            "price": "Berbayar (API)",
            "desc": "Model speech-to-text open-source/tersedia via API untuk akurasi tinggi.",
            "feature": "Mendukung banyak bahasa dan cocok untuk integrasi custom.",
            "audience": "Developer yang butuh transkripsi terprogram dan multi-bahasa."
        }
    ],
    "code": [
        {
            "name": "GitHub Copilot",
            "price": "Berbayar (trial tersedia)",
            "desc": "Autocompletion dan saran kode berbasis konteks editor.",
            "feature": "Integrasi langsung ke VS Code dan editor populer.",
            "audience": "Developer yang ingin produktivitas coding lebih cepat."
        },
        {
            "name": "Replit Ghostwriter",
            "price": "Freemium / Berbayar",
            "desc": "Asisten kode di browser dengan kemampuan menjalankan project cepat.",
            "feature": "Lingkungan development terintegrasi + saran kode real-time.",
            "audience": "Pelajar dan dev yang ingin prototyping cepat di web."
        },
        {
            "name": "Tabnine",
            "price": "Freemium / Berbayar",
            "desc": "Autocompletion AI yang mendukung banyak bahasa dan lokal model.",
            "feature": "Pilihan private models untuk tim dan keamanan kode.",
            "audience": "Tim dev yang ingin kontrol privasi model."
        }
    ],
    "general": [
        {
            "name": "ChatGPT (OpenAI)",
            "price": "Freemium / Berbayar (ChatGPT Plus)",
            "desc": "Asisten percakapan umum untuk drafting teks, ide, dan automasi.",
            "feature": "Kemampuan dialog lanjutan, plugin, dan API integrasi.",
            "audience": "Siapa saja yang butuh asisten teks serbaguna."
        },
        {
            "name": "Claude (Anthropic)",
            "price": "Freemium / Berbayar",
            "desc": "Model percakapan dengan fokus keselamatan dan instruksi.",
            "feature": "Kemampuan penanganan instruksi yang panjang dan konteks besar.",
            "audience": "Tim yang butuh analisis teks dan penjelasan yang aman."
        },
        {
            "name": "Notion AI",
            "price": "Freemium / Berbayar",
            "desc": "AI terintegrasi untuk membantu pembuatan konten dan manajemen knowledge.",
            "feature": "Langsung bekerja di workspace Notion, cocok untuk dokumentasi.",
            "audience": "Tim yang mengorganisir pengetahuan dan konten internal."
        }
    ]
}


def choose_category(text: str, extra_purpose: str = None) -> str:
    """Simple mapping from user text to one of the categories in TOOL_DB."""
    t = (text or "").lower()
    if extra_purpose:
        t += " " + extra_purpose.lower()
    if any(k in t for k in ["presentasi", "slide", "slide", "present"]):
        return "presentations"
    if any(k in t for k in ["gambar", "image", "ilustrasi", "design", "desain"]):
        return "images"
    if any(k in t for k in ["transcribe", "transkripsi", "audio", "suara", "meeting", "podcast"]):
        return "transcription"
    if any(k in t for k in ["kode", "code", "program", "script", "develop"]):
        return "code"
    # default to general
    return "general"


def render_tool_md(tool: dict) -> str:
    """Return a Markdown block for one tool using the required format."""
    md = f"**{tool['name']}** — *{tool['price']}*\n"
    md += f"- 🎯 **Fungsi Utama:** {tool['desc']}\n"
    md += f"- ⭐ **Fitur Unggulan:** {tool['feature']}\n"
    md += f"- 👤 **Cocok Untuk:** {tool['audience']}\n"
    return md


st.title("🧭 ToolFinder AI — Temukan Tool AI terbaik untuk tugasmu")
st.write("_ToolFinder AI membantu menemukan 3–5 tools AI paling relevan untuk kebutuhan spesifik kamu — ikuti langkah singkat di bawah._")

with st.form("search_form"):
    user_input = st.text_area("Jelaskan pekerjaan atau masalahmu (contoh: 'Buat presentasi dari outline teks, gratis jika bisa'):", height=120)
    submitted = st.form_submit_button("Cari tools")

if submitted:
    if not is_specific(user_input):
        st.info("Sepertinya butuh sedikit klarifikasi supaya rekomendasinya tepat. Jawab 1–2 pertanyaan singkat di bawah:")
        purpose = st.selectbox("Tujuan utama:", ["Pembuatan Presentasi", "Membuat Gambar/Ilustrasi", "Transkripsi Audio", "Bantuan Kode/Programming", "Pembuatan Konten/Teks", "Lainnya"], index=0)
        platform = st.radio("Platform target:", ["Desktop", "Mobile", "Web / Keduanya", "Tidak Peduli"], index=3)
        budget = st.radio("Ketersediaan budget:", ["Gratis", "Freemium", "Berbayar", "Tidak tahu"], index=3)
        if st.button("Lanjutkan rekomendasi"):
            # build a query and choose category
            category = choose_category(user_input, purpose)
            tools = TOOL_DB.get(category, TOOL_DB['general'])
            # limit 3-5
            tools = tools[:5]

            st.markdown("---")
            st.markdown(f"### Rekomendasi tools untuk: **{purpose}** (Platform: *{platform}*, Budget: *{budget}*)")
            for t in tools[:5]:
                st.markdown(render_tool_md(t))
            # Top pick
            top = tools[0]
            st.markdown(f"**Top Pick:** *{top['name']}* — pilihan paling praktis dan ramah-pemula untuk kebutuhan ini.")
            st.markdown("---")
            st.markdown("Dari daftar di atas, ada yang ingin kamu bedah fitur spesifiknya, atau mau cari alternatif yang khusus untuk mobile?")
    else:
        # direct recommendation path
        category = choose_category(user_input)
        tools = TOOL_DB.get(category, TOOL_DB['general'])
        # pick between 3 and 5
        tools = tools[:5]

        st.markdown(f"### Rekomendasi tools (kategori: **{category}**) :")
        for t in tools[:5]:
            st.markdown(render_tool_md(t))

        # Top pick
        top = tools[0]
        st.markdown(f"**Top Pick:** *{top['name']}* — pilihan paling praktis dan ramah-pemula untuk kebutuhan ini.")
        st.markdown("---")
        st.markdown("Dari daftar di atas, ada yang ingin kamu bedah fitur spesifiknya, atau mau cari alternatif yang khusus untuk mobile?")

# Footer/help
with st.expander("Cara kerja ToolFinder AI (ringkas)"):
    st.markdown("- Masukkan kebutuhanmu secara jelas agar rekomendasi bisa langsung akurat.\n- Jika input masih umum, ToolFinder akan tanya 1–2 hal singkat.\n- Setiap rekomendasi menampilkan fungsi utama, fitur unggulan, dan siapa yang cocok menggunakan tool itu.")

st.caption("Dibuat sebagai demo: ToolFinder AI untuk Streamlit — pastikan koneksi internet untuk mengunjungi situs tool yang direkomendasikan.")
