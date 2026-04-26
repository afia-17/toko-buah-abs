import streamlit as st

st.set_page_config(page_title="Toko Buah ABS", layout="wide")

st.title("🍎 Toko Buah ABS")
st.subheader("Buah Segar, Harga Terbaik")

# =========================
# DATA PRODUK
# =========================
products = [
    {"id":1,"name":"Jeruk Manis","price":15000,"unit":"kg"},
    {"id":2,"name":"Mangga Harum Manis","price":18000,"unit":"kg"},
    {"id":3,"name":"Pisang Cavendish","price":8000,"unit":"sisir"},
    {"id":4,"name":"Apel Fuji","price":25000,"unit":"kg"},
    {"id":5,"name":"Melon","price":15000,"unit":"kg"},
]

# =========================
# SESSION STATE (KERANJANG)
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 Cari buah")

filtered = [p for p in products if search.lower() in p["name"].lower()]

# =========================
# TAMPILKAN PRODUK
# =========================
cols = st.columns(3)

for i, p in enumerate(filtered):
    with cols[i % 3]:
        st.markdown(f"### {p['name']}")
        st.write(f"Rp {p['price']:,} / {p['unit']}")

        qty = st.number_input(
            "Jumlah",
            min_value=1,
            value=1,
            key=f"qty_{p['id']}"
        )

        if st.button(f"Tambah {p['name']}", key=p["id"]):
            if p["id"] in st.session_state.cart:
                st.session_state.cart[p["id"]]["qty"] += qty
            else:
                st.session_state.cart[p["id"]] = {
                    "name": p["name"],
                    "price": p["price"],
                    "qty": qty
                }
            st.success(f"{p['name']} ditambahkan!")

# =========================
# SIDEBAR KERANJANG
# =========================
st.sidebar.title("🛒 Keranjang")

total = 0

if st.session_state.cart:
    for item in st.session_state.cart.values():
        subtotal = item["price"] * item["qty"]
        total += subtotal
        st.sidebar.write(f"{item['name']} ({item['qty']}) = Rp{subtotal:,}")

    st.sidebar.markdown("---")
    st.sidebar.write(f"**Total: Rp{total:,}**")

    nama = st.sidebar.text_input("Nama")
    wa = st.sidebar.text_input("No WA")
    alamat = st.sidebar.text_area("Alamat")

    if st.sidebar.button("Pesan via WhatsApp"):
        if nama and wa and alamat:
            pesan = f"""
PESANAN TOKO BUAH ABS

Nama: {nama}
No WA: {wa}
Alamat: {alamat}

"""
            for item in st.session_state.cart.values():
                pesan += f"- {item['name']} x{item['qty']}\n"

            pesan += f"\nTOTAL: Rp{total:,}"

            wa_url = f"https://wa.me/6287875957722?text={pesan}"
            st.sidebar.link_button("Klik Kirim WhatsApp", wa_url)
        else:
            st.sidebar.warning("Lengkapi data dulu!")

    if st.sidebar.button("Kosongkan Keranjang"):
        st.session_state.cart = {}
        st.sidebar.success("Keranjang dikosongkan")

else:
    st.sidebar.write("Keranjang kosong")
