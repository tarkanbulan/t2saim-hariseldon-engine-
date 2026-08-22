# 🏛️ T2SAIM TALİMAT 1: TÜRKİYE (TR) BAĞIMSIZ PODU, DUCKDB MİMARİSİ VE JULES İCRA BİLETLERİ
**Doküman Kodu:** `T2SAIM-TALIMAT-1-TR-POD-SPEC-2026`  
**Tarih:** 22 Ağustos 2026  
**Konum:** `E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\TALIMAT_1_TR_PODU_MIMARI_PLANI_VE_JULES_BILETLERI.md`  
**Baş Mimar & Oyun Kurucu:** James William (DZV)  
**Doktrin Sahibi & Nihai Onay Makamı:** Tarkan Bulan (Kaptan Tarco)  
**Tasarım & Talimat Ajanı:** Gemini Spark Research Core  
**Otonom Kodlayıcı:** Jules (AI Coding Agent / Hermes AIOS)  
**Mühendislik Standartları:** *John Ousterhout Deep Modules, Matt Pocock mp-to-tickets & mp-writing-for-agents, W3C Cryptographic Time-Hash*

---

## 🧭 1. GÜÇLER AYRILIĞI VE İŞ AKIŞI PROTOKOLÜ

Bu şartname, Kaptan'ın 1. Talimatı gereğince hazırlanmış; **Türkiye Podu'nun (`modules/markets/tr/`) sıfır hata ile inşa edilmesi için Spark'a detaylı talimat yazma emri verecek mimari temeldir.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       GÜÇLER AYRILIĞI VE AKIŞ ZİNCİRİ                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. 👑 KAPTAN (Emir & Vizyon):                                               │
│    • TR Podu: BIST-100 Ayrıştırma, 10 Kripto (<$2000), 30 Yıllık Emtialar,  │
│      Sahtekarlık Kalkanı, DuckDB, Tiny Modeller, Nominal/Reel Değer.        │
│                                                                             │
│ 2. 🏛️ JAMES (Baş Mimar - Mevcut Aşama):                                     │
│    • Mimariyi, DuckDB şemalarını, formülleri ve 5 atomik bileti planlar.    │
│    • SHA256 zaman-hash'ini Kara Kutu'ya mühürler.                           │
│                                                                             │
│ 3. ⚡ SPARK (Detaylı Talimat Yazarı - Sıradaki Aşama):                      │
│    • James'in bu planını alır; Jules'un anlayacağı Pydantic V2 tipli,       │
│      çalıştırılabilir Python kodlama talimatını yazar.                      │
│                                                                             │
│ 4. 🔍 KONTROL VE KAPTAN ONAYI:                                              │
│    • Spark'ın hazırladığı kodlama talimatı Kaptan'a sunulur ve onaylanır.   │
│                                                                             │
│ 5. 🛠️ JULES (Otonom Kodlayıcı):                                             │
│    • Onaylanan talimatı alır; dosyaları sırasıyla kodlar ve test eder.     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ 2. `tr_market.duckdb` VERİTABANI ŞEMASI VE TABLO YAPILARI

Her piyasa bağımsız bir DuckDB gölünde yaşar. Türkiye podunun kalbi:  
📁 `E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\data_lakehouse\tr_market.duckdb`

```sql
-- 1. BIST Günlük Fiyat ve Mikro-Yapı Tablosu
CREATE TABLE IF NOT EXISTS bist_daily_candles (
    timestamp TIMESTAMP,
    symbol VARCHAR(10),
    sector VARCHAR(30),
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE,
    c_takas DOUBLE,        -- Takasbank Konsantrasyonu (0.0 - 1.0)
    r_cancel DOUBLE,       -- Sahte Emir İptal Oranı (0.0 - 1.0)
    vpin DOUBLE,           -- Toksisite İndeksi
    PRIMARY KEY (timestamp, symbol)
);

-- 2. Türkiye Makro, Kur ve Kriz Göstergeleri
CREATE TABLE IF NOT EXISTS tr_macro_crisis_telemetry (
    timestamp TIMESTAMP PRIMARY KEY,
    usd_try DOUBLE,
    cbrt_policy_rate DOUBLE,
    cds_5y DOUBLE,
    viop_squeeze_index DOUBLE, -- 17:45 VIOP Teminat Sıkışması
    a_load DOUBLE,             -- Amigdala Korku Yükü (0.0 - 1.0)
    pfc_control DOUBLE,        -- Rasyonel Kontrol Oranı
    psi_decay DOUBLE           -- Seldon Kitle Kırılma Katsayısı
);

-- 3. Pusula Varlıklar (<$2000 Kripto & 30Y Süper Emtialar)
CREATE TABLE IF NOT EXISTS compass_assets_daily (
    timestamp TIMESTAMP,
    asset_type VARCHAR(20),    -- 'CRYPTO_SUB2000' veya 'SUPER_COMMODITY'
    symbol VARCHAR(15),        -- 'SOL', 'AVAX', 'XAG_USD', 'COCOA_FUT'
    price DOUBLE,
    funding_rate DOUBLE,       -- Kripto 8h Fonlama Oranı
    wash_trading_score DOUBLE, -- TAS-GNN Sahtekarlık Skoru (0-1)
    physical_premium DOUBLE,   -- Emtia Fiziki Teslimat Primi
    PRIMARY KEY (timestamp, symbol)
);

-- 4. Ex-Ante Tahminler ve Kaptan Onay Kütüğü
CREATE TABLE IF NOT EXISTS tr_signals_ledger (
    signal_id VARCHAR(64) PRIMARY KEY,
    timestamp TIMESTAMP,
    symbol VARCHAR(15),
    horizon_days INTEGER,      -- D+5, D+15, D+30
    nominal_expected_roi DOUBLE,
    real_expected_roi DOUBLE,  -- Enflasyon/Kur düşülmüş Net Alım Gücü Kârı
    confidence_score DOUBLE,
    fraud_risk_score DOUBLE,
    captain_approval VARCHAR(10), -- 'PENDING', 'APPROVED', 'VETOED'
    sha256_hash VARCHAR(64)
);
```

