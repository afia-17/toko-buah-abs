import streamlit as st
import pandas as pd
import json, os, urllib.parse, io
from datetime import datetime, date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Toko Buah ABS",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Constants ──────────────────────────────────────────────────────────────────
TOKO_WA      = "6281212408274"
TOKO_NAMA    = "Toko Buah ABS"
TOKO_ALAMAT  = "Jl. Mandala Raya, RT.02/RW.02, Ciparigi, Kec. Bogor Utara, Kota Bogor, Jawa Barat 16157"
TOKO_JAM     = "08.00 - 21.30 WIB (Setiap Hari)"
TOKO_TELP    = "081212408274"
MAPS_URL     = "https://maps.google.com/?q=Jl.+Mandala+Raya+RT.02+RW.02+Ciparigi+Bogor+Utara+Kota+Bogor"
DATA_FILE    = "data_pesanan.json"
ADMIN_PASS   = "absadmin2024"  # Ganti sesuai kebutuhan

PRODUK = [
    # ── BUAH LOKAL ────────────────────────────────────────────────────────────
    {
        "id": 1, "nama": "Jeruk Siam Pontianak",
        "emoji": "🍊", "harga": 18000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Jeruk siam lokal, manis-asam segar"
    },
    {
        "id": 2, "nama": "Jeruk Santang / Baby",
        "emoji": "🟠", "harga": 15000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Jeruk kecil manis, kulit tipis mudah dikupas"
    },
    {
        "id": 3, "nama": "Mangga Harum Manis",
        "emoji": "🥭", "harga": 20000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Mangga lokal premium, manis legit tanpa serat"
    },
    {
        "id": 4, "nama": "Buah Naga Merah",
        "emoji": "🔴", "harga": 20000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Buah naga merah, kaya antioksidan"
    },
    {
        "id": 5, "nama": "Pisang Cavendish",
        "emoji": "🍌", "harga": 16000, "satuan": "per sisir",
        "kategori": "Lokal", "stok": True,
        "info": "Pisang kuning segar, manis dan lembut"
    },
    {
        "id": 6, "nama": "Belimbing Dewi",
        "emoji": "⭐", "harga": 10000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Belimbing segar manis, cocok untuk jus"
    },
    {
        "id": 7, "nama": "Salak Pondoh",
        "emoji": "🤎", "harga": 16000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Salak pondoh Sleman, manis renyah"
    },
    {
        "id": 8, "nama": "Melon Hijau",
        "emoji": "🍈", "harga": 12000, "satuan": "per kg",
        "kategori": "Lokal", "stok": True,
        "info": "Melon hijau segar, daging tebal dan manis"
    },
    {
        "id": 9, "nama": "Nanas Subang",
        "emoji": "🍍", "harga": 10000, "satuan": "per buah",
        "kategori": "Lokal", "stok": True,
        "info": "Nanas subang, manis asam segar"
    },
    # ── BUAH IMPOR ────────────────────────────────────────────────────────────
    {
        "id": 10, "nama": "Apel Fuji (Hijau Import)",
        "emoji": "🍏", "harga": 35000, "satuan": "per kg",
        "kategori": "Impor", "stok": True,
        "info": "Apel hijau segar dari China, renyah & asam manis"
    },
    {
        "id": 11, "nama": "Apel Washington (Merah Import)",
        "emoji": "🍎", "harga": 32000, "satuan": "per kg",
        "kategori": "Impor", "stok": True,
        "info": "Apel merah Washington import, manis dan renyah"
    },
    {
        "id": 12, "nama": "Apel Pink Lady",
        "emoji": "🌸", "harga": 45000, "satuan": "per kg",
        "kategori": "Impor", "stok": True,
        "info": "Apel Pink Lady premium import, manis berbuih khas"
    },
    {
        "id": 13, "nama": "Anggur Red Globe (Merah Import)",
        "emoji": "🍇", "harga": 45000, "satuan": "per kg",
        "kategori": "Impor", "stok": True,
        "info": "Anggur merah besar import, manis dan berair"
    },
    {
        "id": 14, "nama": "Kelengkeng Bangkok",
        "emoji": "🟡", "harga": 32000, "satuan": "per kg",
        "kategori": "Impor", "stok": True,
        "info": "Kelengkeng Bangkok, manis daging tebal"
    },
    # ── PARCEL ────────────────────────────────────────────────────────────────
    {
        "id": 15, "nama": "Parcel Buah Kecil",
        "emoji": "🎁", "harga": 75000, "satuan": "per paket",
        "kategori": "Parcel", "stok": True,
        "info": "Pisang, Jeruk Siam, Apel Merah, Belimbing",
        "isi": "Pisang Cavendish, Jeruk Siam, Apel Merah, Belimbing (sekitar 4 jenis buah pilihan)"
    },
    {
        "id": 16, "nama": "Parcel Buah Sedang",
        "emoji": "🎁", "harga": 125000, "satuan": "per paket",
        "kategori": "Parcel", "stok": True,
        "info": "Mangga, Anggur, Apel Hijau, Pisang, Jeruk, Melon",
        "isi": "Mangga Harum Manis, Anggur Merah, Apel Hijau, Pisang, Jeruk Siam, Melon Hijau (sekitar 6 jenis buah pilihan)"
    },
    {
        "id": 17, "nama": "Parcel Buah Besar",
        "emoji": "🎁", "harga": 200000, "satuan": "per paket",
        "kategori": "Parcel", "stok": True,
        "info": "9-10 jenis buah premium pilihan",
        "isi": "Mangga, Anggur, Kelengkeng, Apel Pink Lady, Apel Merah, Buah Naga, Melon, Nanas, Jeruk Siam (sekitar 9-10 jenis buah premium)"
    },
]

