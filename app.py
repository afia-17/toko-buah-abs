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
TOKO_WA      = "6287875957722"
TOKO_NAMA    = "Toko Buah ABS"
TOKO_ALAMAT  = "Jl. Mandala Raya, RT.02/RW.02, Ciparigi, Kec. Bogor Utara, Kota Bogor, Jawa Barat 16157"
TOKO_JAM     = "08.00 - 21.30 (Setiap Hari)"
TOKO_TELP    = "087875957722"
MAPS_URL     = "https://maps.google.com/?q=Jl.+Mandala+Raya+RT.02+RW.02+Ciparigi+Bogor+Utara+Kota+Bogor"
DATA_FILE    = "data_pesanan.json"

PRODUK = [
    {"id":1,  "nama":"Jeruk Siam",        "emoji":"🍊","harga":12000,"satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":2,  "nama":"Jeruk Kecil",       "emoji":"🍋","harga":8000, "satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":3,  "nama":"Mangga Harum Manis","emoji":"🥭","harga":18000,"satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":4,  "nama":"Buah Naga",         "emoji":"🐉","harga":15000,"satuan":"per buah", "kategori":"Lokal","stok":True},
    {"id":5,  "nama":"Pisang Cavendish",  "emoji":"🍌","harga":5000, "satuan":"per sisir","kategori":"Lokal","stok":True},
    {"id":6,  "nama":"Belimbing",         "emoji":"⭐","harga":7000, "satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":7,  "nama":"Salak Pondoh",      "emoji":"🌰","harga":10000,"satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":8,  "nama":"Melon",             "emoji":"🍈","harga":9000, "satuan":"per kg",   "kategori":"Lokal","stok":True},
    {"id":9,  "nama":"Nanas",             "emoji":"🍍","harga":8000, "satuan":"per buah", "kategori":"Lokal","stok":True},
    {"id":10, "nama":"Apel Hijau",        "emoji":"🍏","harga":22000,"satuan":"per kg",   "kategori":"Impor","stok":True},
    {"id":11, "nama":"Apel Merah",        "emoji":"🍎","harga":20000,"satuan":"per kg",   "kategori":"Impor","stok":True},
    {"id":12, "nama":"Anggur",            "emoji":"🍇","harga":35000,"satuan":"per kg",   "kategori":"Impor","stok":True},
    {"id":13, "nama":"Kelengkeng",        "emoji":"🫐","harga":28000,"satuan":"per kg",   "kategori":"Impor","stok":True},
    {
        "id":14,"nama":"Parcel Buah Kecil","emoji":"🎁","harga":75000,"satuan":"per paket",
        "kategori":"Parcel","stok":True,
        "isi":"Pisang Cavendish, Jeruk Siam, Apel Merah, Belimbing (sekitar 4 jenis buah pilihan)"
    },
    {
        "id":15,"nama":"Parcel Buah Sedang","emoji":"🎁","harga":125000,"satuan":"per paket",
        "kategori":"Parcel","stok":True,
        "isi":"Mangga, Anggur, Apel Hijau, Pisang, Jeruk Siam, Melon (sekitar 6 jenis buah pilihan)"
    },
    {
        "id":16,"nama":"Parcel Buah Besar","emoji":"🎁","harga":200000,"satuan":"per paket",
        "kategori":"Parcel","stok":True,
        "isi":"Mangga, Anggur, Kelengkeng, Apel Merah & Hijau, Buah Naga, Melon, Nanas, Jeruk (sekitar 9-10 jenis buah premium)"
    },
]

# ── Data helpers ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return {"pesanan":[],"pengunjung":0,"saran":[]}

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tambah_pesanan(nama, wa, alamat, items, total):
    data = load_data()
    new = {
        "id":     len(data["pesanan"]) + 1,
        "tanggal":datetime.now().strftime("%Y-%m-%d"),
        "waktu":  datetime.now().strftime("%H:%M"),
        "nama":   nama, "wa": wa, "alamat": alamat,
        "items":  items, "total": total,
    }
    data["pesanan"].append(new)
    save_data(data)
    return new["id"]

def catat_pengunjung():
    data = load_data()
    data["pengunjung"] = data.get("pengunjung",0) + 1
    save_data(data)

# ── Session init ───────────────────────────────────────────────────────────────
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}
if "halaman" not in st.session_state:
    st.session_state.halaman = "Beranda"
if "filter_kat" not in st.session_state:
    st.session_state.filter_kat = "Semua"
if "pengunjung_dicatat" not in st.session_state:
    catat_pengunjung()
    st.session_state.pengunjung_dicatat = True

