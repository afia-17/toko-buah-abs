import streamlit as st
import pandas as pd
import json, os, io
from datetime import datetime, date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admin - Toko Buah ABS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Config ─────────────────────────────────────────────────────────────────────
ADMIN_PASSWORD = "absadmin2024"   # Ganti sesuai kebutuhan
DATA_FILE      = "https://tokobuahabsapp.streamlit.app/"  # File yang sama dengan website toko

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');
html,[class*="css"]{font-family:'Nunito',sans-serif!important;}
.stApp{background:#f0f4f8;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}

.admin-header{background:linear-gradient(135deg,#1e3a5f 0%,#2d5f9e 60%,#4a90d9 100%);
  border-radius:18px;padding:2rem 2rem 1.5rem;margin-bottom:1.5rem;color:white;text-align:center;
  box-shadow:0 8px 30px rgba(30,58,95,.35);}
.admin-header h1{font-family:'Poppins',sans-serif!important;font-size:2rem!important;
  font-weight:800!important;margin:0!important;color:white!important;}
.admin-header p{opacity:.85;margin:.4rem 0 0;font-size:.9rem;}

.scard{background:white;border-radius:16px;padding:1.3rem 1rem;text-align:center;
  box-shadow:0 2px 12px rgba(0,0,0,.08);}
.sval{font-size:2rem;font-weight:900;}
.slbl{font-size:.78rem;font-weight:700;margin-top:4px;color:#666;}

.sec-title{font-family:'Poppins',sans-serif;font-size:1.1rem;font-weight:800;
  color:#1e3a5f;border-left:5px solid #2d5f9e;padding-left:12px;margin:1.2rem 0 .8rem;}

.login-box{max-width:380px;margin:4rem auto;background:white;border-radius:20px;
  padding:2.5rem;box-shadow:0 8px 30px rgba(0,0,0,.12);}
</style>""", unsafe_allow_html=True)

# ── Data helpers ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return {"pesanan":[],"pengunjung":0,"saran":[]}

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fmt_rp(n): return "Rp {:,.0f}".format(n).replace(",",".")

# ── Login ──────────────────────────────────────────────────────────────────────
if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if not st.session_state.admin_login:
    st.markdown("""
<div class="login-box">
  <h2 style="text-align:center;color:#1e3a5f;margin-bottom:1.5rem;">🔐 Admin Login<br><small style="font-size:.75rem;color:#888;">Toko Buah ABS</small></h2>
</div>""", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔐 Login Admin - Toko Buah ABS")
        pwd = st.text_input("Password", type="password", placeholder="Masukkan password admin")
        if st.button("Login", type="primary", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_login = True
                st.rerun()
            else:
                st.error("Password salah!")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD (hanya muncul setelah login)
# ═════════════════════════════════════════════════════════════════════════════

data = load_data()
pesanan = data.get("pesanan", [])
pengunjung = data.get("pengunjung", 0)
saran = data.get("saran", [])

# Header
st.markdown("""
<div class="admin-header">
  <h1>📊 Dashboard Admin</h1>
  <p>Toko Buah ABS &nbsp;|&nbsp; Panel Manajemen & Laporan Keuangan</p>
</div>""", unsafe_allow_html=True)

# Logout
col_lout = st.columns([6,1])
with col_lout[1]:
    if st.button("🚪 Logout"):
        st.session_state.admin_login = False; st.rerun()

# ── NAVIGASI ADMIN ─────────────────────────────────────────────────────────────
if "admin_tab" not in st.session_state:
    st.session_state.admin_tab = "Statistik"

tabs = ["📊 Statistik", "📦 Pesanan", "📅 Laporan Keuangan", "💬 Kritik & Saran"]
tcols = st.columns(len(tabs))
for i, t in enumerate(tabs):
    with tcols[i]:
        aktif = st.session_state.admin_tab == t
        if st.button(t, key=f"at_{i}", type="primary" if aktif else "secondary", use_container_width=True):
            st.session_state.admin_tab = t; st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB: STATISTIK
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.admin_tab == "📊 Statistik":
    total_pesanan   = len(pesanan)
    total_pemasukan = sum(p["total"] for p in pesanan)
    rata_order      = total_pemasukan / total_pesanan if total_pesanan else 0

    # Hari ini
    hari_ini  = date.today().strftime("%Y-%m-%d")
    p_hari    = [p for p in pesanan if p["tanggal"] == hari_ini]
    omset_hari = sum(p["total"] for p in p_hari)

    # Bulan ini
    bulan_ini = date.today().strftime("%Y-%m")
    p_bulan   = [p for p in pesanan if p["tanggal"].startswith(bulan_ini)]
    omset_bulan = sum(p["total"] for p in p_bulan)

    # Stat cards row 1
    s1,s2,s3,s4 = st.columns(4)
    cards = [
        (s1, "👥", str(pengunjung),     "Total Pengunjung",      "#2d5f9e"),
        (s2, "🛒", str(total_pesanan),  "Total Semua Pesanan",   "#16a34a"),
        (s3, "💰", fmt_rp(total_pemasukan), "Total Pemasukan",   "#b45309"),
        (s4, "📦", fmt_rp(rata_order),  "Rata-rata per Pesanan", "#7c3aed"),
    ]
    for col, em, val, lbl, clr in cards:
        with col:
            st.markdown(f"""
<div class="scard" style="border-top:4px solid {clr};">
  <div style="font-size:1.8rem;">{em}</div>
  <div class="sval" style="color:{clr};font-size:1.3rem;">{val}</div>
  <div class="slbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stat cards row 2 (hari ini & bulan ini)
    s5,s6,_ = st.columns([1,1,2])
    with s5:
        st.markdown(f"""
<div class="scard" style="border-top:4px solid #0891b2;">
  <div style="font-size:1.8rem;">📅</div>
  <div class="sval" style="color:#0891b2;font-size:1.3rem;">{len(p_hari)} pesanan</div>
  <div class="slbl">Hari Ini · {fmt_rp(omset_hari)}</div>
</div>""", unsafe_allow_html=True)
    with s6:
        st.markdown(f"""
<div class="scard" style="border-top:4px solid #dc2626;">
  <div style="font-size:1.8rem;">🗓️</div>
  <div class="sval" style="color:#dc2626;font-size:1.3rem;">{len(p_bulan)} pesanan</div>
  <div class="slbl">Bulan Ini · {fmt_rp(omset_bulan)}</div>
</div>""", unsafe_allow_html=True)

    # Grafik produk terlaris
    if pesanan:
        st.markdown('<div class="sec-title">🏆 Produk Terlaris</div>', unsafe_allow_html=True)
        all_items = []
        for p in pesanan:
            for it in p.get("items", []):
                all_items.append({"nama": it["nama"], "qty": it["qty"], "subtotal": it["subtotal"]})
        df_items = pd.DataFrame(all_items)
        if not df_items.empty:
            terlaris = df_items.groupby("nama")["qty"].sum().sort_values(ascending=False).head(8)
            st.bar_chart(terlaris)

    # Tren harian (7 hari terakhir)
    if pesanan:
        st.markdown('<div class="sec-title">📈 Tren Pemasukan 7 Hari Terakhir</div>', unsafe_allow_html=True)
        df_all = pd.DataFrame(pesanan)
        df_all["tanggal"] = pd.to_datetime(df_all["tanggal"])
        tren = df_all.groupby("tanggal")["total"].sum().tail(7)
        st.line_chart(tren)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: PESANAN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.admin_tab == "📦 Pesanan":
    st.markdown('<div class="sec-title">📦 Daftar Semua Pesanan</div>', unsafe_allow_html=True)

    if not pesanan:
        st.info("Belum ada pesanan masuk.")
    else:
        # Filter
        col_f1, col_f2 = st.columns([2,2])
        with col_f1:
            cari = st.text_input("Cari nama / nomor order", placeholder="Ketik nama pemesan...")
        with col_f2:
            tgl_filter = st.date_input("Filter tanggal (kosongkan untuk semua)", value=None)

        df = pd.DataFrame(pesanan)
        df["tanggal"] = pd.to_datetime(df["tanggal"])

        if cari:
            df = df[df["nama"].str.contains(cari, case=False, na=False)]
        if tgl_filter:
            df = df[df["tanggal"].dt.date == tgl_filter]

        df_tampil = df[["id","tanggal","waktu","nama","wa","alamat","total"]].copy()
        df_tampil.columns = ["No Order","Tanggal","Waktu","Nama","WA","Alamat","Total (Rp)"]
        df_tampil["Tanggal"] = df_tampil["Tanggal"].dt.strftime("%d-%m-%Y")
        df_tampil["Total (Rp)"] = df_tampil["Total (Rp)"].apply(fmt_rp)
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)

        # Detail pesanan
        st.markdown('<div class="sec-title">Detail Item per Pesanan</div>', unsafe_allow_html=True)
        pilih_id = st.selectbox("Pilih No. Order untuk lihat detail item:",
                                 [p["id"] for p in pesanan], index=len(pesanan)-1)
        pesanan_detail = next((p for p in pesanan if p["id"]==pilih_id), None)
        if pesanan_detail:
            st.write(f"**Pemesan:** {pesanan_detail['nama']} | **WA:** {pesanan_detail['wa']}")
            st.write(f"**Alamat:** {pesanan_detail['alamat']}")
            df_det = pd.DataFrame(pesanan_detail["items"])
            df_det.columns = ["Produk","Qty","Harga Satuan","Subtotal"]
            df_det["Harga Satuan"] = df_det["Harga Satuan"].apply(fmt_rp)
            df_det["Subtotal"]     = df_det["Subtotal"].apply(fmt_rp)
            st.dataframe(df_det, use_container_width=True, hide_index=True)
            st.markdown(f"**Total: {fmt_rp(pesanan_detail['total'])}**")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: LAPORAN KEUANGAN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.admin_tab == "📅 Laporan Keuangan":
    st.markdown('<div class="sec-title">📅 Laporan Keuangan</div>', unsafe_allow_html=True)

    if not pesanan:
        st.info("Belum ada data pesanan.")
    else:
        periode = st.radio("Periode laporan:", ["Harian","Bulanan","Tahunan"], horizontal=True)
        df_raw = pd.DataFrame(pesanan)
        df_raw["tanggal"] = pd.to_datetime(df_raw["tanggal"])
        df_raw["bulan"]   = df_raw["tanggal"].dt.to_period("M").astype(str)
        df_raw["tahun"]   = df_raw["tanggal"].dt.year.astype(str)

        if periode == "Harian":
            pilih = st.date_input("Pilih tanggal:", value=date.today())
            df_f  = df_raw[df_raw["tanggal"].dt.date == pilih]
            label = str(pilih)
        elif periode == "Bulanan":
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
        else:
            total_periode = df_f["total"].sum()
            jumlah_order  = len(df_f)

            k1,k2,k3 = st.columns(3)
            with k1:
                st.metric("Jumlah Pesanan", jumlah_order)
            with k2:
                st.metric("Total Pemasukan", fmt_rp(total_periode))
            with k3:
                st.metric("Rata-rata/Pesanan", fmt_rp(total_periode/jumlah_order))

            # Tabel
            df_show = df_f[["id","tanggal","waktu","nama","alamat","total"]].copy()
            df_show.columns = ["No Order","Tanggal","Waktu","Nama","Alamat","Total (Rp)"]
            df_show["Tanggal"] = df_show["Tanggal"].dt.strftime("%d-%m-%Y")
            df_show["Total (Rp)"] = df_show["Total (Rp)"].apply(fmt_rp)
            st.dataframe(df_show, use_container_width=True, hide_index=True)

            # Grafik
            if periode == "Bulanan":
                st.markdown('<div class="sec-title">Grafik Pemasukan Harian</div>', unsafe_allow_html=True)
                chart = df_f.groupby(df_f["tanggal"].dt.day)["total"].sum()
                chart.index.name = "Tanggal"
                st.bar_chart(chart)
            elif periode == "Tahunan":
                st.markdown('<div class="sec-title">Grafik Pemasukan Bulanan</div>', unsafe_allow_html=True)
                chart = df_f.groupby("bulan")["total"].sum()
                st.bar_chart(chart)

            # Export Excel 3 sheet
            st.markdown('<div class="sec-title">📥 Export Laporan ke Excel</div>', unsafe_allow_html=True)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Sheet Ringkasan
                ring = pd.DataFrame({
                    "Keterangan": ["Toko","Periode","Jumlah Pesanan","Total Pemasukan","Rata-rata per Pesanan"],
                    "Nilai": ["Toko Buah ABS", label, jumlah_order, fmt_rp(total_periode), fmt_rp(total_periode/jumlah_order)]
                })
                ring.to_excel(writer, sheet_name="Ringkasan", index=False)

                # Sheet Detail Pesanan
                det = df_f[["id","tanggal","waktu","nama","wa","alamat","total"]].copy()
                det.columns = ["No Order","Tanggal","Waktu","Nama","WA","Alamat","Total (Rp)"]
                det["Tanggal"] = det["Tanggal"].dt.strftime("%d-%m-%Y")
                det.to_excel(writer, sheet_name="Detail Pesanan", index=False)

                # Sheet Detail Item
                all_items = []
                for _, row in df_f.iterrows():
                    for it in row.get("items", []):
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


# ══════════════════════════════════════════════════════════════════════════════
# TAB: KRITIK & SARAN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.admin_tab == "💬 Kritik & Saran":
    st.markdown('<div class="sec-title">💬 Kritik & Saran dari Pelanggan</div>', unsafe_allow_html=True)
    if not saran:
        st.info("Belum ada kritik atau saran masuk.")
    else:
        for s in reversed(saran):
            with st.container():
                st.markdown(f"""
<div style="background:white;border-radius:12px;padding:1rem 1.2rem;margin-bottom:10px;
  border-left:4px solid #2d5f9e;box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <b style="color:#1e3a5f;">{s['nama']}</b>
  <span style="float:right;font-size:.75rem;color:#888;">{s['tanggal']}</span><br>
  <p style="margin:.5rem 0 0;color:#333;">{s['pesan']}</p>
</div>""", unsafe_allow_html=True)
