# 🛰️ JULES İÇİN T2SAIM TÜRKİYE KRİZ ERKEN UYARI VE BİRLEŞİK SOSYO-EKONOFİZİK SENSÖRÜ MİMARİ ŞARTNAMESİ
**Hedef Uygulayıcı:** Jules (Autonomous AI Coding Agent) / Hermes Multi-Agent Framework  
**Proje Adı:** T2SAIM Unified Crisis Early Warning & Socio-Physics Sensory Engine (Türkiye EWS v5.0)  
**Hedef Dizin:** `Google Drive / Macroekonomics / hermes_crisis_lab /` & `PROMETEUS_SISTEM /`  
**Tarih:** 23 Ağustos 2026  
**Standart:** Sıfır-Güven (Zero-Trust) Adli Ekonofizik, Richards Heuer Bilişsel Hijyeni, Zero Future Leakage ($\lambda=0.15$), Walk-Forward Back To The Future (BTF)  
**Teknoloji Yığını:** Python 3.11+, DuckDB Parquet, SQLite WAL, River (Online ML + ADWIN), TreeSHAP, Venn-Abers Calibration, Pydantic V2, FastMCP (Port 39300), QuantEcon  

---

## 1. MİMARİ GENEL BAKIŞ VE HİPOTEZ
Bu şartname, Türkiye piyasalarındaki makroekonomik, finansal, sosyo-antropolojik ve kurumsal kırılmaları **3 ay ila 1 yıl öncesinden tespit eden ve yanlış alarmları (false positives) %7'nin altına kalibre eden** Birleşik Kriz Takip Sensörü'nün (Unified Crisis Sensor) sıfırdan otonom olarak kodlanması için tüm matematiksel modelleri, veri gereksinimlerini, açıklanabilirlik algoritmalarını ve faz planını içerir.

Geleneksel ekonometrik modeller krizleri doğrusal finansal rasyolara (cari açık, bütçe açığı) indirgeyerek "neden şimdi patlamıyor?" sorusunu ıskalar. T2SAIM mimarisi ise krizleri **5 Boyutlu Dinamik Faz Geçişi (Phase Transition)** olarak modeller:

1. **Makroekonomik & Minsky Borç Rezonansı ($\Phi_{\text{Macro}}$):** Parabolik borç servisi vs doğrusal borç büyümesi kesişimi ($t^*$ tekilliği), net rezerv erimesi ve Kapalıçarşı kur makası (DOLGAP).
2. **Bankacılık & Likidite Kilitlenmesi ($\Phi_{\text{Bank}}$):** Kredi/mevduat gerilimi ($LDR$), ötelenen hayalet krediler ($NPL_{\text{real}}$), TED spread ve 4 finansal boğulma eğrisi (İcra, Çek, Kredi Kartı, Konkordato).
3. **Nörofinans & Toplumsal Kaçış ($\Phi_{\text{Neuro}}$):** Amigdala stres yükü ($A_{\text{load}}$), Prefrontal korteks denetim çöküşü ($PFC$), fiziki döviz/altına mevduat kaçış hızı ($v_{\text{run}}$) ve Kuramoto sürü senkronizasyonu ($H_{\text{herd}}$).
4. **Emilio Gullini Ekonofizik Güvensizlik Modeli ($\Phi_{\text{Gullini}}$):** Sözleşmelere ve resmi otoriteye inançsızlık ($G_{\text{def}}$), REER sarkaç aşırı değerlenmesi ve faz uzayı kaotik çekicisi.
5. **Daron Acemoğlu Kurumsal Çürüme & Adli Anomaliler ($\Phi_{\text{Acemoglu}}$):** Sömürücü kurum dengesi, ihale yoğunlaşması ($HHI$), Rant/İmalat kredi oranı, $TR\text{-}DEI$ Ölü Ekonomi Endeksi, $IDIS$ veri şeffaflığı ve LM-1/LM-2/LM-3 adli kanunları.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   T2SAIM UNIFIED CRISIS SENSOR ENGINE (MİMARİ AKIŞ)                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. ÇOK BOYUTLU VERİ TOPLAMA (DATA INGESTION PIPELINE)                                  │
│    ├── Makro & TCMB EVDS (M2/NIR, REER, Faiz, 191B$ Dış Borç, Swap Hariç Net Rezerv)   │
│    ├── Mikro Piyasa & Likidite (DOLGAP Kapalıçarşı, BIST-30 C_takas, VPIN, LDR, TED)   │
│    ├── Sosyo-Antropolojik & Adli (UYAP İcra, Karşılıksız Çek, Narkotik Atıksu, KİK)     │
│    └── OSINT & Yüksek Frekans (Telegram 8 Kanal, 103 RSS VADER/FinBERT, Polymarket)    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. 5 KATMANLI EKONOFİZİK & NÖRO-BİLİŞSEL ÇEKİRDEK                                      │
│    ├── Φ_Macro (Minsky Borç Duvarı & Rezerv Sıkışması)                                 │
│    ├── Φ_Bank (Hayalet Krediler & Likidite Boğulması)                                  │
│    ├── Φ_Neuro (A_load, PFC Kontrolü, v_run Mevduat Kaçışı)                            │
│    ├── Φ_Gullini (Güven Erozyonu G_def & Faz Uzayı Kaotik Çöküş Çekicisi)              │
│    └── Φ_Acemoglu (TR-DEI Kurumsal Çürüme, İhale HHI, LM 1-3 Adli Anomalileri)         │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. KALİBRASYON, ADAPTİF ÖĞRENME & YANLIŞ ALARM ELEME KATMANI                           │
│    ├── River + ADWIN: Rejim/Politika Değişimlerinde Konsept Kayması (Drift) Tespiti    │
│    ├── Conformal Prediction & Venn-Abers: Kalibre Edilmiş Olasılık Aralıkları [p0, p1] │
│    ├── BTF-Amnesia Sönümleme (λ = 0.15): Geçmiş Travma Sönümlemesi & Sıfır Sızıntı     │
│    └── TreeSHAP Faktör Ayrıştırması: Anlık Kriz Tetikleyicilerinin Şeffaflaştırılması   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. KARAR & İKİ KADEMELİ ERKEN UYARI ÇIKTISI                                            │
│    ├── ⚡ Taktik Kriz İbresi (D+14..D+45 Gün): DOLGAP + VPIN + Amigdala Kaçış Alarmı    │
│    ├── 🏛️ Stratejik Kriz İbresi (M+3..M+12 Ay): Minsky Borç Tekilliği (t*) + TR-DEI     │
│    └── 🛡️ Kasa Koruması: Çeyrek Kelly / %100 Nakit Kapısı / VIOP Kur Hedge             │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. VERİ SETİ GEREKSİNİMLERİ VE ÖZNİTELİK (FEATURE) HARİTASI
Jules, aşağıdaki 5 ana kaynaktan gelen zaman serilerini DuckDB Parquet ve SQLite WAL üzerinde birleştirmelidir:

### 2.1. Makroekonomik ve Para Politikası Serileri (Haftalık / Aylık)
* `M2_NIR_Ratio`: TCMB M2 Para Arzı / Net Uluslararası Rezervler (Swap hariç). Kritik eşik $> 15.0$.
* `Net_NIR_USD`: Swap hariç net rezerv seviyesi (Milyar USD). Kritik bölge $< -40$ Mr $.
* `REER_CPI_Base`: TÜFE Bazlı Reel Efektif Döviz Kuru ($2025=100$). Sarkaç tepesi $\theta \ge 68.0$ (Aşırı değerli TL).
* `Ext_Debt_Service_1Y`: 12 ay içinde vadesi gelen toplam dış borç servisi (Milyar USD). (Güncel: $191$ Mr $).
* `GLP_AOFM_Spread`: Geç Likidite Penceresi ile Ağırlıklı Ortalama Fonlama Maliyeti makası ($\%$).
* `Current_Account_GDP`: Yıllıklandırılmış Cari İşlemler Açığı / GSYH ($\%$).