# ── Data helpers ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"pesanan": [], "pengunjung": 0, "saran": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tambah_pesanan(nama, wa, alamat, items, total, pembayaran):
    data = load_data()
    new = {
        "id":        len(data["pesanan"]) + 1,
        "tanggal":   datetime.now().strftime("%Y-%m-%d"),
        "waktu":     datetime.now().strftime("%H:%M"),
        "nama":      nama, "wa": wa, "alamat": alamat,
        "items":     items, "total": total,
        "pembayaran": pembayaran, "status": "Baru",
    }
    data["pesanan"].append(new)
    save_data(data)
    return new["id"]

def catat_pengunjung():
    data = load_data()
    data["pengunjung"] = data.get("pengunjung", 0) + 1
    save_data(data)

# ── Session init ───────────────────────────────────────────────────────────────
if "keranjang"          not in st.session_state: st.session_state.keranjang = {}
if "halaman"            not in st.session_state: st.session_state.halaman   = "Beranda"
if "filter_kat"         not in st.session_state: st.session_state.filter_kat= "Semua"
if "admin_login"        not in st.session_state: st.session_state.admin_login = False
if "pengunjung_dicatat" not in st.session_state:
    catat_pengunjung()
    st.session_state.pengunjung_dicatat = True

# ── Helpers ────────────────────────────────────────────────────────────────────
def fmt_rp(n):   return "Rp {:,.0f}".format(int(n)).replace(",", ".")
def total_krj(): return sum(v["harga"] * v["qty"] for v in st.session_state.keranjang.values())
def jml_item():  return sum(v["qty"] for v in st.session_state.keranjang.values())

def tambah_krj(p, qty):
    pid = str(p["id"])
    if pid in st.session_state.keranjang:
        st.session_state.keranjang[pid]["qty"] += qty
    else:
        st.session_state.keranjang[pid] = {**p, "qty": qty}

def hapus_krj(pid):
    if str(pid) in st.session_state.keranjang:
        del st.session_state.keranjang[str(pid)]

# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@500;600;700;800&display=swap');
html,[class*="css"]{font-family:'Nunito',sans-serif!important;}
.stApp{background:#f4fbee;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}

/* ── HERO ── */
.hero{background:linear-gradient(135deg,#1a4a05 0%,#2d8a0e 55%,#5aba2a 100%);
  border-radius:22px;padding:2.5rem 2rem 2rem;margin-bottom:1.4rem;color:white;
  text-align:center;box-shadow:0 10px 40px rgba(45,138,14,.35);position:relative;overflow:hidden;}
.hero::after{content:"🍎  🥭  🍊  🍌  🍇  🍈  🍍  🐉";position:absolute;bottom:6px;
  left:0;right:0;font-size:18px;letter-spacing:16px;opacity:.15;white-space:nowrap;}
.hero h1{font-family:'Poppins',sans-serif!important;font-size:2.8rem!important;
  font-weight:900!important;margin:0!important;color:white!important;
  text-shadow:0 3px 12px rgba(0,0,0,.25);}
.hero .sub{font-size:1.05rem;opacity:.92;font-weight:700;margin:.4rem 0 1rem;}
.hero-badges{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:1rem;}
.hbadge{background:rgba(255,255,255,.2);border:1.5px solid rgba(255,255,255,.4);
  border-radius:30px;padding:5px 16px;font-size:.82rem;font-weight:700;}
.hero-info{display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;
  font-size:.8rem;opacity:.85;}
.hero-info span{display:flex;align-items:center;gap:4px;}

/* ── SECTION TITLE ── */
.sec-title{font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:800;
  color:#1a4a05;border-left:5px solid #4caf1e;padding-left:12px;margin-bottom:1rem;}
.sec-title-admin{font-family:'Poppins',sans-serif;font-size:1.1rem;font-weight:800;
  color:#1e3a5f;border-left:5px solid #2d5f9e;padding-left:12px;margin:1.2rem 0 .8rem;}

/* ── PRODUCT CARD ── */
.pcard{background:white;border-radius:18px;padding:1.1rem;text-align:center;
  box-shadow:0 2px 14px rgba(0,0,0,.07);border:1.5px solid #e0f2d0;
  transition:transform .15s,box-shadow .15s;height:100%;}
.pcard:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(76,175,30,.18);border-color:#5aba2a;}
.pemoji{font-size:3rem;display:block;margin-bottom:.3rem;}
.pname{font-size:.88rem;font-weight:800;color:#1a4a05;margin-bottom:3px;}
.pinfo{font-size:.68rem;color:#6aaa40;margin-bottom:5px;font-style:italic;}
.pprice{font-size:1rem;font-weight:800;color:#2d6a0a;background:#edfadd;
  padding:3px 14px;border-radius:20px;display:inline-block;margin-bottom:6px;}
.psatuan{font-size:.72rem;color:#5aaa25;margin-bottom:6px;}
.pisi{font-size:.68rem;color:#557a3a;background:#f5fdf0;border-radius:8px;
  padding:5px 8px;margin:4px 0 6px;line-height:1.5;text-align:left;}
.bl{font-size:.68rem;padding:2px 10px;border-radius:20px;font-weight:700;display:inline-block;margin-bottom:5px;}
.bl-lokal{background:#d4edda;color:#155724;}
.bl-impor{background:#cce5ff;color:#004085;}
.bl-parcel{background:#fff3cd;color:#856404;}

/* ── CART & ORDER ── */
.osec{background:white;border-radius:16px;padding:1.4rem;
  box-shadow:0 2px 12px rgba(0,0,0,.07);border:1.5px solid #e0f2d0;}
.total-box{text-align:right;font-size:1.15rem;font-weight:900;color:#2d6a0a;padding:8px 0;}

/* ── PAYMENT ── */
.pay-sel{border-radius:12px;padding:.9rem 1.1rem;margin:.4rem 0;
  border:2px solid transparent;cursor:pointer;}
.pay-tunai{background:#f0fdf4;border-color:#16a34a;}
.pay-nontunai{background:#eff6ff;border-color:#2563eb;}
.info-green{background:#f0fdf4;border:1.5px solid #86efac;border-radius:12px;
  padding:.8rem 1rem;font-size:.84rem;color:#14532d;margin:.5rem 0;}
.info-blue{background:#eff6ff;border:1.5px solid #93c5fd;border-radius:12px;
  padding:.8rem 1rem;font-size:.84rem;color:#1e3a5f;margin:.5rem 0;}
.info-yellow{background:#fffbeb;border:1.5px solid #fcd34d;border-radius:12px;
  padding:.9rem 1.1rem;font-size:.85rem;color:#78350f;margin-bottom:1rem;}

/* ── WA BUTTON ── */
.wa-link{display:block;width:100%;background:#25D366;color:white!important;
  text-align:center;padding:14px;border-radius:12px;font-weight:800;font-size:1rem;
  text-decoration:none;margin-top:10px;box-shadow:0 4px 14px rgba(37,211,102,.35);}
.wa-link:hover{background:#1da851;}
.maps-link{display:inline-block;background:#4285F4;color:white!important;
  padding:9px 20px;border-radius:10px;font-weight:700;font-size:.85rem;
  text-decoration:none;box-shadow:0 3px 10px rgba(66,133,244,.3);}

/* ── ADMIN ── */
.admin-header{background:linear-gradient(135deg,#1e3a5f 0%,#2d5f9e 60%,#4a90d9 100%);
  border-radius:18px;padding:1.8rem 2rem 1.5rem;margin-bottom:1.5rem;color:white;text-align:center;
  box-shadow:0 8px 30px rgba(30,58,95,.35);}
.admin-header h2{font-family:'Poppins',sans-serif!important;font-size:1.8rem!important;
  font-weight:800!important;margin:0!important;color:white!important;}
.scard{background:white;border-radius:16px;padding:1.2rem 1rem;text-align:center;
  box-shadow:0 2px 12px rgba(0,0,0,.08);}
.sval{font-size:1.8rem;font-weight:900;}
.slbl{font-size:.74rem;font-weight:700;margin-top:4px;color:#666;}
.pay-tunai-badge{background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:700;}
.pay-nontunai-badge{background:#dbeafe;color:#1e3a5f;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:700;}
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN PUBLIK
# ══════════════════════════════════════════════════════════════════════════════

def pg_beranda():
    st.markdown(f"""
<div class="hero">
  <h1>🍎 {TOKO_NAMA}</h1>
  <div class="sub">Menjual Aneka Buah Lokal dan Impor &middot; Segar Setiap Hari</div>
  <div class="hero-badges">
    <span class="hbadge">🌿 Buah Lokal</span>
    <span class="hbadge">✈️ Buah Impor</span>
    <span class="hbadge">🎁 Parcel Buah</span>
    <span class="hbadge">🚚 Antar ke Rumah</span>
    <span class="hbadge">💳 QRIS &amp; Tunai</span>
  </div>
  <div class="hero-info">
    <span>📍 Ciparigi, Bogor Utara</span>
    <span>📞 {TOKO_TELP}</span>
    <span>🕐 {TOKO_JAM}</span>
  </div>
</div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🛒 Pesan Sekarang", use_container_width=True, type="primary"):
            st.session_state.halaman = "Pesan"; st.rerun()
    with c2:
        n = jml_item()
        label = f"🛍️ Keranjang ({n})" if n else "🛍️ Keranjang"
        if st.button(label, use_container_width=True):
            st.session_state.halaman = "Keranjang"; st.rerun()
    with c3:
        st.link_button("📍 Google Maps", MAPS_URL, use_container_width=True)
    with c4:
        if st.button("📞 Kontak & Saran", use_container_width=True):
            st.session_state.halaman = "Kontak"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="sec-title">📋 Informasi Toko</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="osec">
  <p>📍 <b>Alamat</b><br><small>{TOKO_ALAMAT}</small></p><br>
  <p>📞 <b>Telepon / WA:</b> {TOKO_TELP}</p>
  <p>🕐 <b>Jam Buka:</b> {TOKO_JAM}</p>
  <p>💳 <b>Pembayaran:</b> Tunai (saat bertemu) &amp; Non-Tunai (QRIS / Transfer)</p>
  <p>🌿 <b>Produk:</b> Buah Lokal, Buah Impor &amp; Parcel Buah</p><br>
  <a class="maps-link" href="{MAPS_URL}" target="_blank">🗺️ Buka Google Maps</a>
</div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="sec-title">⭐ Produk Unggulan</div>', unsafe_allow_html=True)
        unggulan = [p for p in PRODUK if p["kategori"] != "Parcel"][:4]
        r1, r2 = st.columns(2)
        for i, p in enumerate(unggulan):
            col = r1 if i % 2 == 0 else r2
            with col:
                st.markdown(f"""
<div class="pcard" style="margin-bottom:10px;">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']}</div>
</div>""", unsafe_allow_html=True)

    # Parcel section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">🎁 Parcel Buah Spesial</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-yellow">
  🎁 Tersedia parcel buah untuk lebaran, ulang tahun, pernikahan, dan acara spesial.
  Dikemas cantik dengan buah-buah segar pilihan. Hubungi kami untuk pemesanan massal!
</div>""", unsafe_allow_html=True)

    parcels = [p for p in PRODUK if p["kategori"] == "Parcel"]
    pc = st.columns(len(parcels))
    for i, p in enumerate(parcels):
        with pc[i]:
            st.markdown(f"""
<div class="pcard">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <span class="bl bl-parcel">Parcel</span><br>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']}</div>
  <div class="pisi">🍃 Isi: {p.get('isi', '')}</div>
</div>""", unsafe_allow_html=True)


def pg_pesan():
    st.markdown('<div class="sec-title">🛒 Katalog Buah Segar</div>', unsafe_allow_html=True)

    cats = ["Semua", "Lokal", "Impor", "Parcel"]
    cols_t = st.columns(len(cats))
    for i, c in enumerate(cats):
        with cols_t[i]:
            aktif = st.session_state.filter_kat == c
            if st.button(c, key=f"t_{c}", type="primary" if aktif else "secondary",
                         use_container_width=True):
                st.session_state.filter_kat = c; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    tampil = PRODUK if st.session_state.filter_kat == "Semua" else [
        p for p in PRODUK if p["kategori"] == st.session_state.filter_kat]

    for r in range(0, len(tampil), 3):
        row = tampil[r:r + 3]
        cols = st.columns(3)
        for i, p in enumerate(row):
            with cols[i]:
                badge_cls = ("bl-lokal" if p["kategori"] == "Lokal"
                             else "bl-impor" if p["kategori"] == "Impor"
                             else "bl-parcel")
                isi_html = f'<div class="pisi">🍃 {p["isi"]}</div>' if "isi" in p else ""
                st.markdown(f"""
<div class="pcard">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <span class="bl {badge_cls}">{p['kategori']}</span><br>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']}</div>
  <div class="pinfo">{p.get('info', '')}</div>
  {isi_html}
</div>""", unsafe_allow_html=True)
                if p["stok"]:
                    qty = st.number_input("Jumlah", min_value=1, max_value=50, value=1,
                                          key=f"qty_{p['id']}", label_visibility="collapsed")
                    if st.button("+ Keranjang", key=f"add_{p['id']}", use_container_width=True):
                        tambah_krj(p, qty)
                        st.success(f"Ditambahkan: {p['nama']}")
                else:
                    st.button("Stok Habis", key=f"add_{p['id']}", disabled=True,
                              use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)

    if jml_item() > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🛍️ Lihat Keranjang ({jml_item()} item) — {fmt_rp(total_krj())}",
                     type="primary", use_container_width=True):
            st.session_state.halaman = "Keranjang"; st.rerun()


def pg_keranjang():
    st.markdown('<div class="sec-title">🛍️ Keranjang Belanja</div>', unsafe_allow_html=True)

    if not st.session_state.keranjang:
        st.info("Keranjang masih kosong. Yuk pilih buah segar dulu!")
        if st.button("🍎 Lihat Katalog", type="primary"):
            st.session_state.halaman = "Pesan"; st.rerun()
        return

    for pid, item in list(st.session_state.keranjang.items()):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        with c1:
            st.markdown(f"""
<div style="padding:6px 0;">
  <span style="font-size:1.3rem;">{item['emoji']}</span>
  <b style="color:#1a4a05;"> {item['nama']}</b><br>
  <small style="color:#5aaa25;">{item['satuan']}</small>
</div>""", unsafe_allow_html=True)
        with c2:
            nq = st.number_input("Qty", min_value=1, max_value=50, value=item["qty"],
                                  key=f"kq_{pid}", label_visibility="collapsed")
            st.session_state.keranjang[pid]["qty"] = nq
        with c3:
            st.markdown(
                f'<div style="padding:10px 0;font-weight:800;color:#2d6a0a;">'
                f'{fmt_rp(item["harga"] * nq)}</div>',
                unsafe_allow_html=True)
        with c4:
            if st.button("x", key=f"del_{pid}"):
                hapus_krj(pid); st.rerun()

    st.divider()
    st.markdown(f'<div class="total-box">Total: {fmt_rp(total_krj())}</div>',
                unsafe_allow_html=True)

    # Form pemesanan
    st.markdown('<div class="sec-title" style="margin-top:1.4rem;">📝 Data Pemesanan</div>',
                unsafe_allow_html=True)
    nama    = st.text_input("Nama Lengkap Pemesan", placeholder="Contoh: Budi Santoso")
    wa      = st.text_input("Nomor WhatsApp", placeholder="Contoh: 08123456789")
    alamat  = st.text_area("Alamat Pengiriman", placeholder="Tulis alamat lengkap...")
    catatan = st.text_area("Catatan Tambahan (opsional)",
                            placeholder="Misal: buah yang matang, dll.")

    # Pilih metode pembayaran
    st.markdown('<div class="sec-title" style="margin-top:1.2rem;">💳 Metode Pembayaran</div>',
                unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
<div class="pay-sel pay-tunai">
  <span style="font-size:1.8rem;">💵</span>
  <b style="color:#15803d;display:block;margin-top:.3rem;">Tunai</b>
  <small style="color:#555;">Bayar saat pesanan tiba / bertemu penjual</small>
</div>""", unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
<div class="pay-sel pay-nontunai">
  <span style="font-size:1.8rem;">📲</span>
  <b style="color:#1d4ed8;display:block;margin-top:.3rem;">Non-Tunai</b>
  <small style="color:#555;">QRIS · Transfer Bank</small>
</div>""", unsafe_allow_html=True)

    pembayaran = st.radio(
        "Pilih:",
        ["💵 Tunai (Bayar saat bertemu / antar)",
         "📲 Non-Tunai (QRIS / Transfer Bank)"],
        label_visibility="collapsed",
    )

    if "Non-Tunai" in pembayaran:
        st.markdown("""
<div class="info-blue">
  📲 <b>Cara pembayaran non-tunai:</b><br>
  &bull; <b>QRIS:</b> Penjual akan kirimkan QR code via WhatsApp untuk di-scan<br>
  &bull; <b>Transfer Bank:</b> Info rekening dikirim via WhatsApp setelah konfirmasi<br>
  &bull; Kirimkan bukti transfer ke WhatsApp penjual untuk konfirmasi pesanan
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="info-green">
  💵 <b>Pembayaran tunai:</b> Siapkan uang saat penjual mengantar. 
  Konfirmasi terlebih dahulu via WhatsApp.
</div>""", unsafe_allow_html=True)

    pay_label = ("Tunai" if "Tunai" in pembayaran
                 else "Non-Tunai (QRIS / Transfer Bank)")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Konfirmasi & Pesan via WhatsApp", type="primary", use_container_width=True):
        if not nama or not wa or not alamat:
            st.error("Mohon isi nama, nomor WA, dan alamat terlebih dahulu!")
        else:
            items_list = [
                {"nama": v["nama"], "qty": v["qty"], "harga": v["harga"],
                 "subtotal": v["qty"] * v["harga"]}
                for v in st.session_state.keranjang.values()
            ]
            oid = tambah_pesanan(nama, wa, alamat, items_list, total_krj(), pay_label)
            detail = "\n".join(
                f"- {it['nama']} {it['qty']}x @ {fmt_rp(it['harga'])} = {fmt_rp(it['subtotal'])}"
                for it in items_list
            )
            if catatan:
                detail += f"\n\nCatatan: {catatan}"
            pay_info = ("Tunai (bayar saat bertemu)" if "Tunai" in pembayaran
                        else "Non-Tunai — QRIS / Transfer Bank")
            pesan = urllib.parse.quote(
                f"PESANAN TOKO BUAH ABS\nNo. Order: #{oid}\n\n"
                f"Nama: {nama}\nAlamat: {alamat}\n\n"
                f"Detail Pesanan:\n{detail}\n\n"
                f"TOTAL: {fmt_rp(total_krj())}\n"
                f"Pembayaran: {pay_info}\n\n"
                f"Mohon konfirmasi ketersediaan dan estimasi pengiriman. Terima kasih!"
            )
            wa_url = f"https://wa.me/{TOKO_WA}?text={pesan}"
            st.success(f"Pesanan #{oid} berhasil dicatat! Klik tombol di bawah.")
            st.markdown(
                f'<a class="wa-link" href="{wa_url}" target="_blank">'
                f'💬 Kirim Pesanan via WhatsApp</a>',
                unsafe_allow_html=True)
            st.session_state.keranjang = {}


def pg_kontak():
    st.markdown('<div class="sec-title">📞 Hubungi Kami</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="osec">
  <h3 style="color:#1a4a05;">🍎 {TOKO_NAMA}</h3>
  <p>📍 <b>Alamat:</b><br>{TOKO_ALAMAT}</p><br>
  <p>📞 <b>Telepon / WhatsApp:</b> {TOKO_TELP}</p>
  <p>🕐 <b>Jam Operasional:</b> {TOKO_JAM}</p>
  <p>💳 <b>Pembayaran:</b> Tunai &amp; Non-Tunai (QRIS, Transfer Bank)</p><br>
  <a class="wa-link" href="https://wa.me/{TOKO_WA}" target="_blank">💬 Chat via WhatsApp</a>
  <br><br>
  <a class="maps-link" href="{MAPS_URL}" target="_blank">🗺️ Lihat di Google Maps</a>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">✍️ Kritik & Saran</div>', unsafe_allow_html=True)
    with st.form("saran_form"):
        nama_s  = st.text_input("Nama (opsional)")
        pesan_s = st.text_area("Pesan / Saran / Kritik")
        sub = st.form_submit_button("Kirim", type="primary", use_container_width=True)
        if sub:
            if pesan_s:
                data = load_data()
                if "saran" not in data:
                    data["saran"] = []
                data["saran"].append({
                    "nama": nama_s or "Anonim",
                    "pesan": pesan_s,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                save_data(data)
                st.success("Terima kasih atas masukan Anda!")
            else:
                st.warning("Tulis pesannya dulu ya!")


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN ADMIN (password-protected, dalam 1 file yang sama)
# ══════════════════════════════════════════════════════════════════════════════

def pg_admin_login():
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
<div style="background:white;border-radius:20px;padding:2.5rem;
  box-shadow:0 8px 30px rgba(0,0,0,.12);text-align:center;margin-top:2rem;">
  <div style="font-size:3rem;">🔐</div>
  <h2 style="color:#1e3a5f;margin:.5rem 0 .3rem;">Login Admin</h2>
  <p style="color:#888;font-size:.85rem;">Toko Buah ABS — Akses Terbatas</p>
</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pwd = st.text_input("Password Admin", type="password",
                             placeholder="Masukkan password...")
        if st.button("Masuk", type="primary", use_container_width=True):
            if pwd == ADMIN_PASS:
                st.session_state.admin_login = True; st.rerun()
            else:
                st.error("Password salah!")
        if st.button("Kembali ke Toko", use_container_width=True):
            st.session_state.halaman = "Beranda"; st.rerun()


def pg_admin_dashboard():
    data       = load_data()
    pesanan    = data.get("pesanan", [])
    pengunjung = data.get("pengunjung", 0)
    saran_list = data.get("saran", [])

    # Admin header
    st.markdown("""
<div class="admin-header">
  <h2>📊 Dashboard Admin</h2>
  <p>Toko Buah ABS &nbsp;|&nbsp; Manajemen & Laporan Keuangan</p>
</div>""", unsafe_allow_html=True)

    col_hd1, col_hd2 = st.columns([5, 1])
    with col_hd2:
        if st.button("🚪 Logout"):
            st.session_state.admin_login = False
            st.session_state.halaman = "Beranda"; st.rerun()

    # Tab navigasi admin
    if "admin_tab" not in st.session_state:
        st.session_state.admin_tab = "📊 Statistik"

    tabs = ["📊 Statistik", "📦 Pesanan", "📅 Laporan Keuangan", "💬 Saran"]
    tcols = st.columns(len(tabs))
    for i, t in enumerate(tabs):
        with tcols[i]:
            aktif = st.session_state.admin_tab == t
            if st.button(t, key=f"at_{i}",
                         type="primary" if aktif else "secondary",
                         use_container_width=True):
                st.session_state.admin_tab = t; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TAB STATISTIK ─────────────────────────────────────────────────────────
    if st.session_state.admin_tab == "📊 Statistik":
        total_p   = len(pesanan)
        total_omz = sum(p["total"] for p in pesanan)
        rata      = total_omz / total_p if total_p else 0

        hari_ini    = date.today().strftime("%Y-%m-%d")
        p_hari      = [p for p in pesanan if p.get("tanggal") == hari_ini]
        omz_hari    = sum(p["total"] for p in p_hari)

        bulan_ini   = date.today().strftime("%Y-%m")
        p_bulan     = [p for p in pesanan if p.get("tanggal", "").startswith(bulan_ini)]
        omz_bulan   = sum(p["total"] for p in p_bulan)

        tunai_cnt    = sum(1 for p in pesanan if "Tunai" in p.get("pembayaran", "") and "Non" not in p.get("pembayaran", ""))
        nontunai_cnt = sum(1 for p in pesanan if "Non" in p.get("pembayaran", ""))

        s1, s2, s3, s4 = st.columns(4)
        cards = [
            (s1, "👥", str(pengunjung),       "Total Pengunjung",    "#2d5f9e"),
            (s2, "🛒", str(total_p),          "Total Pesanan",       "#16a34a"),
            (s3, "💰", fmt_rp(total_omz),     "Total Pemasukan",     "#b45309"),
            (s4, "📦", fmt_rp(rata),          "Rata-rata/Pesanan",   "#7c3aed"),
        ]
        for col, em, v, lbl, clr in cards:
            with col:
                st.markdown(f"""
<div class="scard" style="border-top:4px solid {clr};">
  <div style="font-size:1.6rem;">{em}</div>
  <div class="sval" style="color:{clr};font-size:1.15rem;">{v}</div>
  <div class="slbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        s5, s6, s7, s8 = st.columns(4)
        cards2 = [
            (s5, "📅", f"{len(p_hari)} pesanan",  f"Hari Ini · {fmt_rp(omz_hari)}",   "#0891b2"),
            (s6, "🗓️", f"{len(p_bulan)} pesanan", f"Bulan Ini · {fmt_rp(omz_bulan)}", "#dc2626"),
            (s7, "💵", str(tunai_cnt),             "Pesanan Tunai",                     "#15803d"),
            (s8, "📲", str(nontunai_cnt),          "Pesanan Non-Tunai",                 "#1d4ed8"),
        ]
        for col, em, v, lbl, clr in cards2:
            with col:
                st.markdown(f"""
<div class="scard" style="border-top:4px solid {clr};">
  <div style="font-size:1.5rem;">{em}</div>
  <div class="sval" style="color:{clr};font-size:1.05rem;">{v}</div>
  <div class="slbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

        if pesanan:
            st.markdown('<div class="sec-title-admin">🏆 Produk Terlaris</div>',
                        unsafe_allow_html=True)
            all_items = []
            for p in pesanan:
                for it in p.get("items", []):
                    all_items.append({"nama": it.get("nama", ""), "qty": it.get("qty", 0)})
            if all_items:
                df_i = pd.DataFrame(all_items)
                terlaris = df_i.groupby("nama")["qty"].sum().sort_values(ascending=False).head(8)
                st.bar_chart(terlaris)

            st.markdown('<div class="sec-title-admin">📈 Tren 7 Hari Terakhir</div>',
                        unsafe_allow_html=True)
            df_all = pd.DataFrame(pesanan)
            df_all["tanggal"] = pd.to_datetime(df_all["tanggal"], errors="coerce")
            df_all["total"]   = pd.to_numeric(df_all["total"],   errors="coerce").fillna(0)
            tren = df_all.groupby("tanggal")["total"].sum().tail(7)
            if not tren.empty:
                st.line_chart(tren)

    # ── TAB PESANAN ───────────────────────────────────────────────────────────
    elif st.session_state.admin_tab == "📦 Pesanan":
        st.markdown('<div class="sec-title-admin">📦 Semua Pesanan</div>',
                    unsafe_allow_html=True)
        if not pesanan:
            st.info("Belum ada pesanan.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1: cari = st.text_input("Cari nama", placeholder="Nama pemesan...")
            with c2: tgl  = st.date_input("Filter tanggal", value=None)
            with c3: pay  = st.selectbox("Filter pembayaran",
                                          ["Semua", "Tunai", "Non-Tunai"])

            df = pd.DataFrame(pesanan)
            df["tanggal_dt"] = pd.to_datetime(df["tanggal"], errors="coerce")
            if cari: df = df[df["nama"].str.contains(cari, case=False, na=False)]
            if tgl:  df = df[df["tanggal_dt"].dt.date == tgl]
            if pay != "Semua":
                df = df[df["pembayaran"].str.contains(pay, case=False, na=False)]

            show_cols = [c for c in ["id","tanggal","waktu","nama","wa","alamat",
                                      "total","pembayaran","status"] if c in df.columns]
            df_show = df[show_cols].copy()
            if "total" in df_show.columns:
                df_show["total"] = df_show["total"].apply(
                    lambda x: fmt_rp(float(x)) if x else "-")
            st.dataframe(df_show, use_container_width=True, hide_index=True)

            # Update status
            st.markdown('<div class="sec-title-admin">✏️ Update Status</div>',
                        unsafe_allow_html=True)
            all_ids = [str(p.get("id")) for p in pesanan]
            cu1, cu2, cu3 = st.columns([2, 2, 1])
            with cu1:
                sel = st.selectbox("No. Order:", all_ids, index=len(all_ids)-1)
            with cu2:
                ns = st.selectbox("Status baru:",
                                   ["Baru","Diproses","Dikirim","Selesai","Dibatalkan"])
            with cu3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Update", type="primary", use_container_width=True):
                    data = load_data()
                    for p in data["pesanan"]:
                        if str(p.get("id")) == sel:
                            p["status"] = ns; break
                    save_data(data)
                    st.success(f"Order #{sel} → {ns}"); st.rerun()

            # Detail item
            st.markdown('<div class="sec-title-admin">🔍 Detail Item</div>',
                        unsafe_allow_html=True)
            sel_d = st.selectbox("Pilih order:", all_ids, index=len(all_ids)-1, key="det2")
            p_det = next((p for p in pesanan if str(p.get("id")) == sel_d), None)
            if p_det:
                d1, d2 = st.columns(2)
                with d1:
                    st.write(f"**Pemesan:** {p_det.get('nama','-')} | **WA:** {p_det.get('wa','-')}")
                    st.write(f"**Alamat:** {p_det.get('alamat','-')}")
                with d2:
                    pay_v = p_det.get("pembayaran", "")
                    badge = "pay-tunai-badge" if "Non" not in pay_v else "pay-nontunai-badge"
                    st.markdown(f'**Pembayaran:** <span class="{badge}">{pay_v}</span>',
                                unsafe_allow_html=True)
                    st.write(f"**Status:** {p_det.get('status', '-')}")
                if p_det.get("items"):
                    df_det = pd.DataFrame(p_det["items"])
                    if not df_det.empty:
                        for col in ["harga", "subtotal"]:
                            if col in df_det.columns:
                                df_det[col] = df_det[col].apply(
                                    lambda x: fmt_rp(float(x)) if x else "-")
                        st.dataframe(df_det, use_container_width=True, hide_index=True)
                st.markdown(f"**Total: {fmt_rp(p_det.get('total', 0))}**")

    # ── TAB LAPORAN ───────────────────────────────────────────────────────────
    elif st.session_state.admin_tab == "📅 Laporan Keuangan":
        st.markdown('<div class="sec-title-admin">📅 Laporan Keuangan</div>',
                    unsafe_allow_html=True)
        if not pesanan:
            st.info("Belum ada data pesanan.")
        else:
            periode = st.radio("Periode:", ["Harian", "Bulanan", "Tahunan"], horizontal=True)
            df_raw  = pd.DataFrame(pesanan)
            df_raw["tanggal"] = pd.to_datetime(df_raw["tanggal"], errors="coerce")
            df_raw["total"]   = pd.to_numeric(df_raw["total"],   errors="coerce").fillna(0)
            df_raw["bulan"]   = df_raw["tanggal"].dt.to_period("M").astype(str)
            df_raw["tahun"]   = df_raw["tanggal"].dt.year.astype(str)

            if periode == "Harian":
                pilih = st.date_input("Tanggal:", value=date.today())
                df_f  = df_raw[df_raw["tanggal"].dt.date == pilih]; label = str(pilih)
            elif periode == "Bulanan":
                bl = sorted(df_raw["bulan"].dropna().unique(), reverse=True)
                pilih = st.selectbox("Bulan:", bl) if bl else None
                df_f  = df_raw[df_raw["bulan"] == pilih] if pilih else df_raw.iloc[0:0]
                label = str(pilih)
            else:
                tl = sorted(df_raw["tahun"].dropna().unique(), reverse=True)
                pilih = st.selectbox("Tahun:", tl) if tl else None
                df_f  = df_raw[df_raw["tahun"] == pilih] if pilih else df_raw.iloc[0:0]
                label = str(pilih)

            if df_f.empty:
                st.warning("Tidak ada data untuk periode ini.")
            else:
                tp  = df_f["total"].sum()
                jp  = len(df_f)
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Pesanan", jp)
                k2.metric("Total Pemasukan", fmt_rp(tp))
                k3.metric("Rata-rata", fmt_rp(tp / jp))
                if "pembayaran" in df_f.columns:
                    tn = df_f["pembayaran"].str.contains("Non", na=False)
                    k4.metric("Tunai / Non-Tunai",
                               f"{(~tn).sum()} / {tn.sum()}")

                show_cols = [c for c in ["id","tanggal","waktu","nama","alamat",
                                          "total","pembayaran","status"] if c in df_f.columns]
                df_s = df_f[show_cols].copy()
                if "total" in df_s.columns:
                    df_s["total"] = df_s["total"].apply(lambda x: fmt_rp(float(x)) if x else "-")
                if "tanggal" in df_s.columns:
                    df_s["tanggal"] = pd.to_datetime(df_s["tanggal"]).dt.strftime("%d-%m-%Y")
                st.dataframe(df_s, use_container_width=True, hide_index=True)
                st.markdown(
                    f'<div style="text-align:right;font-size:1.1rem;font-weight:900;'
                    f'color:#1e3a5f;">Total ({label}): {fmt_rp(tp)}</div>',
                    unsafe_allow_html=True)

                if periode == "Bulanan":
                    chart = df_f.groupby(df_f["tanggal"].dt.day)["total"].sum()
                    chart.index.name = "Tanggal"; st.bar_chart(chart)
                elif periode == "Tahunan":
                    chart = df_f.groupby("bulan")["total"].sum()
                    st.bar_chart(chart)

                # Export Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    ring = pd.DataFrame({
                        "Keterangan": ["Toko","Periode","Jumlah Pesanan",
                                       "Total Pemasukan","Rata-rata/Pesanan"],
                        "Nilai": ["Toko Buah ABS", label, jp,
                                  fmt_rp(tp), fmt_rp(tp/jp)]
                    })
                    ring.to_excel(writer, sheet_name="Ringkasan", index=False)

                    det = df_f[show_cols].copy()
                    if "tanggal" in det.columns:
                        det["tanggal"] = det["tanggal"].dt.strftime("%d-%m-%Y")
                    det.to_excel(writer, sheet_name="Detail Pesanan", index=False)

                    all_items = []
                    for _, row in df_f.iterrows():
                        for it in (row.get("items", []) or []):
                            all_items.append({
                                "No Order": row.get("id"),
                                "Tanggal":  row["tanggal"].strftime("%d-%m-%Y")
                                            if hasattr(row["tanggal"], "strftime")
                                            else str(row["tanggal"]),
                                "Produk":   it.get("nama", ""),
                                "Qty":      it.get("qty", 0),
                                "Harga":    it.get("harga", 0),
                                "Subtotal": it.get("subtotal", 0),
                            })
                    if all_items:
                        pd.DataFrame(all_items).to_excel(
                            writer, sheet_name="Detail Item", index=False)

                st.download_button(
                    label="📊 Download Laporan Excel",
                    data=output.getvalue(),
                    file_name=f"laporan_abs_{label}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary", use_container_width=True,
                )

    # ── TAB SARAN ─────────────────────────────────────────────────────────────
    elif st.session_state.admin_tab == "💬 Saran":
        st.markdown('<div class="sec-title-admin">💬 Kritik & Saran Pelanggan</div>',
                    unsafe_allow_html=True)
        if not saran_list:
            st.info("Belum ada saran masuk.")
        else:
            for s in reversed(saran_list):
                st.markdown(f"""
<div style="background:white;border-radius:12px;padding:1rem 1.2rem;margin-bottom:10px;
  border-left:4px solid #2d5f9e;box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <b style="color:#1e3a5f;">{s.get('nama','-')}</b>
  <span style="float:right;font-size:.75rem;color:#888;">{s.get('tanggal','-')}</span><br>
  <p style="margin:.5rem 0 0;color:#333;">{s.get('pesan','-')}</p>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    inject_css()

    # Jika di halaman admin
    if st.session_state.halaman == "Admin":
        if not st.session_state.admin_login:
            pg_admin_login()
        else:
            pg_admin_dashboard()
        return

    # Navbar publik
    n = jml_item()
    menu_map = {
        "Beranda":   "🏠 Beranda",
        "Pesan":     "🛒 Pesan",
        "Keranjang": f"🛍️ Keranjang ({n})" if n else "🛍️ Keranjang",
        "Kontak":    "📞 Kontak",
    }
    cols = st.columns(len(menu_map))
    for i, (key, label) in enumerate(menu_map.items()):
        with cols[i]:
            aktif = st.session_state.halaman == key
            if st.button(label, key=f"nav_{key}",
                         type="primary" if aktif else "secondary",
                         use_container_width=True):
                st.session_state.halaman = key; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    hal = st.session_state.halaman
    if   hal == "Beranda":   pg_beranda()
    elif hal == "Pesan":     pg_pesan()
    elif hal == "Keranjang": pg_keranjang()
    elif hal == "Kontak":    pg_kontak()

    # Tombol admin tersembunyi di bagian bawah halaman
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    col_admin = st.columns([6, 1])
    with col_admin[1]:
        if st.button("🔐 Admin", key="goto_admin", help="Akses dashboard admin"):
            st.session_state.halaman = "Admin"; st.rerun()


if __name__ == "__main__":
    main()
