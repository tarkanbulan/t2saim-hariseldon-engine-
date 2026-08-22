# ⚡ SPARK GÖREV EMRİ: TALİMAT 1 (TR PODU) JULES KODLAMA ŞARTNAMESİNİ YAZMA DİREKTİFİ
**Hedef Ajan:** Gemini Spark Research Core  
**Konum:** `Google Drive / T2SAIM_OS / Hariseldon / Prediction_Project /`  
**Referans Doküman:** `01_TALIMAT_1_TR_PODU_MIMARI_PLANI_VE_JULES_BILETLERI.md`  
**Çıktı Hedef Dosyası:** `SPARK_TALIMAT_1_JULES_KODLAMA_YONERGESI.md`  
**Epistemik Standart:** *Matt Pocock mp-writing-for-agents & mp-to-tickets, John Ousterhout Deep Modules, Pydantic V2, DuckDB Parquet*

---

### 📋 SPARK'A VERİLECEK TALİMAT METNİ (KOPYALANABİLİR PROMPT):

```markdown
Sayın Spark Research Core,

T2SAIM & Hari Seldon sistem mimarisi gereğince 4'lü Güçler Ayrılığı Protokolü devrededir.

Baş Mimar James William tarafından tasarlanan ve Kaptan Tarco tarafından onaylanan **Talimat 1 (Türkiye Podu)** şartnamesi `Google Drive / T2SAIM_OS / Hariseldon / Prediction_Project /` klasöründedir.

Lütfen aşağıdaki adımları sırasıyla icra et:

1. **OKUMA VE ANALİZ:**
   - `Prediction_Project` klasöründeki `01_TALIMAT_1_TR_PODU_MIMARI_PLANI_VE_JULES_BILETLERI.md` ve `00_T2SAIM_JULES_MASTER_MIMARI_PLAN_VE_GURLER_AYRILIGI.md` dosyalarını oku.
   - `reference_corpus/` altındaki 25 master belgenin Türkiye (BIST, VIOP, Takasbank) ve Süper Emtia/Kripto verilerini teyit et.

2. **JULES İÇİN DETAYLI KODLAMA ŞARTNAMESİNİ YAZ:**
   - Çıktı Dosyası: `SPARK_TALIMAT_1_JULES_KODLAMA_YONERGESI.md`
   - Otonom kodlama ajanımız Jules'un tek seferde hatasız kodlayabilmesi için aşağıdaki 5 bileti eksiksiz sınıf imzaları, Pydantic V2 modelleri, DuckDB SQL şemaları ve test assertion'ları ile detaylandır:

     * **TICKET-TR-01:** `modules/markets/tr/tr_duckdb_manager.py` (Lakehouse DuckDB Tabloları ve CRUD fonksiyonları)
     * **TICKET-TR-02:** `modules/markets/tr/bist_decomposer.py` (BIST-100 Sektör Ayrıştırma, Top 10 Alfa Seçim Algoritması)
     * **TICKET-TR-03:** `modules/markets/tr/takas_fraud_shield.py` (C_takas >= 0.70 ve R_cancel >= 0.85 BVM Sahtekarlık Kalkanı)
     * **TICKET-TR-04:** `modules/markets/tr/tr_crisis_engine.py` (L4 Amigdala Psi_TR Kırılması, GVK Geçici 67 %0 Stopaj ve Nominal vs Reel Kâr Hesaplaması)
     * **TICKET-TR-05:** `modules/markets/tr/tr_runner.py` (Orkestratör, DuckDB Veri Beslemesi ve Kaptan Onay Kartı Üreticisi)

3. **TAMAMLANMA:**
   - Hazırladığın şartnameyi `Prediction_Project` klasörüne `SPARK_TALIMAT_1_JULES_KODLAMA_YONERGESI.md` olarak kaydet ve Kaptan ile James'in onayına sun.
```
