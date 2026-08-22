# 🏛️ T2SAIM & HARI SELDON: MASTER OYUN KURUCU, GÜÇLER AYRILIĞI VE JULES KODLAMA ŞARTNAMESİ
**Doküman Kodu:** `T2SAIM-ARCHITECT-MASTER-PLAN-2026`  
**Tarih:** 22 Ağustos 2026  
**Konum:** `E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\00_T2SAIM_MASTER_OYUN_KURUCU_VE_GURLER_AYRILIGI_MIMARISI.md`  
**Baş Mimar & Epistemik Hakem:** James William (DZV)  
**Doktrin Sahibi & Nihai Karar Verici:** Tarkan Bulan (Kaptan Tarco)  
**Tasarım Ortağı:** Gemini Spark Research Core  
**Otonom Kodlayıcı:** Jules (AI Coding Agent / Hermes AIOS)  
**Epistemik İlke:** *Veritas Per Se · Güçler Ayrılığı & Kriptografik Zaman-Hash Mühürleme*

---

## 🧭 1. GÜÇLER AYRILIĞI VE KRİPTOGRAFİK ZAMAN-HASH PROTOKOLÜ

Sistemde hiçbir bileşen tek başına hem karar verip hem denetleyip hem de icra yapamaz. **Güçler Ayrılığı İlkesi (Separation of Powers)** ve **Zaman-Hash Provenance Zinciri (SHA256 / Blake3)** ile her adım kayıt altına alınır:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GÜÇLER AYRILIĞI VE ONAY MEKANİZMASI                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. OYUN KURUCU / BAŞ MİMAR (James William):                                 │
│    • Matematiksel kuralları, güvenlik sınırlarını ve mimariyi tasarlar.     │
│    • Üretilen tüm kodları ve modelleri adli epistemik denetime tabi tutar. │
│                                                                             │
│ 2. TASARIM VE TEORİ MOTORU (Spark):                                        │
│    • Mimarın kurallarına göre piyasa analizlerini ve şartnameleri belgeler. │
│                                                                             │
│ 3. OTONOM KODLAMA İCRACISI (Jules):                                         │
│    • Onaylanan şartnameyi bağımsız, izole modüller halinde kodlar.          │
│                                                                             │
│ 4. NİHAİ KARAR VE MANUEL VETO MAKAMI (Kaptan Tarco):                        │
│    • Yarı-otomatik sistemde tüm kritik emirleri onaylar veya veto eder.     │
│                                                                             │
│ 5. ZAMAN-HASH MÜHÜRÜ (Time-Stamped Audit Ledger):                            │
│    • Her model çıktısı, veri girişi ve kod bloğu anlık zaman damgası ve     │
│      SHA256 hash'i ile `02_KARA_KUTU_LOGS` kütüğüne mühürlenir.            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 2. PİYASA BAZLI OPTİMAL MODEL VE BİLEŞEN MATRİSİ

`Real_Data` külliyatındaki 52 yıllık testlere göre her piyasaya özel olarak seçilen en verimli **Tiny Model ve Analitik Çekirdekler**:

