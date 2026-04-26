import streamlit as st

st.set_page_config(page_title="Toko Buah ABS", layout="wide")

st.title("🍎 TOKO BUAH ABS")
st.write("Pesan buah segar dari rumah, langsung kami antar!")

# ===== DATA BUAH =====
buah = [
    {"nama": "Apel", "harga": 10000, "gambar": "https://via.placeholder.com/150"},
    {"nama": "Pisang", "harga": 8000, "gambar": "https://via.placeholder.com/150"},
    {"nama": "Jeruk", "harga": 12000, "gambar": "https://via.placeholder.com/150"},
    {"nama": "Mangga", "harga": 15000, "gambar": "https://via.placeholder.com/150"},
]

st.header("Daftar Buah")

total_harga = 0
pesanan = []

# ===== TAMPILAN MENU =====
cols = st.columns(2)

for i, item in enumerate(buah):
    with cols[i % 2]:
        st.image(item["gambar"], width=150)
        st.subheader(item["nama"])
        st.write(f"Harga: Rp {item['harga']}")

        jumlah = st.number_input(
            f"Jumlah {item['nama']}", min_value=0, step=1, key=i
        )

        if jumlah > 0:
            total = jumlah * item["harga"]
            total_harga += total
            pesanan.append(f"{item['nama']} x{jumlah} = Rp {total}")

# ===== TOTAL =====
st.markdown("---")
st.subheader(f"Total: Rp {total_harga}")

# ===== FORM CUSTOMER =====
nama = st.text_input("Nama Pembeli")
alamat = st.text_area("Alamat Pengiriman")

# ===== TOMBOL PESAN =====
if st.button("Pesan Sekarang"):
    if pesanan and nama and alamat:
        pesan_text = "Halo, saya ingin pesan:\n"
        pesan_text += "\n".join(pesanan)
        pesan_text += f"\n\nTotal: Rp {total_harga}"
        pesan_text += f"\n\nNama: {nama}"
        pesan_text += f"\nAlamat: {alamat}"

        # GANTI nomor ini dengan nomor penjual
        nomor_wa = "6281234567890"

        link = f"https://wa.me/{nomor_wa}?text={pesan_text.replace(' ', '%20').replace('\n', '%0A')}"

        st.success("Pesanan siap dikirim!")
        st.markdown(f"[Klik di sini untuk kirim ke WhatsApp]({link})")

    else:
        st.warning("Lengkapi pesanan dan data terlebih dahulu!")
