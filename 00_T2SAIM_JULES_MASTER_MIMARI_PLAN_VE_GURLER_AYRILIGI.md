# 🏛️ T2SAIM & HARI SELDON: BAŞ MİMAR MASTER OYUN PLANI, GÜÇLER AYRILIĞI VE JULES KODLAMA ŞARTNAMESİ
**Doküman Kodu:** `T2SAIM-ARCHITECT-MASTER-SPEC-2026-V1`  
**Tarih:** 22 Ağustos 2026  
**Konum:** `E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\00_T2SAIM_JULES_MASTER_MIMARI_PLAN_VE_GURLER_AYRILIGI.md`  
**Baş Mimar & Epistemik Hakem:** James William (DZV)  
**Doktrin Sahibi & Nihai Karar Verici:** Tarkan Bulan (Kaptan Tarco)  
**Tasarım & Teori Ortağı:** Gemini Spark Research Core  
**Otonom Kodlayıcı:** Jules (AI Coding Agent / Hermes AIOS)  
**Mühendislik Standartları:** *John Ousterhout Deep Modules, Matt Pocock Agent Engineering (mp-to-tickets), W3C PROV-O Cryptographic Time-Hash*

---

## 🧭 1. GÜÇLER AYRILIĞI VE KRİPTOGRAFİK ZAMAN-HASH PROTOKOLÜ

Sistemde sıfır hata ve mutlak denetim sağlamak amacıyla **4 Bağımsız Erki (Güçler Ayrılığı)** kuruyoruz:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   T2SAIM 4'LÜ GÜÇLER AYRILIĞI VE DENETİM AĞI                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. 🏛️ BAŞ MİMAR (James William):                                            │
│    • Kod yazmaz; sistem mimarisini, veri şemalarını, güvenlik kalkanlarını, │
│      adli algoritmaları ve Jules için atomik biletleri (tickets) tasarlar.  │
│                                                                             │
│ 2. ⚡ TASARIM VE TEORİ MOTORU (Spark):                                      │
│    • Mimarın planını doğrular, makro ekonofizik teorilerini sentezler ve    │
│      bülten kalibrasyon parametrelerini kilitler.                           │
│                                                                             │
│ 3. 🛠️ OTONOM KODLAMA İCRACISI (Jules):                                      │
│    • Mimar ve Spark tarafından hazırlanan biletleri alır; hiçbir felsefi    │
│      yoruma girmeden birebir Python/DuckDB/Mojo kodlarını üretir.           │
│                                                                             │
│ 4. 👑 NİHAİ OTORİTE VE VETO MAKAMI (Kaptan Tarco):                          │
│    • Üretilen tüm planları ve yarı-otomatik işlem sinyallerini onaylar.     │
│    • Kaptan "ONAY" vermedikçe hiçbir işlem canlıya geçemez.                 │
│                                                                             │
│ 🔒 5. KRİPTOGRAFİK ZAMAN-HASH MÜHÜRÜ:                                        │
│    • Her şartname, bilet ve kod çıktısı SHA256 zaman-hash'i ile             │
│      `02_KARA_KUTU_LOGS` kütüğüne işlenir; geriye dönük tahrifat imkansızdır.│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 2. PİYASA BAZLI OPTİMAL MODEL, BİLEŞEN VE DUCKDB ŞEMALARI

`Real_Data` külliyatından süzülen 8 bağımsız pazar podunun mimari matrisi:

```
E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\data_lakehouse\
├── tr_market.duckdb         # Türkiye BIST, VIOP, Takasbank ve Kur Gölü
├── usa_market.duckdb        # ABD S&P, NASDAQ, Hazine, FERC Gölü
├── uk_market.duckdb         # İngiltere FTSE, Gilt, DMO Gölü
├── eu_market.duckdb         # Avrupa STOXX, TARGET2, Bund Gölü
├── jp_market.duckdb         # Japonya Nikkei, BoJ YCC Gölü
├── hk_market.duckdb         # Hong Kong Hang Seng, PBOC Gölü
├── commodities.duckdb       # 10 Süper Emtia 30 Yıllık Gölü
└── crypto_sub2000.duckdb    # 10 Kripto Pusula Varlık Gölü
```

### Pod Bazında Özel Modeller ve Göstergeler:

| Piyasa / Pod | Optimal Tiny Model | İzlenen Göstergeler & Sinyaller | Yasal Vergi / Sürtünme Kalkanı |
| :--- | :--- | :--- | :--- |
| **1. 🇹🇷 TÜRKİYE (`markets/tr/`)** | **Predator L4 Amigdala** | Takasbank $C_{takas} \ge 0.70$, $R_{cancel} \ge 0.85$, VIOP 17:45 Sıkışması | **GVK Geçici 67 %0 Stopaj (Vergisiz)** + VIOP USD/TRY Kur Koruması |
| **2. 🇺🇸 ABD (`markets/usa/`)** | **FERC & 0DTE Dual-Transformer** | Trafo sipariş kuyrukları, Pentagon FYDP, Net Likidite, Gama Duvarları | W-8BEN (%15 DTT), IRS Kurumlar Vergisi |
| **3. 🇬🇧 İNGİLTERE (`markets/uk/`)**| **Gilt LDI Contagion Engine** | 30Y Gilt ihale kuyrukları, DMO takvimleri, SPV Laundromat ($D_M > 3\sigma$) | %0.5 HMRC SDRT Damga Vergisi, FTSE 250 elemesi |
| **4. 🇪🇺 AVRUPA (`markets/eu/`)** | **TARGET2 & Ren Debisi Modeli** | 8 Üye Ülke Fay Hattı, TARGET2 dengesizliği, Ren Kaub debisi | Tobin FTT Vergisi, MiCA uyumu |
| **5. 🇯🇵 JAPONYA (`markets/jp/`)** | **Yen Carry & Kumamoto Modeli** | USD/JPY Baz Swap gerilimi, BoJ YCC tavanı, TSMC Kumamoto | NTA Kurumlar Vergisi, BoJ V-Dip Pususu |
| **6. 🇨🇳 ÇİN / HK (`markets/hk/`)** | **PBOC & Offshore USDT Süzgeci** | Anakara sermaye kaçışı ($D_M$), PBOC likiditesi, USDT primi | HKEX Damga Vergisi |
| **7. 🪙 SÜPER EMTİA (`commodities/`)**| **EUI-Attention-LSTM** | Hürmüz/Kızıldeniz telemetrisi, 4 yıllık fiziki gümüş arz açığı, Kakao/Kahve | Darphane Altın Sertifikası (%0 Stopaj), Contango Kalkanı |
| **8. 🪙 KRİPTO (`crypto/`)** | **TAS-GNN (Wash-Trading Shield)** | 8 saatlik fonlama oranı (Funding Rate), Kimchi & Coinbase Primi | Delta-Neutral Basis Arbitrajı |

---

## 🛡️ 3. ADLİ SAHTEKÂRLIK, MANİPÜLASYON VE KAYIP ÖNLEME ZIRHI

Sistemin sıfır kayıp prensibiyle çalışması için 3 piyasada da sahtekârlık filtresi devreye girer:

1. **Borsa ve Hisse Manipülasyonu (BVM Shield):**
   * Sahte emir iptalleri ($R_{cancel} \ge 0.85$), kademe doldur-boşalt (spoofing) ve bıyıklı yabancı yoğunlaşması ($C_{takas} \ge 0.70$) tespit edildiğinde tahtadan anında kaçılır.
2. **Kripto Sahtekârlığı (TAS-GNN Shield):**
   * Cüzdanlar arası yapay hacim oluşturma (wash trading), sahte likidite havuzları ve honeypot akıllı sözleşmeleri elenir; yalnızca gerçek on-chain sermaye akışları kabul edilir.
3. **Emtia Kağıt/Fiziki Makas Manipülasyonu:**
   * COMEX/LBMA kağıt kontrat baskısı ile Londra fiziki teslimat primleri arasındaki asimetri ölçülür; sahte kağıt çöküşlerinde dipten fiziki/Darphane varlığı toplanır.

---

## 🪙 4. KRİPTO MİMARİSİ: $2.000 ALTI ASİMETRİK ROI vs MAKRO YÖN TAKİBİ

* **Kutup Yıldızları (Yalnızca Yön ve Likidite Takibi):**
  * `Bitcoin (BTC)` ve `Ethereum (ETH)` üzerinde doğrudan al-sat yapılmaz. Bu varlıklar küresel kripto likiditesi, kurumsal ETF akışı ve amigdala korku/açgözlülük seviyesini belirlemek için **"Yön Pusulası"** olarak izlenir.