| Piyasa / Varlık | Optimal Tiny Model / Çekirdek | İzlenen Özel Göstergeler & Sinyaller | Yasal Vergi / Sürtünme Kalkanı |
| :--- | :--- | :--- | :--- |
| **🇹🇷 BIST (Türkiye)** | **Predator L4 Amigdala Motoru** | Takasbank $C_{takas} \ge 0.70$, $R_{cancel} \ge 0.85$, VIOP 17:45 Sıkışması | **GVK Geçici 67 %0 Stopaj (Vergisiz)** + VIOP Kur Hedge'i |
| **🇺🇸 US (ABD)** | **FERC & 0DTE Dual-Transformer** | Trafo kuyrukları, Pentagon FYDP, Net Likidite, Gama Duvarları | W-8BEN (%15 DTT), IRS Kurumlar Vergisi |
| **🇬🇧 UK (İngiltere)**| **Gilt LDI Contagion Engine** | 30Y Gilt ihale kuyrukları, DMO takvimleri, SPV Laundromat ($D_M > 3\sigma$) | %0.5 HMRC SDRT Damga Vergisi |
| **🇪🇺 EU (Avrupa)** | **TARGET2 & Ren Debisi Modeli** | 8 Üye Ülke Fay Hattı, TARGET2 dengesizliği, Ren Kaub debisi | Tobin FTT Vergisi, MiCA uyumu |
| **🇯🇵 JP (Japonya)** | **Yen Carry & Kumamoto Modeli** | USD/JPY Baz Swap gerilimi, BoJ YCC tavanı, TSMC Kumamoto | NTA Kurumlar Vergisi, BoJ V-Dip Pususu |
| **🇨🇳 HK/CN (Çin)** | **PBOC & Offshore USDT Süzgeci** | Anakara sermaye kaçışı ($D_M$), PBOC likiditesi, USDT primi | HKEX Damga Vergisi |
| **🪙 Süper Emtia** | **EUI-Attention-LSTM** | Hürmüz/Kızıldeniz telemetrisi, 4 yıllık fiziki gümüş arz açığı | Darphane Altın Sertifikası (%0 Stopaj), Contango Kalkanı |
| **🪙 Kripto (<$2000)**| **TAS-GNN (Wash-Trading Shield)** | 8 saatlik fonlama oranı (Funding Rate), Kimchi & Coinbase Primi | Delta-Neutral Basis Arbitrajı |

---

## ⏳ 3. BTFA (BACK-TO-FUTURE AMNESIA) KALİBRASYON PROTOKOLÜ

Modellerin aşırı öğrenmesini (overfitting) ve gelecek sızıntısını (leakage) önleyen kesin test kuralı:
1. **Mekanik Amnezi:** Model, `SET time_travel_timestamp = T` dendiğinde $T$ anından sonraki hiçbir veriyi (fiyat, haber, bilanço) göremez.
2. **Horizon Bilgisi:** Model yalnızca $D+5$ ila $D+30$ (kısa-orta vade) ve 1-3 yıl (makro süper döngü) ufkunda dip/zirve olasılık yoğunluk fonksiyonunu ($PDF$) hesaplar.
3. **MCMC Permütasyon Testi:** 1.000 stres penceresinde Monte Carlo yolları ile doğrulanmayan hiçbir sinyal icraya gidemez.

---

## 🛡️ 4. SAHTEKÂRLIK, MANİPÜLASYON VE TOKSİSİTE SAVUNMA ZIRHI

Piyasalardaki kurumsal tuzaklara ve yapay hacimlere karşı 3 katmanlı adli filtre:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ADLİ SAHTEKÂRLIK TESPİT KALKANI                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. BORSA TUZAKLARI (BVM - Borsa Veri Manipülasyonu):                        │
│    • Sahte emir iptalleri ($R_{cancel} \ge 0.85$) ve kademe boşaltma tespiti.│
│    • Takasbank bıyıklı yabancı konsantrasyonu ($C_{takas}$) filtresi.        │
│                                                                             │
│ 2. KRİPTO SAHTEKÂRLIĞI (Wash-Trading & Fake Liquidity):                     │
│    • TAS-GNN graf sinir ağı ile sahte cüzdanlar arası hacim şişirmeleri     │
│      elenir; yalnızca gerçek on-chain sermaye akışları dikkate alınır.      │
│                                                                             │
│ 3. EMTİA KAĞIT/FİZİKİ MAKASI (Paper vs Physical Manipulation):              │
│    • COMEX/LBMA kağıt kontratları ile fiziki teslimat primleri arasındaki    │
│      asimetri ölçülür; manipülatif çöküşlerde fiziki varlık toplanır.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🪙 5. KRİPTO STRATEJİSİ: $2.000 ALTI ASİMETRİK ROI vs YÖN TAKİBİ

