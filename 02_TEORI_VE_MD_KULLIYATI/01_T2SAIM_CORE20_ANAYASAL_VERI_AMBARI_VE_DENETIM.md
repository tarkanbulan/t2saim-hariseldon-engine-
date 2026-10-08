# 🏛️ T2SAIM CORE-20 ANAYASAL VERİ AMBARI VE ADLİ DENETİM KÜTÜĞÜ
**Mühür:** VERITAS PER SE (Yalnızca Hakikat)
**Kural:** SIFIR SENTETİK VERİ, SIFIR DUMMY, SIFIR TAHMİN (Anti-Fabrication Protocol)
**Kapsam:** 20 Kanonik Egemen Ülke (TUR, USA, GBR, DEU, FRA, ITA, ESP, GRC, NLD, CHE, NOR, JPN, KOR, IND, IDN, BRA, MEX, ZAF, CAN, AUS)
**Zaman Aralığı:** 1996 – 2026 (30 Yıllık Bitemporal Seri)

---

## 📊 1. RESMÎ VERİ AMBARI DENETİM TABLOSU (5.612 BİTEMPORAL GÖZLEM)
Aşağıdaki 13 kanonik Silver Parquet veri seti Dünya Bankası API v2, Eurostat ve FRED birincil sunucularından doğrudan çekilerek mühürlenmiştir:

| Kanonik Veri Seti (Parquet) | Core-20 Gözlem | Ülke Kapsamı | Zaman Aralığı | Kaynak Gösterge Kodu & Açıklama |
| :--- | :---: | :---: | :---: | :--- |
| `MIG_NET_MIGRATION_canonical_silver.parquet` | **600** | 20 / 20 | 1996–2025 | World Bank `SM.POP.NETM` (Net Uluslararası Göç) |
| `MIG_REMIT_IN_USD_canonical_silver.parquet` | **592** | 20 / 20 | 1996–2025 | World Bank `BX.TRF.PWKR.CD.DT` (Gelen İşçi Havaleleri, USD) |
| `TUR_ARR_TOTAL_canonical_silver.parquet` | **483** | 20 / 20 | 1996–2020 | World Bank `ST.INT.ARVL` (Uluslararası Turist Girişleri) |
| `TUR_RECEIPTS_USD_canonical_silver.parquet` | **407** | 20 / 20 | 1996–2020 | World Bank `ST.INT.RCPT.CD` (Uluslararası Turizm Gelirleri, USD) |
| `GOV_DEBT_GDP_canonical_silver.parquet` | **279** | 13 / 20 | 1996–2024 | Eurostat & FRED `GC.DOD.TOTL.GD.ZS` (Merkezi Hükümet Borcu / GSYİH %) |
| `GOV_EXPENSE_GDP_canonical_silver.parquet` | **494** | 20 / 20 | 1996–2023 | World Bank `GC.XPN.TOTL.GD.ZS` (Kamu Harcamaları / GSYİH %) |
| `TAX_REV_GDP_canonical_silver.parquet` | **495** | 19 / 20 | 1996–2024 | World Bank `GC.TAX.TOTL.GD.ZS` (Vergi Gelirleri / GSYİH %) |
| `EDU_EXPENSE_GOV_ZS_canonical_silver.parquet` | **359** | 19 / 20 | 1996–2025 | UNESCO / WB `SE.XPD.TOTL.GB.ZS` (Kamu Eğitim Harcaması / Bütçe %) |
| `TRANS_AIR_DEPARTURES_canonical_silver.parquet` | **541** | 20 / 20 | 1996–2023 | ICAO / WB `IS.AIR.DPRT` (Kayıtlı Havayolu Sefer Kalkış Sayısı) |
| `TRANS_AIR_FREIGHT_canonical_silver.parquet` | **541** | 20 / 20 | 1996–2023 | ICAO / WB `IS.AIR.GOOD.MT.K1` (Hava Kargo Taşımacılığı, Milyon Ton-Km) |
| `TRANS_AIR_PASSENGER_canonical_silver.parquet` | **541** | 20 / 20 | 1996–2023 | ICAO / WB `IS.AIR.PSGR` (Taşınan Havayolu Yolcu Sayısı) |
| `TRANS_LPI_INFRA_canonical_silver.parquet` | **140** | 20 / 20 | 2007–2022 | World Bank `LP.LPI.INFR.XQ` (Lojistik Performans Endeksi - Altyapı) |
| `TRANS_LPI_LOGS_canonical_silver.parquet` | **140** | 20 / 20 | 2007–2022 | World Bank `LP.LPI.LOGS.XQ` (Lojistik Performans Endeksi - Hizmet Kalitesi) |
| **GENEL TOPLAM** | **5.612** | **20 Ülke** | **30 Yıl** | **[VERIFIED - SIFIR SENTETİK VERİ]** |