---

## 🔬 3. BIST-100 AYRIŞTIRMA VE TOP 10 ALFA SEÇİM MATRİSİ

BIST-100 endeksi rastgele bir bütün değildir; 3 ana kümeye ayrıştırılır (`bist_decomposer.py`):
1. **İhracatçı / Döviz Gelirli Monopoller (%40 Ağırlık):** Kur şokundan pozitif etkilenen, dolar geliri olan liderler (Örn: `ASELS`, `THYAO`, `TUPRS`, `FROTO`).
2. **Yüksek Beta & Teknoloji (%30 Ağırlık):** Bilişsel ve savunma ivmesi yüksek olanlar (`KCHOL`, `SAHOL`, `ASELS`).
3. **Savunmacı Nakit Akışı (%30 Ağırlık):** Kriz anında amigdala çöküşüne direnen perakende/gıda devleri (`BIMAS`, `CCOLA`).

* **Top 10 Alfa Filtresi:**  
  $$Score_i = \left( \frac{\text{NetKarMarji}_i \cdot \text{DövizGelirOranı}_i}{\text{Borç/FAVÖK}_i + \epsilon} \right) \cdot (1 - R_{cancel, i}) \cdot (1 - C_{takas, i})$$

---

## 🛡️ 4. SAHTEKÂRLIK VE TOKSİSİTE TESPİT KALKANI (FRAUD SHIELD)

Sistemin sıfır kayıp prensibiyle çalışması için 3 piyasada da sahtekârlık filtresi devreye girer (`takas_fraud_shield.py`):