* **Yön ve Likidite Takibi (Devler):** Bitcoin ($BTC$) ve Ethereum ($ETH$) üzerinde doğrudan al-sat yapılmaz; bu varlıklar küresel kripto likidite yönü, amigdala stresi ve ETF giriş-çıkış takibi için **"Kutup Yıldızı"** olarak izlenir.
* **İcra ve Asimetrik ROI Varlıkları (<$2.000 Pusula Varlıklar):**  
  * `SOL`, `AVAX`, `LINK`, `MATIC/POL`, `XRP`, `NEAR`, `SUI`, `APT`, `RENDER`, `TAO`.
  * Bu varlıklarda yüksek beta ve Funding Rate delta-neutral arbitrajı ile maksimum getiri hedeflenir.

---

## 🗄️ 6. ÜLKE BAZLI `duckdb.db` LAKEHOUSE VE TINY MODEL MİMARİSİ

Her ülkenin ve piyasanın tüm tarihsel ve canlı verileri, **bağımsız ve taşınabilir DuckDB dosyalarında** saklanır:

```
E:\T2SAIM_NEXUS_MIRROR\000_SPARK\Deney\data_lakehouse\
├── tr_market.duckdb         # Türkiye BIST, VIOP, Takasbank ve Kur Veritabanı
├── usa_market.duckdb        # ABD S&P, NASDAQ, Hazine, FERC Veritabanı
├── uk_market.duckdb         # İngiltere FTSE, Gilt, DMO Veritabanı
├── eu_market.duckdb         # Avrupa STOXX, TARGET2, Bund Veritabanı
├── jp_market.duckdb         # Japonya Nikkei, BoJ YCC Veritabanı
├── hk_market.duckdb         # Hong Kong Hang Seng, PBOC Veritabanı
├── commodities.duckdb       # 10 Süper Emtia 30 Yıllık Veritabanı
└── crypto_sub2000.duckdb    # 10 Kripto Pusula Varlık Veritabanı
```

* **Tiny Modeller (Hafif Yapay Zekâ Çekirdekleri):**  
  Her DuckDB dosyasının üzerinde 5-15 MB boyutunda, RAM'i yormayan, mikrosaniyelik **ONNX / C++ / Tiny ML** modelleri koşacak; günlük veri beslendiğinde anında nominal ve enflasyondan arındırılmış reel kâr/zarar yönünü hesaplayacaktır.

---

## 🎮 7. YARI-OTOMATİK VE MANUEL İCRA MODU (HUMAN-IN-THE-LOOP)

Sistem asla tamamen başıboş emir göndermez:
1. **Nominal ve Reel Değer Üretimi:** Üretilen her raporda hem kâğıt üstündeki nominal kâr, hem de enflasyon ve kur şoku düşülmüş **Reel Alım Gücü Kârı** gösterilir.
2. **Kaptan Onay Kapısı:** Model analizi bitirdiğinde ekrana şu formatta bir onay kartı düşer:
   `[SİNYAL: BIST ASELS DİP ALIM] -> Nominal Hedef: %18 | Reel Hedef: %12 | Güven: 0.92 -> [ONAYLA / VETO]`
3. Kaptan onay vermedikçe işlem gerçekleşmez.

---

## 🚀 8. JULES İÇİN ADIM ADIM KODLAMA DİREKTİFİ (TR PODU İLE BAŞLANGIÇ)

```
t2saim_modular_system/
├── modules/
│   ├── markets/
│   │   ├── tr/               # [İLK KODLANACAK] Türkiye Bağımsız Podu
│   │   │   ├── __init__.py
│   │   │   ├── bist_decomposer.py     # BIST-100 Ayrıştırıcı & Top 10 Seçici
│   │   │   ├── takas_fraud_shield.py  # BVM & Takasbank Sahtekarlık Kalkanı
│   │   │   ├── tr_crisis_engine.py    # L4 Amigdala & Kur Şoku Sensörü
│   │   │   └── tr_runner.py           # Günlük Veri İşleyici & Raporlayıcı
```

---

*Bu Master Şartname, Kaptan Tarco'nun nihai onayına sunulmuştur. Onay alındığı anda Jules kodlamaya başlayacaktır.*