### 2.2. Piyasa Mikroyapısı ve Likidite Göstergeleri (Günlük / Canlı)
* `DOLGAP_Premium`: Kapalıçarşı fiziki efektif dolar/altın kuru ile resmi bankalararası kur makası ($\%$).
* `BIST_Takas_Concentration` ($C_{\text{takas}}$): BIST-30 hisselerinde ilk 5 aracı kurum takas yoğunlaşması. Eşik $\ge 0.70$.
* `BIST_Cancel_Ratio` ($R_{\text{cancel}}$): Emir iptal / toplam emir oranı. Eşik $\ge 0.85$ (HFT manipülasyonu).
* `VPIN_Toxicity`: Hacim bazlı emir toksisitesi ($0.0 - 1.0$).
* `LDR_Ratio`: Bankacılık Kredi / Mevduat Oranı. Eşik $> 1.15$ (Likidite açığı).
* `NPL_Spread`: Yüzdürülen ve ötelenen gerçek takipteki kredi oranı ($NPL_{\text{real}}$) ile resmi $NPL$ makası ($NPL_{\text{real}} / NPL_{\text{resmi}} \ge 2.0$).
* `TED_Spread_TR`: TR Gösterge Tahvil faizi ile 3 aylık mevduat/interbank faiz makası ($\%$).

### 2.3. Nörofinans ve Davranışsal Kaçış Göstergeleri (Günlük)
* `A_load` (Amigdala Yükü): $\text{clip}(0.3 + (\sigma_{20}/\sigma_{60} - 1) \cdot \chi_\sigma, 0.1, 1.0)$, $\chi_\sigma = 0.25$.
* `PFC_control` (Prefrontal Korteks Denetimi): $\frac{1}{1 + \exp(\kappa_p \cdot (A_{\text{load}} - \theta_{\text{panic}}))}$, $\kappa_p = 5.0464$, $\theta_{\text{panic}} = 0.70$.
* `v_run` (Mevduat Kaçış Hızı): KKM ve TL mevduattan fiziki altın/döviz ve kripto varlıklara net transfer ivmesi ($0.0 - 1.0$).
* `H_herd` (Kuramoto Senkronizasyonu): $0.30 \cdot h_{\text{haber}} + 0.30 \cdot h_{\text{sosyal}} + 0.25 \cdot h_{\text{fng}} + 0.15 \cdot h_{\text{hacim}}$. Eşik $> 0.50$ (Kilitli sürü).

### 2.4. Sosyo-Antropolojik, Adli ve Toplumsal Göstergeler (Aylık / Çeyreklik)
* `UYAP_Active_Enforcement`: Aktif UYAP icra dosyası sayısı (Milyon).
* `Bounced_Checks_Volume`: Karşılıksız çek hacmi (Milyar TL) ve yıllık artış ivmesi.
* `Credit_Card_Default_Rate`: Asgari ödemesini yapamayan bireysel kredi kartı oranı ($\%$).
* `Concordat_Filings`: Konkordato ve iflas erteleme talep eden şirket sayısı.
* `Fatalism_Buffer`: Tevekkül tamponu doluluk oranı ($0.0 - 1.5$). Kriz şoklarının toplumsal patlamaya dönüşmesini geciktiren psikososyal katsayı.
* `Brain_Drain_Rate` ($f_{\text{BrainDrain}}$): Nitelikli işgücü göç hızı (Sigmoid eşiği: 80 bin kişi/yıl).
* `Narcotic_Wastewater_Signal`: Atıksu analizlerindeki uyarıcı/kimyasal kalıntı trendi (Toplumsal anestezi ve dopamin ikamesi göstergesi).

