import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Toko Buah ABS",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Constants ─────────────────────────────────────────────────────────────────
TOKO_WA   = "6287875957722"
TOKO_NAMA = "Toko Buah ABS"
TOKO_ALAMAT = "Jl. Mandala Raya, RT.02/RW.02, Ciparigi, Kec. Bogor Utara, Kota Bogor, Jawa Barat 16157"
TOKO_JAM  = "08.00 – 21.30 (Setiap Hari)"
TOKO_TELP = "087875957722"
DATA_FILE = "data_pesanan.json"

PRODUK = [
    {"id": 1,  "nama": "Jeruk Siam",       "emoji": "🍊", "harga": 12000, "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 2,  "nama": "Jeruk Kecil",      "emoji": "🍋", "harga": 8000,  "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 3,  "nama": "Mangga Harum Manis","emoji": "🥭","harga": 18000, "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 4,  "nama": "Buah Naga",        "emoji": "🐉", "harga": 15000, "satuan": "per buah",  "kategori": "Lokal"},
    {"id": 5,  "nama": "Pisang Cavendish", "emoji": "🍌", "harga": 5000,  "satuan": "per sisir", "kategori": "Lokal"},
    {"id": 6,  "nama": "Belimbing",        "emoji": "⭐", "harga": 7000,  "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 7,  "nama": "Salak Pondoh",     "emoji": "🌰", "harga": 10000, "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 8,  "nama": "Apel Hijau",       "emoji": "🍏", "harga": 22000, "satuan": "per kg",    "kategori": "Impor"},
    {"id": 9,  "nama": "Apel Merah",       "emoji": "🍎", "harga": 20000, "satuan": "per kg",    "kategori": "Impor"},
    {"id": 10, "nama": "Melon",            "emoji": "🍈", "harga": 9000,  "satuan": "per kg",    "kategori": "Lokal"},
    {"id": 11, "nama": "Nanas",            "emoji": "🍍", "harga": 8000,  "satuan": "per buah",  "kategori": "Lokal"},
    {"id": 12, "nama": "Parcel Buah S",    "emoji": "🎁", "harga": 75000, "satuan": "per paket", "kategori": "Parcel"},
    {"id": 13, "nama": "Parcel Buah M",    "emoji": "🎁", "harga": 125000,"satuan": "per paket", "kategori": "Parcel"},
    {"id": 14, "nama": "Parcel Buah L",    "emoji": "🎁", "harga": 200000,"satuan": "per paket", "kategori": "Parcel"},
]

# ── Data helpers ──────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"pesanan": [], "pengunjung": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tambah_pesanan(nama, wa, alamat, items, total):
    data = load_data()
    pesanan_baru = {
        "id": len(data["pesanan"]) + 1,
        "tanggal": datetime.now().strftime("%Y-%m-%d"),
        "waktu": datetime.now().strftime("%H:%M"),
        "nama": nama,
        "wa": wa,
        "alamat": alamat,
        "items": items,
        "total": total,
    }
    data["pesanan"].append(pesanan_baru)
    save_data(data)
    return pesanan_baru["id"]

def catat_pengunjung():
    data = load_data()
    data["pengunjung"] = data.get("pengunjung", 0) + 1
    save_data(data)

# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }

    .stApp { background: #f7fdf3; }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #2d6a0a 0%, #4a9d1a 50%, #76c442 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(74,157,26,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: "🍎🥭🍊🍌🍉🍇🍋🍈🍍";
        position: absolute; top: 8px; left: 0; right: 0;
        font-size: 22px; letter-spacing: 12px;
        opacity: 0.25; white-space: nowrap;
    }
    .hero-banner h1 {
        font-family: 'Poppins', sans-serif !important;
        font-size: 2.6rem !important; font-weight: 800 !important;
        margin: 0 !important; text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        color: white !important;
    }
    .hero-banner .tagline {
        font-size: 1.1rem; opacity: 0.92; margin: 0.3rem 0 1rem;
        font-weight: 600;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.22);
        border: 1.5px solid rgba(255,255,255,0.45);
        border-radius: 30px; padding: 5px 18px;
        font-size: 0.85rem; font-weight: 700; margin: 3px;
    }
    .hero-info {
        margin-top: 1rem;
        font-size: 0.82rem; opacity: 0.85;
        display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;
    }
    .hero-info span { display: flex; align-items: center; gap: 5px; }

    /* ── Nav Tabs ── */
    .nav-tabs {
        display: flex; gap: 8px; margin-bottom: 1.2rem; flex-wrap: wrap;
    }
    .nav-tab {
        padding: 8px 20px; border-radius: 30px; font-size: 0.88rem;
        font-weight: 700; cursor: pointer; border: 2px solid transparent;
        transition: all 0.2s; text-decoration: none;
    }
    .nav-tab-active {
        background: #2d6a0a; color: white; border-color: #2d6a0a;
    }
    .nav-tab-inactive {
        background: white; color: #2d6a0a; border-color: #c8e6b0;
    }
    .nav-tab-inactive:hover { background: #f0fae8; border-color: #4a9d1a; }

    /* ── Product Cards ── */
    .product-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border: 1.5px solid #e8f5e0;
        transition: transform 0.15s, box-shadow 0.15s;
        height: 100%;
        text-align: center;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74,157,26,0.15);
        border-color: #76c442;
    }
    .product-emoji { font-size: 3rem; margin-bottom: 0.4rem; display: block; }
    .product-name { font-size: 0.95rem; font-weight: 800; color: #1a4a05; margin-bottom: 2px; }
    .product-satuan { font-size: 0.75rem; color: #6aaa3a; margin-bottom: 6px; }
    .product-price {
        font-size: 1.05rem; font-weight: 800; color: #2d6a0a;
        background: #edfade; padding: 3px 12px; border-radius: 20px;
        display: inline-block; margin-bottom: 10px;
    }
    .badge-lokal {
        font-size: 0.7rem; background: #d4edda; color: #155724;
        padding: 2px 10px; border-radius: 20px; font-weight: 700;
        display: inline-block; margin-bottom: 8px;
    }
    .badge-impor {
        font-size: 0.7rem; background: #cce5ff; color: #004085;
        padding: 2px 10px; border-radius: 20px; font-weight: 700;
        display: inline-block; margin-bottom: 8px;
    }
    .badge-parcel {
        font-size: 0.7rem; background: #fff3cd; color: #856404;
        padding: 2px 10px; border-radius: 20px; font-weight: 700;
        display: inline-block; margin-bottom: 8px;
    }

    /* ── Stat Cards ── */
    .stat-card {
        background: white; border-radius: 16px;
        padding: 1.4rem 1.2rem; text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 5px solid #4a9d1a;
    }
    .stat-val { font-size: 2rem; font-weight: 900; color: #2d6a0a; }
    .stat-label { font-size: 0.82rem; color: #6aaa3a; font-weight: 600; margin-top: 4px; }

    /* ── Section title ── */
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem; font-weight: 700; color: #1a4a05;
        border-left: 5px solid #4a9d1a;
        padding-left: 12px; margin-bottom: 1rem;
    }

    /* ── Cart item ── */
    .cart-row {
        background: #f7fdf3; border-radius: 10px;
        padding: 10px 14px; margin-bottom: 6px;
        border: 1px solid #d4edda;
        display: flex; justify-content: space-between; align-items: center;
    }
    .cart-name { font-weight: 700; font-size: 0.9rem; color: #1a4a05; }
    .cart-sub  { font-size: 0.78rem; color: #6aaa3a; }
    .cart-price { font-weight: 800; color: #2d6a0a; font-size: 0.92rem; }

    /* ── Order form ── */
    .order-section {
        background: white; border-radius: 16px; padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07); border: 1.5px solid #e8f5e0;
        margin-top: 1rem;
    }

    /* ── WA button ── */
    .wa-btn {
        display: block; width: 100%;
        background: #25D366; color: white;
        text-align: center; padding: 14px;
        border-radius: 12px; font-weight: 800; font-size: 1.05rem;
        text-decoration: none; margin-top: 12px;
        box-shadow: 0 4px 14px rgba(37,211,102,0.35);
        transition: background 0.2s;
    }
    .wa-btn:hover { background: #1da851; color: white; text-decoration: none; }

    /* ── Maps btn ── */
    .maps-btn {
        display: inline-block;
        background: #4285F4; color: white;
        padding: 10px 22px; border-radius: 10px;
        font-weight: 700; font-size: 0.88rem;
        text-decoration: none; margin-top: 8px;
        box-shadow: 0 3px 10px rgba(66,133,244,0.3);
    }
    .maps-btn:hover { background: #3367d6; color: white; text-decoration: none; }

    /* ── Info box ── */
    .info-box {
        background: #fff9e6; border: 1.5px solid #ffe082;
        border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1rem;
        font-size: 0.88rem; color: #7a5800;
    }

    /* hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}
if "halaman" not in st.session_state:
    st.session_state.halaman = "Beranda"
if "pengunjung_tercatat" not in st.session_state:
    catat_pengunjung()
    st.session_state.pengunjung_tercatat = True
if "filter_kategori" not in st.session_state:
    st.session_state.filter_kategori = "Semua"

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_rp(n):
    return f"Rp {n:,.0f}".replace(",", ".")

def total_keranjang():
    return sum(p["harga"] * p["qty"] for p in st.session_state.keranjang.values())

def jumlah_item():
    return sum(p["qty"] for p in st.session_state.keranjang.values())

def tambah_ke_keranjang(produk, qty):
    pid = str(produk["id"])
    if pid in st.session_state.keranjang:
        st.session_state.keranjang[pid]["qty"] += qty
    else:
        st.session_state.keranjang[pid] = {**produk, "qty": qty}

def hapus_dari_keranjang(pid):
    if str(pid) in st.session_state.keranjang:
        del st.session_state.keranjang[str(pid)]

# ── PAGES ─────────────────────────────────────────────────────────────────────

def page_beranda():
    # Hero
    st.markdown(f"""
    <div class="hero-banner">
        <h1>🍎 {TOKO_NAMA}</h1>
        <div class="tagline">Menjual Aneka Buah Lokal dan Impor · Segar Setiap Hari</div>
        <div>
            <span class="hero-badge">🌿 Buah Lokal</span>
            <span class="hero-badge">✈️ Buah Impor</span>
            <span class="hero-badge">🎁 Parcel Buah</span>
            <span class="hero-badge">🚚 Antar ke Rumah</span>
        </div>
        <div class="hero-info">
            <span>📍 {TOKO_ALAMAT[:40]}...</span>
            <span>📞 {TOKO_TELP}</span>
            <span>🕐 {TOKO_JAM}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol navigasi utama
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🛒 Pesan Sekarang", use_container_width=True, type="primary"):
            st.session_state.halaman = "Pesan"
            st.rerun()
    with c2:
        if st.button("🛍️ Lihat Keranjang", use_container_width=True):
            st.session_state.halaman = "Keranjang"
            st.rerun()
    with c3:
        st.link_button(
            "📍 Temukan di Maps",
            "https://maps.google.com/?q=Jl.+Mandala+Raya+RT.02+RW.02+Ciparigi+Bogor+Utara",
            use_container_width=True,
        )
    with c4:
        if st.button("📊 Statistik Toko", use_container_width=True):
            st.session_state.halaman = "Statistik"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Info toko
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown('<div class="section-title">📋 Informasi Toko</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="order-section">
            <p>📍 <b>Alamat:</b><br>{TOKO_ALAMAT}</p>
            <p>📞 <b>Telepon / WA:</b> {TOKO_TELP}</p>
            <p>🕐 <b>Jam Buka:</b> {TOKO_JAM}</p>
            <p>🌿 <b>Produk:</b> Buah Lokal, Buah Impor, Parcel Buah</p>
            <a class="maps-btn" href="https://maps.google.com/?q=Jl.+Mandala+Raya+RT.02+RW.02+Ciparigi+Bogor+Utara" target="_blank">
                🗺️ Buka Google Maps
            </a>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="section-title">⭐ Produk Unggulan</div>', unsafe_allow_html=True)
        unggulan = [p for p in PRODUK if p["kategori"] != "Parcel"][:4]
        r1, r2 = st.columns(2)
        for i, p in enumerate(unggulan):
            col = r1 if i % 2 == 0 else r2
            with col:
                st.markdown(f"""
                <div class="product-card" style="margin-bottom:10px;">
                    <span class="product-emoji">{p['emoji']}</span>
                    <div class="product-name">{p['nama']}</div>
                    <div class="product-price">{fmt_rp(p['harga'])}</div>
                    <div class="product-satuan">{p['satuan']}</div>
                </div>""", unsafe_allow_html=True)

    # Parcel section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎁 Parcel Buah Spesial</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        🎁 Tersedia parcel buah untuk berbagai keperluan: lebaran, ulang tahun, arisan, dan acara spesial lainnya.
        Hubungi kami untuk informasi lebih lanjut!
    </div>
    """, unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    parcel_produk = [p for p in PRODUK if p["kategori"] == "Parcel"]
    cols_p = [pc1, pc2, pc3]
    for i, p in enumerate(parcel_produk):
        with cols_p[i]:
            st.markdown(f"""
            <div class="product-card">
                <span class="product-emoji">{p['emoji']}</span>
                <div class="product-name">{p['nama']}</div>
                <div class="product-price">{fmt_rp(p['harga'])}</div>
                <div class="product-satuan">{p['satuan']}</div>
                <div class="badge-parcel">Parcel</div>
            </div>""", unsafe_allow_html=True)


def page_pesan():
    st.markdown('<div class="section-title">🛒 Katalog Buah</div>', unsafe_allow_html=True)

    # Filter kategori
    cats = ["Semua", "Lokal", "Impor", "Parcel"]
    cols_tab = st.columns(len(cats))
    for i, cat in enumerate(cats):
        with cols_tab[i]:
            aktif = st.session_state.filter_kategori == cat
            if st.button(
                cat,
                key=f"tab_{cat}",
                type="primary" if aktif else "secondary",
                use_container_width=True,
            ):
                st.session_state.filter_kategori = cat
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    produk_tampil = PRODUK if st.session_state.filter_kategori == "Semua" else [
        p for p in PRODUK if p["kategori"] == st.session_state.filter_kategori
    ]

    # Grid produk 3 kolom
    for row_start in range(0, len(produk_tampil), 3):
        row_items = produk_tampil[row_start:row_start + 3]
        cols = st.columns(3)
        for i, p in enumerate(row_items):
            with cols[i]:
                badge_class = (
                    "badge-lokal"  if p["kategori"] == "Lokal"  else
                    "badge-impor"  if p["kategori"] == "Impor"  else
                    "badge-parcel"
                )
                st.markdown(f"""
                <div class="product-card">
                    <span class="product-emoji">{p['emoji']}</span>
                    <div class="product-name">{p['nama']}</div>
                    <div class="{badge_class}">{p['kategori']}</div><br>
                    <div class="product-price">{fmt_rp(p['harga'])}</div>
                    <div class="product-satuan">{p['satuan']}</div>
                </div>""", unsafe_allow_html=True)
                qty = st.number_input(
                    "Jumlah",
                    min_value=1, max_value=50, value=1,
                    key=f"qty_{p['id']}",
                    label_visibility="collapsed",
                )
                if st.button(f"+ Keranjang", key=f"add_{p['id']}", use_container_width=True):
                    tambah_ke_keranjang(p, qty)
                    st.success(f"✅ {p['nama']} ditambahkan!")
                st.markdown("<br>", unsafe_allow_html=True)

    # Tombol lihat keranjang
    if jumlah_item() > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            f"🛍️ Lihat Keranjang ({jumlah_item()} item) · {fmt_rp(total_keranjang())}",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.halaman = "Keranjang"
            st.rerun()


def page_keranjang():
    st.markdown('<div class="section-title">🛍️ Keranjang Belanja</div>', unsafe_allow_html=True)

    if not st.session_state.keranjang:
        st.info("🛒 Keranjang masih kosong. Yuk pilih buah segar dulu!")
        if st.button("🍎 Lihat Katalog", type="primary"):
            st.session_state.halaman = "Pesan"
            st.rerun()
        return

    # Tabel keranjang
    for pid, item in list(st.session_state.keranjang.items()):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        with c1:
            st.markdown(f"""
            <div style="padding:6px 0;">
                <span style="font-size:1.4rem;">{item['emoji']}</span>
                <b style="color:#1a4a05;"> {item['nama']}</b><br>
                <small style="color:#6aaa3a;">{item['satuan']}</small>
            </div>""", unsafe_allow_html=True)
        with c2:
            new_qty = st.number_input(
                "Qty", min_value=1, max_value=50,
                value=item["qty"], key=f"kqty_{pid}",
                label_visibility="collapsed"
            )
            st.session_state.keranjang[pid]["qty"] = new_qty
        with c3:
            st.markdown(f"""
            <div style="padding:10px 0; font-weight:800; color:#2d6a0a;">
                {fmt_rp(item['harga'] * new_qty)}
            </div>""", unsafe_allow_html=True)
        with c4:
            if st.button("✕", key=f"del_{pid}"):
                hapus_dari_keranjang(pid)
                st.rerun()

    st.divider()
    st.markdown(f"""
    <div style="text-align:right; font-size:1.2rem; font-weight:900; color:#2d6a0a; padding:6px 0;">
        Total: {fmt_rp(total_keranjang())}
    </div>""", unsafe_allow_html=True)

    # Form order
    st.markdown('<div class="section-title" style="margin-top:1.5rem;">📝 Data Pemesanan</div>', unsafe_allow_html=True)
    with st.container():
        nama   = st.text_input("👤 Nama Lengkap Pemesan", placeholder="Contoh: Budi Santoso")
        wa     = st.text_input("📱 Nomor WhatsApp", placeholder="Contoh: 08123456789")
        alamat = st.text_area("📍 Alamat Pengiriman", placeholder="Tulis alamat lengkap...")
        catatan = st.text_area("📋 Catatan Tambahan (opsional)", placeholder="Misal: buah yang matang, dll.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Konfirmasi & Pesan via WhatsApp", type="primary", use_container_width=True):
            if not nama or not wa or not alamat:
                st.error("⚠️ Mohon isi nama, nomor WA, dan alamat terlebih dahulu!")
            else:
                # Simpan pesanan
                items_list = [
                    {"nama": v["nama"], "qty": v["qty"], "harga": v["harga"],
                     "subtotal": v["qty"] * v["harga"]}
                    for v in st.session_state.keranjang.values()
                ]
                order_id = tambah_pesanan(nama, wa, alamat, items_list, total_keranjang())

                # Buat pesan WA
                detail = "\n".join([
                    f"- {it['nama']} {it['qty']}x @ {fmt_rp(it['harga'])} = {fmt_rp(it['subtotal'])}"
                    for it in items_list
                ])
                if catatan:
                    detail += f"\n\n📋 Catatan: {catatan}"

                import urllib.parse
                pesan = urllib.parse.quote(
                    f"*PESANAN TOKO BUAH ABS*\n"
                    f"No. Order: #{order_id}\n\n"
                    f"*Nama:* {nama}\n"
                    f"*Alamat:* {alamat}\n\n"
                    f"*Detail Pesanan:*\n{detail}\n\n"
                    f"*TOTAL: {fmt_rp(total_keranjang())}*\n\n"
                    f"Mohon konfirmasi ketersediaan dan estimasi pengiriman. Terima kasih! 🙏"
                )
                wa_url = f"https://wa.me/{TOKO_WA}?text={pesan}"

                st.success(f"✅ Pesanan #{order_id} berhasil dicatat! Klik tombol di bawah untuk konfirmasi.")
                st.markdown(f'<a class="wa-btn" href="{wa_url}" target="_blank">💬 Kirim Pesanan via WhatsApp</a>', unsafe_allow_html=True)
                st.session_state.keranjang = {}


def page_statistik():
    data = load_data()
    pesanan = data.get("pesanan", [])
    pengunjung = data.get("pengunjung", 0)

    st.markdown('<div class="section-title">📊 Data Statistik Toko</div>', unsafe_allow_html=True)

    total_pesanan = len(pesanan)
    total_pemasukan = sum(p["total"] for p in pesanan)
    rata_order = total_pemasukan / total_pesanan if total_pesanan > 0 else 0

    # Stat cards
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">👥 {pengunjung}</div>
            <div class="stat-label">Total Pengunjung</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#f59e0b;">
            <div class="stat-val">🛒 {total_pesanan}</div>
            <div class="stat-label">Total Pesanan</div>
        </div>""", unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#10b981;">
            <div class="stat-val">💰</div>
            <div class="stat-label">Total Pemasukan<br><b style="font-size:1rem;color:#2d6a0a;">{fmt_rp(total_pemasukan)}</b></div>
        </div>""", unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#6366f1;">
            <div class="stat-val">📦</div>
            <div class="stat-label">Rata-rata/Pesanan<br><b style="font-size:1rem;color:#2d6a0a;">{fmt_rp(rata_order)}</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Laporan Keuangan ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📅 Laporan Keuangan</div>', unsafe_allow_html=True)

    filter_tab = st.radio(
        "Periode:", ["Harian", "Bulanan", "Tahunan"],
        horizontal=True, label_visibility="collapsed"
    )

    if not pesanan:
        st.info("Belum ada data pesanan.")
        return

    df_raw = pd.DataFrame(pesanan)
    df_raw["tanggal"] = pd.to_datetime(df_raw["tanggal"])
    df_raw["bulan"]   = df_raw["tanggal"].dt.to_period("M").astype(str)
    df_raw["tahun"]   = df_raw["tanggal"].dt.year.astype(str)

    if filter_tab == "Harian":
        pilih = st.date_input("Pilih tanggal:", value=date.today())
        df_f  = df_raw[df_raw["tanggal"].dt.date == pilih]
        label = str(pilih)
    elif filter_tab == "Bulanan":
        bulan_list = sorted(df_raw["bulan"].unique(), reverse=True)
        pilih = st.selectbox("Pilih bulan:", bulan_list)
        df_f  = df_raw[df_raw["bulan"] == pilih]
        label = pilih
    else:
        tahun_list = sorted(df_raw["tahun"].unique(), reverse=True)
        pilih = st.selectbox("Pilih tahun:", tahun_list)
        df_f  = df_raw[df_raw["tahun"] == pilih]
        label = pilih

    if df_f.empty:
        st.warning(f"Tidak ada pesanan untuk periode ini.")
        return

    # Tabel tampilan
    tampil = df_f[["id","tanggal","waktu","nama","alamat","total"]].copy()
    tampil.columns = ["No. Order","Tanggal","Waktu","Nama","Alamat","Total (Rp)"]
    tampil["Tanggal"] = tampil["Tanggal"].dt.strftime("%d-%m-%Y")
    tampil["Total (Rp)"] = tampil["Total (Rp)"].apply(fmt_rp)
    st.dataframe(tampil, use_container_width=True, hide_index=True)

    total_periode = df_f["total"].sum()
    st.markdown(f"""
    <div style="text-align:right;font-size:1.1rem;font-weight:800;color:#2d6a0a;padding:8px 0;">
        Total Pemasukan ({label}): {fmt_rp(total_periode)}
    </div>""", unsafe_allow_html=True)

    # ── Grafik ────────────────────────────────────────────────────────────────
    if filter_tab == "Bulanan":
        chart_df = df_f.groupby(df_f["tanggal"].dt.day)["total"].sum().reset_index()
        chart_df.columns = ["Tanggal", "Pemasukan"]
        st.bar_chart(chart_df.set_index("Tanggal"))
    elif filter_tab == "Tahunan":
        chart_df = df_f.groupby("bulan")["total"].sum().reset_index()
        chart_df.columns = ["Bulan", "Pemasukan"]
        st.bar_chart(chart_df.set_index("Bulan"))

    # ── Export Excel ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📥 Export Laporan</div>', unsafe_allow_html=True)

    # Buat Excel multi-sheet
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Sheet 1: Ringkasan
        ringkasan = pd.DataFrame({
            "Keterangan": ["Periode", "Total Pesanan", "Total Pemasukan", "Rata-rata per Pesanan"],
            "Nilai": [label, len(df_f), fmt_rp(total_periode), fmt_rp(total_periode/len(df_f))]
        })
        ringkasan.to_excel(writer, sheet_name="Ringkasan", index=False)

        # Sheet 2: Detail pesanan
        detail_df = df_f[["id","tanggal","waktu","nama","wa","alamat","total"]].copy()
        detail_df.columns = ["No Order","Tanggal","Waktu","Nama","WA","Alamat","Total (Rp)"]
        detail_df["Tanggal"] = detail_df["Tanggal"].dt.strftime("%d-%m-%Y")
        detail_df.to_excel(writer, sheet_name="Detail Pesanan", index=False)

        # Sheet 3: Detail item
        all_items = []
        for _, row in df_f.iterrows():
            for it in row["items"]:
                all_items.append({
                    "No Order": row["id"],
                    "Tanggal": row["tanggal"].strftime("%d-%m-%Y"),
                    "Produk": it["nama"],
                    "Qty": it["qty"],
                    "Harga Satuan (Rp)": it["harga"],
                    "Subtotal (Rp)": it["subtotal"],
                })
        if all_items:
            pd.DataFrame(all_items).to_excel(writer, sheet_name="Detail Item", index=False)

    st.download_button(
        label="📊 Download Laporan Excel",
        data=output.getvalue(),
        file_name=f"laporan_toko_buah_abs_{label}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    inject_css()

    # Navbar
    cart_count = jumlah_item()
    menu_items = {
        "Beranda":    "🏠 Beranda",
        "Pesan":      "🛒 Pesan",
        "Keranjang":  f"🛍️ Keranjang ({cart_count})" if cart_count else "🛍️ Keranjang",
        "Statistik":  "📊 Statistik",
    }
    col_nav = st.columns(len(menu_items))
    for i, (key, label) in enumerate(menu_items.items()):
        with col_nav[i]:
            aktif = st.session_state.halaman == key
            if st.button(label, key=f"nav_{key}", type="primary" if aktif else "secondary", use_container_width=True):
                st.session_state.halaman = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Route
    halaman = st.session_state.halaman
    if halaman == "Beranda":
        page_beranda()
    elif halaman == "Pesan":
        page_pesan()
    elif halaman == "Keranjang":
        page_keranjang()
    elif halaman == "Statistik":
        page_statistik()


if __name__ == "__main__":
    main()
