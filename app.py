import streamlit as st

st.set_page_config(page_title="Toko Buah ABS", layout="wide")

# ===== HEADER =====
st.markdown("""
    <h1 style='text-align: center; color: green;'>🍎 TOKO BUAH ABS</h1>
    <h4 style='text-align: center;'>Menjual aneka buah lokal dan impor</h4>
""", unsafe_allow_html=True)

# ===== INFO TOKO =====
with st.container():
    st.info("""
📍 Jl. Mandala Raya, RT.02/RW.02, Ciparigi, Kec. Bogor Utara, Kota Bogor, Jawa Barat 16157  
📞 087875957722  
🕒 08.00–21.30 (Setiap hari)
""")

# ===== DATA PRODUK =====
buah = [
    {"nama": "Jeruk", "harga": 12000},
    {"nama": "Jeruk Kecil", "harga": 8000},
    {"nama": "Mangga", "harga": 15000},
    {"nama": "Buah Naga", "harga": 18000},
    {"nama": "Pisang", "harga": 10000},
    {"nama": "Belimbing", "harga": 12000},
    {"nama": "Salak", "harga": 14000},
    {"nama": "Apel Hijau", "harga": 20000},
    {"nama": "Apel Merah", "harga": 22000},
    {"nama": "Melon", "harga": 25000},
    {"nama": "Nanas", "harga": 13000},
]

parcel = [
    {"nama": "Parcel Hemat", "harga": 50000},
    {"nama": "Parcel Premium", "harga": 100000},
    {"nama": "Parcel Spesial", "harga": 150000},
]

# ===== SESSION STATE =====
if "cart" not in st.session_state:
    st.session_state.cart = []

# ===== MENU BUAH =====
st.header("🍊 Daftar Buah")

cols = st.columns(3)

for i, item in enumerate(buah):
    with cols[i % 3]:
        st.subheader(item["nama"])
        st.write(f"Rp {item['harga']}")

        if st.button(f"Tambah {item['nama']}", key=item["nama"]):
            st.session_state.cart.append(item)

# ===== PARCEL =====
st.header("🎁 Paket Parcel Buah")

cols = st.columns(3)

for i, item in enumerate(parcel):
    with cols[i % 3]:
        st.subheader(item["nama"])
        st.write(f"Rp {item['harga']}")

        if st.button(f"Tambah {item['nama']}", key="parcel"+item["nama"]):
            st.session_state.cart.append(item)

# ===== CART =====
st.header("🛒 Keranjang Belanja")

total = 0

if st.session_state.cart:
    for item in st.session_state.cart:
        st.write(f"- {item['nama']} (Rp {item['harga']})")
        total += item["harga"]

    st.subheader(f"Total: Rp {total}")

    if st.button("Hapus Semua"):
        st.session_state.cart = []

else:
    st.write("Keranjang kosong")

# ===== FORM PEMBELI =====
st.header("📦 Data Pemesan")

nama = st.text_input("Nama")
alamat = st.text_area("Alamat Pengiriman")

# ===== PESAN WA =====
if st.button("Pesan via WhatsApp"):
    if st.session_state.cart and nama and alamat:
        pesan = "Halo, saya ingin pesan:\n"

        for item in st.session_state.cart:
            pesan += f"- {item['nama']} (Rp {item['harga']})\n"

        pesan += f"\nTotal: Rp {total}"
        pesan += f"\nNama: {nama}"
        pesan += f"\nAlamat: {alamat}"

        nomor = "6287875957722"

        link = f"https://wa.me/{nomor}?text={pesan.replace(' ', '%20').replace('\n','%0A')}"

        st.success("Klik link di bawah untuk kirim pesanan 👇")
        st.markdown(f"[Kirim ke WhatsApp]({link})")

    else:
        st.warning("Lengkapi data dan pilih pesanan!")

# ===== FOOTER =====
st.markdown("---")
st.markdown("© 2026 Toko Buah ABS | Fresh Fruit Delivery 🍎")