---

## 🔍 2. ADLİ VERİ TOPLAMA VE PROTOKOL RAPORU
# 🏛️ T2SAIM CORE-20 ANAYASAL VERİ AMBARI DENETİM RAPORU

**Kapsam:** Yalnızca 20 Kanonik Egemen Ülke (TUR, USA, GBR, DEU, FRA, ITA, ESP, GRC, NLD, CHE, NOR, JPN, KOR, IND, IDN, BRA, MEX, ZAF, CAN, AUS)
**Adli Kanıt Standardı:** Daubert Tier-1 Standardı
**Toplam Mühürlenen Satır Sayısı:** 5,612

| Dataset                                       |   Core-20 Rows | Countries Covered   | Year Range   |
|:----------------------------------------------|---------------:|:--------------------|:-------------|
| MIG_NET_MIGRATION_canonical_silver.parquet    |            600 | 20/20               | 1996-2025    |
| MIG_REMIT_IN_USD_canonical_silver.parquet     |            592 | 20/20               | 1996-2025    |
| TUR_ARR_TOTAL_canonical_silver.parquet        |            483 | 20/20               | 1996-2020    |
| TUR_RECEIPTS_USD_canonical_silver.parquet     |            407 | 20/20               | 1996-2020    |
| GOV_DEBT_GDP_canonical_silver.parquet         |            279 | 13/20               | 1996-2024    |
| GOV_EXPENSE_GDP_canonical_silver.parquet      |            494 | 20/20               | 1996-2023    |
| TAX_REV_GDP_canonical_silver.parquet          |            495 | 19/20               | 1996-2024    |
| EDU_EXPENSE_GOV_ZS_canonical_silver.parquet   |            359 | 19/20               | 1996-2025    |
| TRANS_AIR_DEPARTURES_canonical_silver.parquet |            541 | 20/20               | 1996-2023    |
| TRANS_AIR_FREIGHT_canonical_silver.parquet    |            541 | 20/20               | 1996-2023    |
| TRANS_AIR_PASSENGER_canonical_silver.parquet  |            541 | 20/20               | 1996-2023    |
| TRANS_LPI_INFRA_canonical_silver.parquet      |            140 | 20/20               | 2007-2022    |
| TRANS_LPI_LOGS_canonical_silver.parquet       |            140 | 20/20               | 2007-2022    |

# 🏛️ T2SAIM 37 ÜLKE GERÇEK VERİ HASAT VE ADLİ DENETİM RAPORU

**Tarih:** 2026-10-08T09:54:17.400707+00:00
**Kural:** SIFIR SENTETİK VERİ (Veritas Per Se)
**Toplam Çekilen Gerçek Veri Satırı:** 8,552

| Metric               | Code              | Folder                 |   Records |   Countries | YearRange   |
|:---------------------|:------------------|:-----------------------|----------:|------------:|:------------|
| TUR_ARR_TOTAL        | ST.INT.ARVL       | 02_Turizm_Goc          |       841 |          37 | 1996-2020   |
| TUR_RECEIPTS_USD     | ST.INT.RCPT.CD    | 02_Turizm_Goc          |       789 |          37 | 1996-2020   |
| MIG_REMIT_IN_USD     | BX.TRF.PWKR.CD.DT | 02_Turizm_Goc          |       982 |          36 | 1996-2025   |
| MIG_NET_MIGRATION    | SM.POP.NETM       | 02_Turizm_Goc          |      1110 |          37 | 1996-2025   |
| GOV_DEBT_GDP         | GC.DOD.TOTL.GD.ZS | 03_Maliye              |       418 |          22 | 1996-2024   |
| TAX_REV_GDP          | GC.TAX.TOTL.GD.ZS | 03_Maliye              |       861 |          33 | 1996-2024   |
| TRANS_AIR_FREIGHT    | IS.AIR.GOOD.MT.K1 | 06_Ulastirma_Transport |      1010 |          37 | 1996-2023   |
| TRANS_AIR_PASSENGER  | IS.AIR.PSGR       | 06_Ulastirma_Transport |      1012 |          37 | 1996-2023   |
| TRANS_AIR_DEPARTURES | IS.AIR.DPRT       | 06_Ulastirma_Transport |      1013 |          37 | 1996-2023   |
| TRANS_LPI_INFRA      | LP.LPI.INFR.XQ    | 06_Ulastirma_Transport |       258 |          37 | 2007-2022   |
| TRANS_LPI_LOGS       | LP.LPI.LOGS.XQ    | 06_Ulastirma_Transport |       258 |          37 | 2007-2022   |