# ── Helpers ────────────────────────────────────────────────────────────────────
def fmt_rp(n):   return "Rp {:,.0f}".format(n).replace(",",".")
def total_krj(): return sum(v["harga"]*v["qty"] for v in st.session_state.keranjang.values())
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

.sec-title{font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:800;
  color:#1a4a05;border-left:5px solid #4caf1e;padding-left:12px;margin-bottom:1rem;}

.pcard{background:white;border-radius:18px;padding:1.1rem;text-align:center;
  box-shadow:0 2px 14px rgba(0,0,0,.07);border:1.5px solid #e0f2d0;
  transition:transform .15s,box-shadow .15s;height:100%;}
.pcard:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(76,175,30,.18);border-color:#5aba2a;}
.pemoji{font-size:3rem;display:block;margin-bottom:.3rem;}
.pname{font-size:.93rem;font-weight:800;color:#1a4a05;margin-bottom:3px;}
.psatuan{font-size:.73rem;color:#5aaa25;margin-bottom:6px;}
.pprice{font-size:1rem;font-weight:800;color:#2d6a0a;background:#edfadd;
  padding:3px 14px;border-radius:20px;display:inline-block;margin-bottom:8px;}
.pisi{font-size:.7rem;color:#557a3a;background:#f5fdf0;border-radius:8px;
  padding:5px 8px;margin:4px 0 8px;line-height:1.5;text-align:left;}
.bl{font-size:.68rem;padding:2px 10px;border-radius:20px;font-weight:700;display:inline-block;margin-bottom:6px;}
.bl-lokal{background:#d4edda;color:#155724;}
.bl-impor{background:#cce5ff;color:#004085;}
.bl-parcel{background:#fff3cd;color:#856404;}

.osec{background:white;border-radius:16px;padding:1.4rem;
  box-shadow:0 2px 12px rgba(0,0,0,.07);border:1.5px solid #e0f2d0;}
.total-box{text-align:right;font-size:1.15rem;font-weight:900;color:#2d6a0a;padding:8px 0;}
.wa-link{display:block;width:100%;background:#25D366;color:white!important;
  text-align:center;padding:14px;border-radius:12px;font-weight:800;font-size:1rem;
  text-decoration:none;margin-top:10px;box-shadow:0 4px 14px rgba(37,211,102,.35);}
.wa-link:hover{background:#1da851;}
.maps-link{display:inline-block;background:#4285F4;color:white!important;
  padding:9px 20px;border-radius:10px;font-weight:700;font-size:.85rem;
  text-decoration:none;box-shadow:0 3px 10px rgba(66,133,244,.3);}
.info-yellow{background:#fffbeb;border:1.5px solid #fcd34d;border-radius:12px;
  padding:.9rem 1.1rem;font-size:.85rem;color:#78350f;margin-bottom:1rem;}
</style>""", unsafe_allow_html=True)

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
  </div>
  <div class="hero-info">
    <span>📍 Ciparigi, Bogor Utara</span>
    <span>📞 {TOKO_TELP}</span>
    <span>🕐 {TOKO_JAM}</span>
  </div>
</div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if st.button("🛒 Pesan Sekarang", use_container_width=True, type="primary"):
            st.session_state.halaman="Pesan"; st.rerun()
    with c2:
        if st.button(f"🛍️ Keranjang ({jml_item()})", use_container_width=True):
            st.session_state.halaman="Keranjang"; st.rerun()
    with c3:
        st.link_button("📍 Google Maps", MAPS_URL, use_container_width=True)
    with c4:
        if st.button("📞 Kontak & Saran", use_container_width=True):
            st.session_state.halaman="Kontak"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1,1])
    with col_a:
        st.markdown('<div class="sec-title">📋 Informasi Toko</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="osec">
  <p>📍 <b>Alamat</b><br><small>{TOKO_ALAMAT}</small></p><br>
  <p>📞 <b>Telepon / WA:</b> {TOKO_TELP}</p>
  <p>🕐 <b>Jam Buka:</b> {TOKO_JAM}</p>
  <p>🌿 <b>Produk:</b> Buah Lokal, Buah Impor &amp; Parcel Buah</p><br>
  <a class="maps-link" href="{MAPS_URL}" target="_blank">🗺️ Buka Google Maps</a>
</div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="sec-title">⭐ Produk Unggulan</div>', unsafe_allow_html=True)
        unggulan = [p for p in PRODUK if p["kategori"] != "Parcel"][:4]
        r1,r2 = st.columns(2)
        for i,p in enumerate(unggulan):
            col = r1 if i%2==0 else r2
            with col:
                st.markdown(f"""
<div class="pcard" style="margin-bottom:10px;">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">🎁 Parcel Buah Spesial</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-yellow">
  🎁 Parcel buah tersedia untuk berbagai keperluan: lebaran, ulang tahun, pernikahan, arisan,
  dan ucapan selamat. Setiap parcel dikemas cantik dengan buah-buah segar pilihan.
  Hubungi kami untuk pemesanan massal!
</div>""", unsafe_allow_html=True)

    parcels = [p for p in PRODUK if p["kategori"]=="Parcel"]
    pc = st.columns(len(parcels))
    for i,p in enumerate(parcels):
        with pc[i]:
            st.markdown(f"""
<div class="pcard">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <span class="bl bl-parcel">Parcel</span><br>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']}</div>
  <div class="pisi">🍃 Isi: {p.get('isi','')}</div>
</div>""", unsafe_allow_html=True)


def pg_pesan():
    st.markdown('<div class="sec-title">🛒 Katalog Buah Segar</div>', unsafe_allow_html=True)
    cats = ["Semua","Lokal","Impor","Parcel"]
    cols_t = st.columns(len(cats))
    for i,c in enumerate(cats):
        with cols_t[i]:
            aktif = st.session_state.filter_kat == c
            if st.button(c, key=f"t_{c}", type="primary" if aktif else "secondary", use_container_width=True):
                st.session_state.filter_kat = c; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    tampil = PRODUK if st.session_state.filter_kat=="Semua" else [p for p in PRODUK if p["kategori"]==st.session_state.filter_kat]

    for r in range(0, len(tampil), 3):
        row = tampil[r:r+3]
        cols = st.columns(3)
        for i,p in enumerate(row):
            with cols[i]:
                badge_cls = "bl-lokal" if p["kategori"]=="Lokal" else "bl-impor" if p["kategori"]=="Impor" else "bl-parcel"
                isi_html = f'<div class="pisi">🍃 {p["isi"]}</div>' if "isi" in p else ""
                stok_txt = "Tersedia" if p["stok"] else "Habis"
                st.markdown(f"""
<div class="pcard">
  <span class="pemoji">{p['emoji']}</span>
  <div class="pname">{p['nama']}</div>
  <span class="bl {badge_cls}">{p['kategori']}</span><br>
  <div class="pprice">{fmt_rp(p['harga'])}</div>
  <div class="psatuan">{p['satuan']} &middot; {stok_txt}</div>
  {isi_html}
</div>""", unsafe_allow_html=True)
                if p["stok"]:
                    qty = st.number_input("Jumlah", min_value=1, max_value=50, value=1,
                                          key=f"qty_{p['id']}", label_visibility="collapsed")
                    if st.button("+ Keranjang", key=f"add_{p['id']}", use_container_width=True):
                        tambah_krj(p, qty)
                        st.success(f"Ditambahkan: {p['nama']}")
                else:
                    st.button("Stok Habis", key=f"add_{p['id']}", disabled=True, use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)

    if jml_item() > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🛍️ Keranjang ({jml_item()} item) - {fmt_rp(total_krj())}",
                     type="primary", use_container_width=True):
            st.session_state.halaman="Keranjang"; st.rerun()


def pg_keranjang():
    st.markdown('<div class="sec-title">🛍️ Keranjang Belanja</div>', unsafe_allow_html=True)
    if not st.session_state.keranjang:
        st.info("Keranjang masih kosong. Yuk pilih buah segar dulu!")
        if st.button("🍎 Lihat Katalog", type="primary"):
            st.session_state.halaman="Pesan"; st.rerun()
        return

    for pid, item in list(st.session_state.keranjang.items()):
        c1,c2,c3,c4 = st.columns([3,2,2,1])
        with c1:
            st.markdown(f"""
<div style="padding:6px 0;">
  <span style="font-size:1.4rem;">{item['emoji']}</span>
  <b style="color:#1a4a05;"> {item['nama']}</b><br>
  <small style="color:#5aaa25;">{item['satuan']}</small>
</div>""", unsafe_allow_html=True)
        with c2:
            nq = st.number_input("Qty", min_value=1, max_value=50, value=item["qty"],
                                  key=f"kq_{pid}", label_visibility="collapsed")
            st.session_state.keranjang[pid]["qty"] = nq
        with c3:
            st.markdown(f'<div style="padding:10px 0;font-weight:800;color:#2d6a0a;">{fmt_rp(item["harga"]*nq)}</div>',
                        unsafe_allow_html=True)
        with c4:
            if st.button("x", key=f"del_{pid}"):
                hapus_krj(pid); st.rerun()

    st.divider()
    st.markdown(f'<div class="total-box">Total: {fmt_rp(total_krj())}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title" style="margin-top:1.4rem;">📝 Data Pemesanan</div>', unsafe_allow_html=True)
    nama    = st.text_input("Nama Lengkap Pemesan", placeholder="Contoh: Budi Santoso")
    wa      = st.text_input("Nomor WhatsApp", placeholder="Contoh: 08123456789")
    alamat  = st.text_area("Alamat Pengiriman", placeholder="Tulis alamat lengkap...")
    catatan = st.text_area("Catatan Tambahan (opsional)", placeholder="Misal: minta buah yang matang, dll.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Konfirmasi & Pesan via WhatsApp", type="primary", use_container_width=True):
        if not nama or not wa or not alamat:
            st.error("Mohon isi nama, nomor WA, dan alamat terlebih dahulu!")
        else:
            items_list = [
                {"nama":v["nama"],"qty":v["qty"],"harga":v["harga"],"subtotal":v["qty"]*v["harga"]}
                for v in st.session_state.keranjang.values()
            ]
            oid = tambah_pesanan(nama, wa, alamat, items_list, total_krj())
            detail = "\n".join(
                f"- {it['nama']} {it['qty']}x @ {fmt_rp(it['harga'])} = {fmt_rp(it['subtotal'])}"
                for it in items_list
            )
            if catatan: detail += f"\n\nCatatan: {catatan}"
            pesan = urllib.parse.quote(
                f"PESANAN TOKO BUAH ABS\nNo. Order: #{oid}\n\n"
                f"Nama: {nama}\nAlamat: {alamat}\n\n"
                f"Detail Pesanan:\n{detail}\n\n"
                f"TOTAL: {fmt_rp(total_krj())}\n\n"
                f"Mohon konfirmasi ketersediaan dan estimasi pengiriman. Terima kasih!"
            )
            wa_url = f"https://wa.me/{TOKO_WA}?text={pesan}"
            st.success(f"Pesanan #{oid} berhasil dicatat!")
            st.markdown(f'<a class="wa-link" href="{wa_url}" target="_blank">💬 Kirim Pesanan via WhatsApp</a>',
                        unsafe_allow_html=True)
            st.session_state.keranjang = {}


def pg_kontak():
    st.markdown('<div class="sec-title">📞 Hubungi Kami</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="osec">
  <h3 style="color:#1a4a05;">🍎 {TOKO_NAMA}</h3>
  <p>📍 <b>Alamat:</b><br>{TOKO_ALAMAT}</p><br>
  <p>📞 <b>Telepon / WhatsApp:</b> {TOKO_TELP}</p>
  <p>🕐 <b>Jam Operasional:</b> {TOKO_JAM}</p><br>
  <a class="wa-link" href="https://wa.me/{TOKO_WA}" target="_blank">💬 Chat via WhatsApp</a>
  <br><br>
  <a class="maps-link" href="{MAPS_URL}" target="_blank">🗺️ Lihat di Google Maps</a>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Kritik & Saran</div>', unsafe_allow_html=True)
    with st.form("saran_form"):
        nama_s  = st.text_input("Nama (opsional)")
        pesan_s = st.text_area("Pesan / Saran / Kritik")
        sub = st.form_submit_button("Kirim", type="primary", use_container_width=True)
        if sub:
            if pesan_s:
                data = load_data()
                if "saran" not in data: data["saran"] = []
                data["saran"].append({
                    "nama": nama_s or "Anonim",
                    "pesan": pesan_s,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                save_data(data)
                st.success("Terima kasih atas masukan Anda!")
            else:
                st.warning("Tulis pesannya dulu ya!")


# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    n = jml_item()
    menu_map = {
        "Beranda":"🏠 Beranda",
        "Pesan":"🛒 Pesan",
        "Keranjang":f"🛍️ Keranjang ({n})" if n else "🛍️ Keranjang",
        "Kontak":"📞 Kontak",
    }
    cols = st.columns(len(menu_map))
    for i,(key,label) in enumerate(menu_map.items()):
        with cols[i]:
            aktif = st.session_state.halaman == key
            if st.button(label, key=f"nav_{key}", type="primary" if aktif else "secondary", use_container_width=True):
                st.session_state.halaman = key; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    hal = st.session_state.halaman
    if   hal == "Beranda":   pg_beranda()
    elif hal == "Pesan":     pg_pesan()
    elif hal == "Keranjang": pg_keranjang()
    elif hal == "Kontak":    pg_kontak()

if __name__ == "__main__":
    main()
