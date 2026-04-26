<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Toko Buah ABS – Segar & Berkualitas</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --green:#2D6A1F;--green2:#4A9832;--green3:#C8F5A0;--green-light:#EFF8E8;
  --amber:#D4810A;--amber-light:#FFF4E0;
  --red:#C0392B;--cream:#FDFAF3;--white:#fff;
  --text:#1A2E0D;--text2:#4A5E40;--text3:#7A8F72;
  --r:14px;--rs:8px;
  --shadow:0 2px 12px rgba(45,106,31,0.10);
  --shadow2:0 4px 24px rgba(45,106,31,0.15);
}
body{font-family:'Nunito',sans-serif;background:var(--cream);color:var(--text);min-height:100vh;}

/* HERO */
.hero{
  background:linear-gradient(135deg,#1B4A10 0%,#2D6A1F 45%,#4A9832 100%);
  padding:0 0 0 0; position:relative; overflow:hidden;
}
.hero-top{
  display:flex;align-items:center;justify-content:space-between;
  padding:18px 32px 0; gap:12px;
}
.logo{display:flex;align-items:center;gap:10px;}
.logo-icon{
  width:44px;height:44px;background:rgba(255,255,255,0.15);
  border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;
}
.logo-name{color:#fff;font-size:20px;font-weight:900;letter-spacing:-0.3px;}
.logo-tagline{color:rgba(255,255,255,0.65);font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.hero-nav{display:flex;gap:8px;align-items:center;}
.nav-link{color:rgba(255,255,255,0.8);font-size:13px;font-weight:600;text-decoration:none;padding:6px 12px;border-radius:20px;transition:all 0.2s;}
.nav-link:hover{background:rgba(255,255,255,0.15);color:#fff;}
.cart-fab{
  position:fixed;bottom:24px;right:24px;z-index:100;
  background:var(--green);color:#fff;border:none;border-radius:50px;
  padding:12px 20px;font-size:14px;font-weight:700;cursor:pointer;
  box-shadow:0 4px 20px rgba(45,106,31,0.4);display:flex;align-items:center;gap:8px;
  transition:transform 0.15s,box-shadow 0.15s;
}
.cart-fab:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(45,106,31,0.5);}
.fab-badge{
  background:#E74C3C;color:#fff;font-size:11px;font-weight:800;
  border-radius:10px;padding:2px 7px;min-width:20px;text-align:center;
}

.hero-body{
  display:flex;align-items:flex-end;justify-content:space-between;
  padding:40px 32px 0; gap:24px;
}
.hero-text{flex:1;}
.hero-badge{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
  color:#fff;font-size:11px;font-weight:700;letter-spacing:0.5px;
  padding:5px 12px;border-radius:20px;margin-bottom:14px;
}
.hero-title{
  font-family:'Playfair Display',serif;
  font-size:clamp(28px,5vw,46px);font-weight:900;color:#fff;
  line-height:1.15;margin-bottom:10px;
}
.hero-title span{color:#C8F5A0;}
.hero-sub{color:rgba(255,255,255,0.75);font-size:14px;font-weight:600;margin-bottom:20px;line-height:1.6;}
.hero-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:24px;}
.chip{
  background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);
  color:rgba(255,255,255,0.9);font-size:12px;font-weight:700;
  padding:5px 10px;border-radius:20px;
}
.chip.highlight{background:rgba(200,245,160,0.2);border-color:rgba(200,245,160,0.4);color:#C8F5A0;}

.hero-info{
  display:flex;gap:12px;flex-wrap:wrap;padding-bottom:28px;
}
.info-pill{
  display:flex;align-items:center;gap:7px;
  background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);
  border-radius:10px;padding:8px 14px;
}
.info-pill span:first-child{font-size:16px;}
.info-pill-text{font-size:11px;color:rgba(255,255,255,0.85);font-weight:600;line-height:1.3;}
.info-pill-text b{color:#fff;display:block;font-size:12px;}

.hero-wave{height:40px;background:transparent;}
.hero-wave svg{display:block;width:100%;height:40px;}

/* MAIN */
main{max-width:900px;margin:0 auto;padding:28px 20px 120px;}

/* SEARCH + FILTER */
.search-row{display:flex;gap:10px;margin-bottom:16px;align-items:center;}
.search-wrap{flex:1;position:relative;}
.search-wrap input{
  width:100%;padding:10px 16px 10px 40px;font-size:14px;font-family:'Nunito',sans-serif;
  border:1.5px solid #D4E8C8;border-radius:var(--r);background:#fff;color:var(--text);
  transition:border-color 0.2s;
}
.search-wrap input:focus{outline:none;border-color:var(--green2);}
.search-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:16px;pointer-events:none;}
.filter-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:20px;}
.tab{
  padding:7px 16px;border-radius:20px;font-size:13px;font-weight:700;cursor:pointer;
  border:1.5px solid #D4E8C8;background:#fff;color:var(--text2);
  transition:all 0.15s;white-space:nowrap;
}
.tab.active{background:var(--green);color:#fff;border-color:var(--green);}
.tab:hover:not(.active){background:var(--green-light);border-color:var(--green2);color:var(--green);}

/* SECTION HEADER */
.section-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;}
.section-title{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:var(--text);}
.section-count{
  background:var(--green-light);color:var(--green);
  font-size:12px;font-weight:700;padding:3px 10px;border-radius:20px;
}

/* PRODUCT GRID */
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
  gap:12px;margin-bottom:32px;
}
.card{
  background:#fff;border:1.5px solid #E8F3DF;border-radius:var(--r);
  padding:14px 12px;cursor:default;
  transition:transform 0.15s,box-shadow 0.15s,border-color 0.15s;
  display:flex;flex-direction:column;position:relative;overflow:hidden;
}
.card:hover{transform:translateY(-2px);box-shadow:var(--shadow2);border-color:#B8DDA0;}
.card.out{opacity:0.6;}
.card-tag{
  position:absolute;top:10px;right:10px;
  font-size:10px;font-weight:800;padding:3px 8px;border-radius:10px;letter-spacing:0.3px;
}
.tag-lokal{background:#E8F5E0;color:#2D6A1F;}
.tag-impor{background:#FFF3E0;color:#D4810A;}
.tag-sayur{background:#F3E0FF;color:#7B2FBE;}
.tag-parcel{background:#FFE0E0;color:#C0392B;}

.fruit-emo{font-size:44px;text-align:center;margin:4px 0 10px;display:block;line-height:1;}
.fruit-name{font-size:13px;font-weight:800;color:var(--text);margin-bottom:2px;line-height:1.2;}
.fruit-unit{font-size:11px;color:var(--text3);margin-bottom:6px;}
.fruit-price{font-size:16px;font-weight:900;color:var(--green);margin-bottom:6px;}
.stock-row{display:flex;align-items:center;gap:5px;margin-bottom:10px;}
.dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.dot.ada{background:#4A9832;}
.dot.habis{background:#E74C3C;}
.stock-text{font-size:11px;color:var(--text3);font-weight:600;}

.qty-row{display:flex;align-items:center;gap:5px;margin-top:auto;}
.qbtn{
  width:28px;height:28px;border:1.5px solid #D4E8C8;border-radius:var(--rs);
  background:var(--green-light);font-size:16px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  color:var(--green);font-weight:700;transition:all 0.1s;
  flex-shrink:0;line-height:1;
}
.qbtn:hover:not(:disabled){background:var(--green);color:#fff;border-color:var(--green);}
.qbtn:disabled{opacity:0.3;cursor:default;}
.qval{font-size:14px;font-weight:800;min-width:22px;text-align:center;color:var(--text);}
.abtn{
  flex:1;padding:6px 0;background:var(--green);color:#fff;
  border:none;border-radius:var(--rs);font-size:11px;font-weight:800;
  cursor:pointer;transition:background 0.15s;font-family:'Nunito',sans-serif;
}
.abtn:hover:not(:disabled){background:#1B4A10;}
.abtn:disabled{background:#D4E8C8;color:#7A8F72;cursor:default;}

/* CART MODAL */
.overlay{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:200;
  align-items:flex-end;justify-content:center;
}
.overlay.open{display:flex;}
.cart-sheet{
  background:#fff;border-radius:24px 24px 0 0;width:100%;max-width:520px;
  max-height:85vh;display:flex;flex-direction:column;
  animation:slideUp 0.25s ease;
}
@keyframes slideUp{from{transform:translateY(100%);}to{transform:translateY(0);}}
.sheet-handle{width:40px;height:4px;background:#E0E8D8;border-radius:2px;margin:12px auto 0;}
.sheet-head{padding:16px 20px 12px;border-bottom:1.5px solid #EFF5E8;display:flex;align-items:center;justify-content:space-between;}
.sheet-title{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;}
.close-btn{width:32px;height:32px;border:none;background:#F2F8ED;border-radius:50%;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;color:var(--text2);}
.sheet-body{flex:1;overflow-y:auto;padding:0 20px;}
.cart-item-row{
  display:flex;align-items:center;gap:12px;
  padding:12px 0;border-bottom:1px solid #EFF5E8;
}
.ci-emo{font-size:28px;flex-shrink:0;}
.ci-info{flex:1;}
.ci-name{font-size:13px;font-weight:800;color:var(--text);}
.ci-sub{font-size:11px;color:var(--text3);}
.ci-price{font-size:14px;font-weight:800;color:var(--green);flex-shrink:0;}
.ci-del{background:none;border:none;color:#E74C3C;cursor:pointer;font-size:18px;padding:0 4px;}

.sheet-total{
  padding:12px 20px 0;display:flex;justify-content:space-between;align-items:center;
  border-top:2px solid var(--green-light);margin-top:4px;
}
.total-label{font-size:14px;color:var(--text2);font-weight:700;}
.total-val{font-size:20px;font-weight:900;color:var(--green);}

.sheet-form{padding:12px 20px 0;}
.form-row{margin-bottom:10px;}
.form-row label{font-size:11px;font-weight:700;color:var(--text2);display:block;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;}
.form-row input,.form-row textarea{
  width:100%;padding:9px 12px;font-size:13px;font-family:'Nunito',sans-serif;
  border:1.5px solid #D4E8C8;border-radius:var(--rs);background:#FAFEF7;color:var(--text);
  transition:border-color 0.2s;
}
.form-row input:focus,.form-row textarea:focus{outline:none;border-color:var(--green2);}
.form-row textarea{resize:vertical;min-height:64px;}
.wa-btn{
  width:100%;padding:13px;background:#25D366;color:#fff;
  border:none;border-radius:var(--r);font-size:15px;font-weight:800;
  cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;
  transition:background 0.15s;font-family:'Nunito',sans-serif;margin:12px 0 20px;
}
.wa-btn:hover:not(:disabled){background:#1da851;}
.wa-btn:disabled{background:#D4E8C8;color:#7A8F72;cursor:default;}

.empty-cart{text-align:center;padding:32px;color:var(--text3);}
.empty-cart .big-emo{font-size:48px;display:block;margin-bottom:10px;}

/* PARCEL SECTION */
.parcel-banner{
  background:linear-gradient(135deg,#FFF4E0,#FFECC7);
  border:1.5px solid #FAD07A;border-radius:var(--r);
  padding:18px 20px;margin-bottom:28px;
  display:flex;align-items:center;gap:16px;
}
.parcel-emo{font-size:48px;flex-shrink:0;}
.parcel-text h3{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#7B4A00;margin-bottom:4px;}
.parcel-text p{font-size:13px;color:#9B6A20;font-weight:600;line-height:1.5;}
.parcel-btn{
  margin-left:auto;flex-shrink:0;
  background:var(--amber);color:#fff;border:none;
  padding:9px 16px;border-radius:var(--rs);font-size:13px;font-weight:800;
  cursor:pointer;font-family:'Nunito',sans-serif;white-space:nowrap;
  transition:background 0.15s;
}
.parcel-btn:hover{background:#B56D00;}

/* TOAST */
.toast{
  position:fixed;top:24px;left:50%;transform:translateX(-50%) translateY(-80px);
  background:var(--green);color:#fff;padding:10px 20px;border-radius:30px;
  font-size:13px;font-weight:700;z-index:999;
  transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1);pointer-events:none;
  white-space:nowrap;
}
.toast.show{transform:translateX(-50%) translateY(0);}

/* FOOTER INFO */
.footer-info{
  background:var(--green);color:#fff;border-radius:var(--r);
  padding:20px 24px;margin-top:8px;
  display:grid;grid-template-columns:1fr 1fr;gap:16px;
}
.fi-item{display:flex;gap:10px;align-items:flex-start;}
.fi-emo{font-size:20px;flex-shrink:0;}
.fi-text{font-size:12px;color:rgba(255,255,255,0.85);font-weight:600;line-height:1.5;}
.fi-text b{color:#fff;display:block;font-size:13px;}
</style>
</head>
<body>

<!-- CART FAB -->
<button class="cart-fab" onclick="toggleCart()">
  🛒 Keranjang <span class="fab-badge" id="fab-badge">0</span>
</button>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<!-- HERO -->
<div class="hero">
  <div class="hero-top">
    <div class="logo">
      <div class="logo-icon">🍎</div>
      <div>
        <div class="logo-name">Toko Buah ABS</div>
        <div class="logo-tagline">Segar Langsung ke Tangan Anda</div>
      </div>
    </div>
    <nav class="hero-nav">
      <a href="#produk" class="nav-link">Produk</a>
      <a href="#parcel" class="nav-link">Parcel</a>
      <a href="#lokasi" class="nav-link">Lokasi</a>
    </nav>
  </div>

  <div class="hero-body">
    <div class="hero-text">
      <div class="hero-badge">🌿 Menjual Aneka Buah Lokal & Impor</div>
      <h1 class="hero-title">Buah Segar,<br><span>Harga Terbaik</span></h1>
      <p class="hero-sub">Pilih, pesan, dan kami antarkan ke depan pintu Anda.<br>Tersedia buah lokal pilihan & buah impor berkualitas.</p>
      <div class="hero-chips">
        <span class="chip highlight">🚚 Antar ke Rumah</span>
        <span class="chip">🎁 Parcel Tersedia</span>
        <span class="chip">⭐ Kualitas Terjamin</span>
      </div>
    </div>
  </div>

  <div class="hero-info" style="padding:0 32px 0; gap:10px; flex-wrap:wrap;">
    <div class="info-pill">
      <span>📍</span>
      <div class="info-pill-text"><b>Lokasi</b>Jl. Mandala Raya, Ciparigi<br>Bogor Utara</div>
    </div>
    <div class="info-pill">
      <span>🕐</span>
      <div class="info-pill-text"><b>Jam Buka</b>08.00 – 21.30 WIB<br>Setiap Hari</div>
    </div>
    <div class="info-pill">
      <span>📱</span>
      <div class="info-pill-text"><b>Hubungi Kami</b>087875957722</div>
    </div>
  </div>

  <div class="hero-wave">
    <svg viewBox="0 0 900 40" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0,0 C150,40 350,0 450,20 C550,40 750,0 900,20 L900,40 L0,40 Z" fill="#FDFAF3"/>
    </svg>
  </div>
</div>

<!-- MAIN -->
<main>

  <!-- SEARCH + FILTER -->
  <div class="search-row">
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="search" placeholder="Cari buah..." oninput="renderGrid()">
    </div>
  </div>
  <div class="filter-tabs" id="filter-tabs">
    <div class="tab active" onclick="setFilter('semua',this)">Semua</div>
    <div class="tab" onclick="setFilter('lokal',this)">🌴 Buah Lokal</div>
    <div class="tab" onclick="setFilter('impor',this)">✈️ Buah Impor</div>
  </div>

  <!-- PARCEL BANNER -->
  <div class="parcel-banner" id="parcel">
    <div class="parcel-emo">🎁</div>
    <div class="parcel-text">
      <h3>Parcel Buah Cantik Tersedia!</h3>
      <p>Hampers & parcel buah segar untuk lebaran, ulang tahun, atau acara spesial.<br>Bisa custom isi & desain sesuai kebutuhan Anda.</p>
    </div>
    <button class="parcel-btn" onclick="orderParcel()">Pesan Parcel</button>
  </div>

  <!-- PRODUCT SECTION -->
  <div id="produk">
    <div class="section-header">
      <div class="section-title">Pilihan Buah Segar</div>
      <div class="section-count" id="prod-count">11 produk</div>
    </div>
    <div class="grid" id="grid"></div>
  </div>

  <!-- FOOTER INFO -->
  <div class="footer-info" id="lokasi">
    <div class="fi-item">
      <div class="fi-emo">📍</div>
      <div class="fi-text"><b>Alamat Toko</b>Jl. Mandala Raya, RT.02/RW.02<br>Ciparigi, Kec. Bogor Utara<br>Kota Bogor, Jawa Barat 16157</div>
    </div>
    <div class="fi-item">
      <div class="fi-emo">🕐</div>
      <div class="fi-text"><b>Jam Operasional</b>Senin – Minggu<br>08.00 – 21.30 WIB</div>
    </div>
    <div class="fi-item">
      <div class="fi-emo">📱</div>
      <div class="fi-text"><b>WhatsApp / Telpon</b>087875957722</div>
    </div>
    <div class="fi-item">
      <div class="fi-emo">🌿</div>
      <div class="fi-text"><b>Tentang Kami</b>Menjual aneka buah lokal dan impor segar berkualitas dengan harga terjangkau.</div>
    </div>
  </div>

</main>

<!-- CART OVERLAY -->
<div class="overlay" id="overlay" onclick="closeCartOutside(event)">
  <div class="cart-sheet" id="cart-sheet">
    <div class="sheet-handle"></div>
    <div class="sheet-head">
      <div class="sheet-title">Keranjang Belanja</div>
      <button class="close-btn" onclick="toggleCart()">✕</button>
    </div>
    <div class="sheet-body" id="sheet-body">
      <div id="cart-items-list"></div>
      <div id="cart-form-area"></div>
    </div>
  </div>
</div>

<script>
const products = [
  {id:1,name:"Jeruk Manis",emoji:"🍊",price:15000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:2,name:"Jeruk Kecil (Limau)",emoji:"🟠",price:10000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:3,name:"Mangga Harum Manis",emoji:"🥭",price:18000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:4,name:"Buah Naga Merah",emoji:"🔴",price:20000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:5,name:"Pisang Cavendish",emoji:"🍌",price:8000,unit:"per sisir",cat:"lokal",stock:true,tag:"lokal"},
  {id:6,name:"Belimbing Manis",emoji:"⭐",price:12000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:7,name:"Salak Pondoh",emoji:"🟤",price:14000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
  {id:8,name:"Nanas Madu",emoji:"🍍",price:10000,unit:"per buah",cat:"lokal",stock:true,tag:"lokal"},
  {id:9,name:"Apel Hijau",emoji:"🍏",price:28000,unit:"per kg",cat:"impor",stock:true,tag:"impor"},
  {id:10,name:"Apel Merah Fuji",emoji:"🍎",price:25000,unit:"per kg",cat:"impor",stock:true,tag:"impor"},
  {id:11,name:"Melon Kuning",emoji:"🍈",price:15000,unit:"per kg",cat:"lokal",stock:true,tag:"lokal"},
];

const tagLabel={lokal:"Lokal",impor:"Impor",parcel:"Parcel"};
const tagClass={lokal:"tag-lokal",impor:"tag-impor",parcel:"tag-parcel"};
let cart={}, qty={};
products.forEach(p=>qty[p.id]=1);
let filter='semua';

function setFilter(cat,el){
  filter=cat;
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderGrid();
}

function renderGrid(){
  const q=document.getElementById('search').value.toLowerCase();
  const filtered=products.filter(p=>{
    const catOk=filter==='semua'||p.cat===filter;
    const searchOk=p.name.toLowerCase().includes(q);
    return catOk&&searchOk;
  });
  document.getElementById('prod-count').textContent=filtered.length+' produk';
  document.getElementById('grid').innerHTML=filtered.map(p=>`
    <div class="card${p.stock?'':' out'}">
      <div class="card-tag ${tagClass[p.tag]}">${tagLabel[p.tag]}</div>
      <span class="fruit-emo">${p.emoji}</span>
      <div class="fruit-name">${p.name}</div>
      <div class="fruit-unit">${p.unit}</div>
      <div class="fruit-price">Rp ${p.price.toLocaleString('id-ID')}</div>
      <div class="stock-row">
        <div class="dot ${p.stock?'ada':'habis'}"></div>
        <span class="stock-text">${p.stock?'Stok Tersedia':'Stok Habis'}</span>
      </div>
      <div class="qty-row">
        <button class="qbtn" onclick="changeQty(${p.id},-1)" ${!p.stock?'disabled':''}>−</button>
        <span class="qval" id="qty-${p.id}">${qty[p.id]}</span>
        <button class="qbtn" onclick="changeQty(${p.id},1)" ${!p.stock?'disabled':''}>+</button>
        <button class="abtn" onclick="addToCart(${p.id})" ${!p.stock?'disabled':''}>${p.stock?'+ Keranjang':'Habis'}</button>
      </div>
    </div>
  `).join('');
}

function changeQty(id,d){
  qty[id]=Math.max(1,(qty[id]||1)+d);
  const el=document.getElementById('qty-'+id);
  if(el) el.textContent=qty[id];
}

function addToCart(id){
  const p=products.find(x=>x.id===id);
  if(!p||!p.stock)return;
  const q=qty[id]||1;
  if(cart[id]) cart[id].qty+=q;
  else cart[id]={...p,qty:q};
  qty[id]=1;
  renderGrid();
  updateBadge();
  showToast('✅ '+p.name+' ditambahkan!');
}

function updateBadge(){
  const t=Object.values(cart).reduce((s,i)=>s+i.qty,0);
  document.getElementById('fab-badge').textContent=t;
}

function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2200);
}

function toggleCart(){
  const ov=document.getElementById('overlay');
  ov.classList.toggle('open');
  if(ov.classList.contains('open')) renderCartSheet();
}

function closeCartOutside(e){
  if(e.target===document.getElementById('overlay')) toggleCart();
}

function removeCart(id){
  delete cart[id];
  updateBadge();
  renderCartSheet();
}

function renderCartSheet(){
  const items=Object.values(cart);
  const list=document.getElementById('cart-items-list');
  const form=document.getElementById('cart-form-area');
  if(items.length===0){
    list.innerHTML='<div class="empty-cart"><span class="big-emo">🛒</span>Keranjang masih kosong.<br>Yuk pilih buah segar dulu!</div>';
    form.innerHTML='';
    return;
  }
  list.innerHTML=items.map(i=>`
    <div class="cart-item-row">
      <span class="ci-emo">${i.emoji}</span>
      <div class="ci-info">
        <div class="ci-name">${i.name}</div>
        <div class="ci-sub">${i.qty} × Rp ${i.price.toLocaleString('id-ID')}</div>
      </div>
      <span class="ci-price">Rp ${(i.qty*i.price).toLocaleString('id-ID')}</span>
      <button class="ci-del" onclick="removeCart(${i.id})">✕</button>
    </div>
  `).join('');
  const total=items.reduce((s,i)=>s+i.qty*i.price,0);
  list.innerHTML+=`<div class="sheet-total"><span class="total-label">Total Pembayaran</span><span class="total-val">Rp ${total.toLocaleString('id-ID')}</span></div>`;
  form.innerHTML=`
    <div class="sheet-form">
      <div class="form-row"><label>Nama Pemesan</label><input id="f-nama" placeholder="Nama lengkap Anda"></div>
      <div class="form-row"><label>Nomor WhatsApp</label><input id="f-wa" placeholder="08xxxxxxxxxx"></div>
      <div class="form-row"><label>Alamat Pengiriman</label><textarea id="f-alamat" placeholder="Tulis alamat lengkap Anda..."></textarea></div>
      <div class="form-row"><label>Catatan (opsional)</label><input id="f-note" placeholder="Contoh: pilihkan yang matang ya"></div>
      <button class="wa-btn" onclick="kirimOrder()">💬 Pesan via WhatsApp</button>
    </div>
  `;
}

function kirimOrder(){
  const nama=document.getElementById('f-nama').value.trim();
  const wa=document.getElementById('f-wa').value.trim();
  const alamat=document.getElementById('f-alamat').value.trim();
  const note=document.getElementById('f-note').value.trim();
  if(!nama||!wa||!alamat){alert('Isi nama, nomor WA, dan alamat dulu ya!');return;}
  const items=Object.values(cart);
  const total=items.reduce((s,i)=>s+i.qty*i.price,0);
  const detail=items.map(i=>`- ${i.name}: ${i.qty}x @ Rp${i.price.toLocaleString('id-ID')} = Rp${(i.qty*i.price).toLocaleString('id-ID')}`).join('%0A');
  const catatan=note?'%0A*Catatan:* '+encodeURIComponent(note):'';
  const msg=`*PESANAN TOKO BUAH ABS*%0A%0A*Nama:* ${encodeURIComponent(nama)}%0A*No. WA:* ${encodeURIComponent(wa)}%0A*Alamat:* ${encodeURIComponent(alamat)}${catatan}%0A%0A*Detail Pesanan:*%0A${detail}%0A%0A*TOTAL: Rp${total.toLocaleString('id-ID')}*%0A%0AMohon konfirmasi ketersediaan dan estimasi waktu pengiriman. Terima kasih! 🙏`;
  window.open('https://wa.me/6287875957722?text='+msg,'_blank');
}

function orderParcel(){
  const msg='Halo Toko Buah ABS! Saya ingin memesan *parcel buah*. Bisa info ketersediaan, pilihan isi, dan harga parcel yang tersedia? Terima kasih! 🎁';
  window.open('https://wa.me/6287875957722?text='+encodeURIComponent(msg),'_blank');
}

renderGrid();
</script>
</body>
</html>