### 2.5. Acemoğlu Kurumsal Çürüme ve Adli Anomali Göstergeleri
* `TR_DEI`: Türkiye Ölü Ekonomi Endeksi ($0.30 f_{\text{GFCF}} + 0.25 f_{\text{BrainDrain}} + 0.25 f_{\text{FiscalObfuscation}} + 0.20 f_{\text{ProdCollapse}}$).
* `Procurement_HHI`: KİK kamu ihalelerinde ilk 5 holdingin yoğunlaşma skoru ($0 - 10000$, $>2500$ oligopol, $>4000$ tam kilitlenme).
* `KIK_21b_Ratio`: 4734 sayılı kanunun 21/b (pazarlık usulü) istisna maddesiyle dağıtılan ihalelerin toplam ihalelere oranı ($\%$).
* `Rent_to_Manufacturing_Credit`: İnşaat/Gayrimenkul kredilerinin Sanayi İmalat kredilerine oranı (Kritik: $>2.5\text{x}$).
* `LM1_Caliper_CV`: Gece yarısı KHK'ları ve keyfi bürokrat azillerinin zaman varyasyon katsayısı ($CV(\Delta t) < 0.15$).
* `LM2_Benford_MAD`: İhale bedelleri ve resmi istatistiklerde Benford ilk basamak sapması ($MAD_B$).
* `LM3_Entropy_DKL`: Resmi TÜİK enflasyon sepeti ve rezerv serilerinin yapay düzeltme entropi sapması ($D_{KL}(P \parallel Q)$).

---

## 3. MATEMATİKSEL FORMÜLLER VE İŞLEM KATMANLARI

### 3.1. Emilio Gullini 5 Katmanlı Kriz Endeksi ($G_{\text{def}}$ ve $Minsky\ t^*$)
Gullini kurumsal güvensizlik katsayısı ($G_{\text{def}}$):
$$G_{\text{def}}(t) = 0.40 \cdot \text{TED}_{\text{norm}}(t) + 0.35 \cdot \text{CDS}_{\text{norm}}(t) + 0.25 \cdot \text{TrustDeficit}_{\text{TCMB}}(t)$$

Minsky Rezonansı ve $t^*$ Tekillik Mesafesi: Doğrusal borç birikimi ($S_D(t) = S_0 + \mu_D t$) ile parabolik borç servisi ($S_S(t) = S_0 e^{r_{\text{eff}} t}$) eğrilerinin kesişim günü ($t^* = \text{2026-11-18}$):
$$\Phi_{\text{Gullini}}(t) = 0.55 \cdot G_{\text{def}}(t) + 0.45 \cdot \exp\left( - \frac{t^* - t}{90} \right)$$

### 3.2. Amnesia Bellek Sönümleme ve Sıfır Gelecek Sızıntısı (BTF Standardı)
Her $S_t$ stres sinyali için bellek yükü ($M_t$):
$$M_t = S_t + (1.0 - \lambda) \cdot M_{t-1}, \quad \lambda = 0.15$$
* $\lambda = 0.15$ mühürlü katsayısı, kriz öncesi 3 aylık (1 çeyrek) kümülatif stres birikimini korurken eski şokları sönümler.
* L6 Faz Kilidi ($L6_{\text{gate}}$):
$$L6_{\text{gate}} = 1 \iff (SRI_{\text{psy}} > 0.50) \land (SRI_{\text{fin}} > 0.45) \land (SRI_{\text{vol}} > 0.50)$$

### 3.3. Doğrusal Olmayan Birleşik Kriz İndeksi ($UCI$)
$$UCI(t) = 1.0 - \exp\left( - 1.45 \cdot \left[ w_1 \Phi_{\text{Macro}} + w_2 \Phi_{\text{Bank}} + w_3 \Phi_{\text{Neuro}} + w_4 \Phi_{\text{Gullini}} + w_5 \Phi_{\text{Acemoglu}} \right] \right)$$
* Sabit Ağırlıklar: $w = [0.25, 0.20, 0.20, 0.20, 0.15]$

---

## 4. YANLIŞ ALARMLARIN KALİBRASYONU VE ADAPTİF ML
Jules, sistemin yanlış alarm oranını %7'nin altında tutmak için şu 4 modern yapay zeka yöntemini entegre edecektir:

