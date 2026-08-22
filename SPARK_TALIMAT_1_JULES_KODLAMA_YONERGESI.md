# 🛠️ SPARK TALİMAT 1: TÜRKİYE PODU JULES KODLAMA ŞARTNAMESİ
**Doküman Kodu:** `SPARK-TALIMAT-1-JULES-SPEC-2026`  
**Tarih:** 22 Ağustos 2026  
**Konum:** `E:\T2SAIM_NEXUS_MIRROR\000_SPARK\T2SAIM _OS\Prediction_Project\SPARK_TALIMAT_1_JULES_KODLAMA_YONERGESI.md`  
**Hazırlayan:** Gemini Spark Research Core  
**Mimar & Hakem:** James William (DZV)  
**Nihai Onay Makamı:** Tarkan Bulan (Kaptan Tarco)  
**Hedef İcracı:** Jules (Autonomous AI Coding Agent)  
**Standartlar:** *Pydantic V2, DuckDB Parquet/WAL, John Ousterhout Deep Modules, Matt Pocock mp-to-tickets, Pytest TDD*

---

## 🧭 1. GİRİŞ VE GÖREV TANIMI

Bu şartname, Baş Mimar James William tarafından belirlenen mimari doğrultusunda **Türkiye Podu'nun (`modules/markets/tr/`)** otonom kodlayıcımız **Jules** tarafından sıfır hata ile inşa edilmesi için hazırlanmıştır.

---

## 🎟️ TICKET-TR-01: `modules/markets/tr/tr_duckdb_manager.py`
* **Sorumluluk:** `data_lakehouse/tr_market.duckdb` yerel gölünü ve 4 temel SQL tablosunu (`bist_daily_candles`, `tr_macro_crisis_telemetry`, `compass_assets_daily`, `tr_signals_ledger`) oluşturmak, WAL modunu etkinleştirmek ve nedensellik penceresi (`get_causal_bist_window`) çekicilerini sağlamak.
* **Veri Modeli:** `BISTCandleRecord` (Pydantic V2 alias, `ge=0.0`, `le=1.0` doğrulamaları).

---

## 🎟️ TICKET-TR-02: `modules/markets/tr/bist_decomposer.py`
* **Sorumluluk:** BIST-100 endeksini 3 stratejik kümeye ayırmak (İhracatçılar %40, Yüksek Beta/Teknoloji %30, Savunmacı %30); hızlı fraktal eğim algoritması (`compute_hurst_fast`, $<0.2\text{ ms}$) ve temel çarpanlarla **Top 10 Alfa Hissesini** seçmek.
* **Alfa Formülü:**
  $$\text{Score}_i = \left( \frac{\text{NetKarMarji}_i \cdot \text{DövizGelirOranı}_i}{\text{Borç/FAVÖK}_i + \epsilon} \right) \cdot (1 - R_{\text{cancel}, i}) \cdot (1 - C_{\text{takas}, i}) \cdot W_{\text{sektör}} \cdot \left(\frac{h_i}{0.50}\right)$$

---

## 🎟️ TICKET-TR-03: `modules/markets/tr/takas_fraud_shield.py`
* **Sorumluluk:** Bıyıklı yabancı konsantrasyonu ($C_{\text{takas}} \ge 0.70$), sahte emir iptali ve kademe boşaltma ($R_{\text{cancel}} \ge 0.85$, $\text{VPIN} \ge 0.45$) anomalilerini filtrelemek; kripto varlıklarda TAS-GNN wash-trading denetimini ($>0.40$ veto) uygulamak.
* **Çıktı Modeli:** `FraudAuditResult` (`is_cleared`, `rejection_code`, risk metrikleri).

---

## 🎟️ TICKET-TR-04: `modules/markets/tr/tr_crisis_engine.py`
* **Sorumluluk:** L4 Amigdala $\Psi_{\text{TR}}$ kriz göstergesini hesaplamak; 1.000.000 Vektörize MCMC Simülasyonunu (Student-t $\nu=4.5$ + Merton Jump Diffusion, $<120\text{ ms}$) yürütmek; GVK Geçici 67 kapsamında **%0 Stopaj (Vergisiz)** ve enflasyon/kur sürtünmesi arındırılmış **Reel Net Alım Gücü Kârını** üretmek.
* **Reel Kâr Denklemi:**
  $$\text{Reel Net Kâr} = \frac{1 + \text{Nominal Kâr}}{1 + \text{Enflasyon} + \text{Kur Artışı}} - 1 - \text{Sürtünme}$$

---

## 🎟️ TICKET-TR-05: `modules/markets/tr/tr_runner.py`
* **Sorumluluk:** Tüm modülleri tek bir akışta birleştiren ana orkestratör. Analiz sonucunda terminale ve JSON kütüğüne SHA256 zaman-mühürlü **Kaptan İcra Onay Kartı** çıktısını üretir.

---

## 🧪 TEST DOĞRULAMA KÜTÜĞÜ: `tests/test_tr_pod.py`
1. `test_hurst_computation`: Hızlı Hurst üssünün geçerlilik aralığını ($0.10 \le h \le 0.95$) denetler.
2. `test_takas_fraud_shield_veto & test_takas_fraud_shield_pass`: Sahte ve organik tahta ayrımını doğrular.
3. `test_1m_mcmc_latency_and_distribution`: 1 Milyon simülasyonun gecikmesini ($<500\text{ ms}$) ve kuyruk sıralamasını test eder.
4. `test_gvk_67_zero_tax_real_profit`: GVK Geçici 67 %0 stopaj kuralını (`gvk_tax_deduction == 0.0`) garanti altına alır.

---

*Bu belge, Baş Mimar James William ve Kaptan Tarco'nun nihai onayına sunulmuştur.*