1. **Borsa Sahtekârlığı (BVM - Borsa Veri Manipülasyonu):**
   * $R_{cancel} \ge 0.85$ (Emirlerin %85'inden fazlası kademeden siliniyorsa tahta manipülatiftir, işlem yasaklanır).
   * $C_{takas} \ge 0.70$ (Takasın %70'i tek bir aracı kurumda veya bıyıklı yabancıda toplanmışsa mal boşaltma tuzağıdır, kaçılır).
2. **Kripto Sahtekârlığı (TAS-GNN Wash-Trading Shield):**
   * Sahte cüzdanlar arası yapay hacim döndürme skoru $> 0.40$ olan tokenlar elenir.
3. **Emtia Kağıt/Fiziki Makas Manipülasyonu:**
   * Kağıt kontrat fiyatı düşerken Londra/Kapalıçarşı fiziki primi artıyorsa, bu suni bir türev manipülasyonudur; dipten fiziki/Darphane sertifikası toplanır.

---

## 🪙 5. KRİPTO ($2.000 ALTI) VE 30 YILLIK SÜPER EMTİA DOKTRİNİ

* **Kutup Yıldızı Yön Takibi:** $BTC$ ve $ETH$ üzerinde al-sat yapılmaz; küresel likidite yönü, kurumsal ETF girişleri ve makro korku seviyesi için izlenir.
* **$2.000 Altı Asimetrik ROI Varlıkları:**  
  `SOL`, `AVAX`, `LINK`, `MATIC/POL`, `XRP`, `NEAR`, `SUI`, `APT`, `RENDER`, `TAO`.
* **29-30 Yıllık Tarihsel En İyi Süper Emtialar:**  
  1. `Gümüş (XAG)` (+%130 Net)  
  2. `Kakao (Cocoa)` (+%145 Net)  
  3. `Kahve (Coffee)` (+%84 Net)  
  4. `Altın (XAU)` (+%78 Net)  
  5. `Uranyum (UX1)` (+%62 Net)  
  6. `Bakır (HG)` (+%42 Net)

---

## 🇹🇷 6. TÜRKİYE KRİZ VE L4 AMİGDALA SENSÖRLERİ

Türkiye kriz motoru (`tr_crisis_engine.py`) anlık kitle çöküşünü şu formülle hesaplar:

$$\Psi_{TR}(t) = \left( \frac{A_{load}(t) \cdot (1.0 + \text{KurŞoku}(t))}{\text{TakasLikiditesi}(t) + \epsilon} \right) \cdot S_{decay}(t)$$

* $\Psi_{TR} \ge 0.80$ (Yerli Panik Satışı): Perakende yatırımcı amigdala korkusuyla tabana mal satarken, sistem **VİOP 17:45 Kur Hedge'i** ve **BIST-30 Vergisiz İhracatçı Monopoller** ile dipten toplar.

---

## 💰 7. YASAL VERGİ, SÜRTÜNME VE REEL ALIM GÜCÜ KÂRI

* **Vergi Kalkanı:** BIST hisselerinde **GVK Geçici 67 gereğince %0 Stopaj (Tamamen Vergisiz Alfa)**.
* **Nominal vs. Reel Değer Denklemi:**
  $$\text{Reel Net Kâr} = \frac{1 + \text{Nominal Kâr}}{1 + \text{Enflasyon/TÜFE} + \text{USDTRY Artışı}} - 1 - \text{Sürtünme}$$
  *(Sürtünme: Aracı kurum komisyonu %0.04 + Slippage %0.02 = %0.06)*.

---

## ⚡ 8. TINY MODELS (HAFİF YAPAY ZEKÂ) MİMARİSİ

* Bellek Kullanımı: `< 25 MB RAM`.
* Format: `ONNX Runtime` ve saf `Python/Numpy` vektörel matris hesaplaması.
* Hız: Milisaniyenin altında (<1.2 ms) sinyal üretimi.

---

## 📋 9. JULES İÇİN 5 ATOMİK MÜHENDİSLİK BİLETİ (`mp-to-tickets`)

Matt Pocock'un ajan mühendisliği standardına göre Jules'un yazacağı 5 bağımsız bilet:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       JULES İÇİN 5 ATOMİK İCRA BİLETİ                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🎫 TICKET-TR-01: DuckDB Lakehouse ve Veri Şeması Kurucusu                   │
│    • Dosya: modules/markets/tr/tr_duckdb_manager.py                         │
│    • Görev: tr_market.duckdb gölünü ve 4 ana tabloyu sıfır hata ile kurmak. │
│                                                                             │
│ 🎫 TICKET-TR-02: BIST-100 Decomposer & Top 10 Alfa Seçici                   │
│    • Dosya: modules/markets/tr/bist_decomposer.py                           │
│    • Görev: 100 hisseyi 3 sektöre ayırıp formülle Top 10 Alfayı seçmek.    │
│                                                                             │
│ 🎫 TICKET-TR-03: BVM & Takasbank Sahtekârlık Kalkanı (Fraud Shield)         │
│    • Dosya: modules/markets/tr/takas_fraud_shield.py                        │
│    • Görev: C_takas ve R_cancel anomalilerini süzüp riskli tahtaları elemek│
│                                                                             │
│ 🎫 TICKET-TR-04: L4 Amigdala Kriz Sensörü & Vergi/Reel Kâr Motoru           │
│    • Dosya: modules/markets/tr/tr_crisis_engine.py                          │
│    • Görev: Psi_TR amigdala kırılmasını ve %0 stopajlı Reel Kârı hesaplamak.│
│                                                                             │
│ 🎫 TICKET-TR-05: TR Master Runner & Kaptan İcra Onay Kartı                  │
│    • Dosya: modules/markets/tr/tr_runner.py                                 │
│    • Görev: Tüm podu koşturup terminale ve JSON'a Onay Kartını basmak.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ 10. SPARK İÇİN TALİMAT YAZMA YÖNERGESİ (SPARK TASK DIRECTIVE)

**Spark'ın Görevi:**  
James'in yukarıdaki 9 maddelik mimari planını ve 5 biletini referans alarak; Jules'un tek seferde hatasız kodlayacağı **Python 3.11 / DuckDB / Pydantic V2 kod bloklarını, sınıf yapılarını ve test assertion'larını içeren detaylı Kodlama Şartnamesini** yazmaktır.

---

*Bu Master Mimari Plan, Kaptan Tarco'nun onayına sunulmuştur.*