1. **River + ADWIN Konsept Kayması Dedektörü:** `river.drift.ADWIN(delta=0.002)` akışı izler. Drift tespit edildiğinde Amnesia $\lambda = 0.25$'e yükseltilerek 20 işlem gününde yeni rejime yumuşak uyum sağlanır.
2. **Conformal Prediction ve Venn-Abers Olasılık Kalibrasyonu:** $P(\text{Crisis}) \in [p_0, p_1]$ aralığı Venn-Abers Isotonic Regression ile $ECE \le 0.0124$ hassasiyetinde üretilir.
3. **Stoa Veto ve Dempster-Shafer Çelişki Filtresi:** Katmanlar arası çelişki $K \ge 0.85$ ise sistem `ABSTENTION` moduna geçer.
4. **TreeSHAP Açıklanabilirlik:** Her gün anlık etki eden ilk 5 faktör şeffaf yüzde olarak raporlanır.

---

## 5. DOSYA VE MODÜL HİYERARŞİSİ

```
t2saim_crisis_engine/
├── pyproject.toml
├── README.md
├── config/
│   ├── settings.py                # Pydantic V2 BaseSettings, Mühürlü Sabitler
│   └── thresholds.yaml            # Eşik Değerleri (Sigma 1.0 / 1.25, ECE <= 0.0124)
├── core/
│   ├── schemas.py                 # TelemetryInput, CrisisOutput Pydantic Modelleri
│   ├── amnesia.py                 # BTF Walk-Forward & Exponential Forgetting (λ=0.15)
│   ├── adwin_drift.py             # River ADWIN Concept Drift Yönetimi
│   └── venn_abers.py              # Venn-Abers & Conformal Prediction Kalibrasyonu
├── analyzers/
│   ├── macro_minsky.py            # Dış Borç, REER, Net NIR, DOLGAP Analizi
│   ├── banking_liquidity.py       # LDR, NPL_real, TED Spread, 4 Boğulma Eğrisi
│   ├── neuro_amigdala.py          # A_load, PFC_control, v_run, H_herd (Kuramoto)
│   ├── gullini_protocol.py        # G_def, Minsky t* Tekilliği, Kaotik Çekici
│   ├── acemoglu_decay.py          # TR-DEI, İhale HHI, LM-1/2/3 Adli Testleri
│   └── shap_explainer.py          # TreeSHAP / Factored Crisis Attribution
├── engine/
│   ├── sensor.py                  # UnifiedCrisisSensor Ana Sınıfı (evaluate & stream)
│   └── execution_router.py        # Çeyrek Kelly, Panik Kapısı, VIOP Hedge Motoru
├── database/
│   ├── duckdb_store.py            # Parquet Zaman Serisi Veri Deposu
│   └── sqlite_telemetry.py        # WAL Modunda Günlük Telemetri Loglama
├── tests/
│   ├── test_amnesia_leakage.py    # Zero-Leakage BTF Doğrulama Testi
│   ├── test_false_alarm_rate.py   # 1960-2024 8/8 Kriz & %7.3 Yanlış Alarm Testi
│   └── test_sensor_integration.py # E2E Canlı Telemetri Entegrasyon Testi
└── main.py                        # CLI ve FastMCP API Sunucusu (Port 39300)
```

---

## 6. JULES İÇİN 5 ATOMİK UYGULAMA FAZI
* **PHASE 1:** Temel Veri Modelleri ve BTF-Amnesia Çekirdeği (`schemas.py`, `amnesia.py`).
* **PHASE 2:** 5 Ekonofizik ve Kurumsal Analiz Modülü (`macro_minsky`, `banking_liquidity`, `neuro_amigdala`, `gullini_protocol`, `acemoglu_decay`).
* **PHASE 3:** Adaptif Kalibrasyon, River ADWIN ve Conformal Prediction (`adwin_drift`, `venn_abers`, `shap_explainer`).
* **PHASE 4:** Birleşik Sensör Motoru ve Karar Yönlendirici (`sensor.py`, `execution_router.py`).
* **PHASE 5:** 33 Yıllık Tarihsel Doğrulama ve Kabul Testleri (1960-2024 8/8 kriz başarısı, yanlış alarm $\le \%7.3$).

---

*Şartname Sürümü: v5.0 — T2SAIM & Prometheus Ekosistemi — Veritas Per Se 2026*