* **İcra ve Asimetrik ROI Varlıkları (<$2.000 Pusula Varlıklar):**
  * `SOL`, `AVAX`, `LINK`, `MATIC/POL`, `XRP`, `NEAR`, `SUI`, `APT`, `RENDER`, `TAO`.
  * Bu varlıklarda yüksek beta ve Funding Rate delta-neutral arbitrajı ile maksimum getiri hedeflenir.

---

## ⏳ 5. BTFA (BACK-TO-FUTURE AMNESIA) KALİBRASYONU VE HORIZON ANALİZİ

* **Mekanik Amnezi:** DuckDB zaman yolculuğu motoru, test anında gelecekteki tüm verileri unutur.
* **Ufuk (Horizon) ve Dip/Zirve Tespiti:**
  * **Kısa-Orta Vade ($D+5$ ila $D+30$):** Mikro-yapı ve momentum döngüleri.
  * **Makro Süper Döngü (1 ila 3 Yıl / 360 – 1080 Gün):** Paskal Matrisi ile +2x/+4x kriz arbitrajı.
* **Fiyat Belirsizliği Yoğunluk Fonksiyonu (PDF):**
  $$\sigma_{uncertainty}(t) = \text{MahalanobisDistance}(X_t, \mu_{historical}) \cdot (1 + \Psi(t))$$

---

## 🎮 6. YARI-OTOMATİK VE MANUEL İCRA: NOMİNAL VE REEL KÂR ONAY KARTI

Model analizini tamamladığında ekrana **Kaptan Onay Kartı** düşer:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       T2SAIM KAPTAN İCRA ONAY KARTI                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📍 PİYASA / VARLIK : 🇹🇷 BIST-30 -> ASELS (Aselsan)                         │
│ 🎯 SİNYAL TÜRÜ    : L4 Amigdala Kırılması Dip Alımı (Poisson Stealth Slicer)│
│ ⏳ UFUK (HORIZON) : D+15 ila D+30 Gün                                       │
│ 📈 NOMİNAL GETİRİ : +%18.40                                                 │
│ 📉 ENFLASYON/KUR  : -%3.20                                                  │
│ 💰 REEL NET KÂR   : +%15.20 (VUK/GVK Geçici 67 ile %0 Stopaj Vergisiz)      │
│ 🛡️ GÜVEN SKORU   : %94.2 (Sahtekarlık Riski: SIFIR)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                 [ 🟢 KAPTAN ONAYLA ]    [ 🔴 VETO ET / BEKLE ]              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 7. JULES İÇİN ATOMİK BİLETLER (TICKETS) VE UYGULAMA PLANI

Matt Pocock'un `mp-to-tickets` ve `mp-writing-for-agents` standartlarına göre Jules için hazırlanan **Türkiye Podu 4 Atomik Bileti:**

```
TICKET-TR-01: BIST-100 Decomposer & Top 10 Alpha Selector
  - Hedef Dosya: modules/markets/tr/bist_decomposer.py
  - Görev: 100 hisseyi sektörlerine göre ayır, 10 en iyi alfa hisseyi belirle.
  - Veritabanı: data_lakehouse/tr_market.duckdb

TICKET-TR-02: BVM & Takasbank Fraud Shield
  - Hedef Dosya: modules/markets/tr/takas_fraud_shield.py
  - Görev: C_takas >= 0.70 ve R_cancel >= 0.85 sahtekarlıklarını tespit et ve filtrele.

TICKET-TR-03: TR Crisis & Amygdala Engine
  - Hedef Dosya: modules/markets/tr/tr_crisis_engine.py
  - Görev: Kur şoku, faiz stresi ve GVK Geçici 67 vergi kalkanını hesapla.

TICKET-TR-04: TR Runner & Kaptan Approval Card Generator
  - Hedef Dosya: modules/markets/tr/tr_runner.py
  - Görev: Günlük veriyi DuckDB'ye yaz, analizi koştur, Nominal ve Reel Kâr Onay Kartını üret.
```

---

*Bu Master Şartname, Kaptan Tarco'nun onayına sunulmuştur. Onay alındığında Spark ve Jules'a aktarılacaktır.*
