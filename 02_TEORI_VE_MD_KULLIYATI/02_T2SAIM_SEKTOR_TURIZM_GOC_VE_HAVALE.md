# 🏛️ T2SAIM SEKTÖREL KÜTÜPHANE: TURİZM, GÖÇ VE İŞÇİ HAVALELERİ
**Mühür:** VERITAS PER SE  
**Konum:** `10_SEKTOREL_VE_TEMATIK_KUTUPHANELER/02_Turizm_Goc`  
**Rolü:** Kriz anlarında döviz likiditesi, rezerv tamponu ve beşeri sermaye kaçışı göstergeleri.

---

# T2SAIM-37 Turizm ve Göç (Tourism & Migration) Sensör Mimarisi (1996-2026)

## 1. Kapsam ve Amaç
Bu modül, T2SAIM 37-ülke paneli için 1996–2026 zaman aralığında:
- **Turizm & Sınır Hareketleri:** Uluslararası ziyaretçi giriş/çıkışları, sınır kapısı operasyonel yoğunlukları, turizm gelir/giderleri, otel doluluk ve geceleme oranları, uçuş/havalimanı yolcu sayıları.
- **Göç, İltica & İskân:** Yasal göçmen akışları, iltica/sığınma başvuruları, çalışma izinleri, sınır dışı/alıkoyma operasyonları, zorla yerinden edilme (IDP), göçmen işçi döviz transferleri (remittances).
- **Adli & Bitemporal Prensip:** Veri eksikliği sıfır kabul edilmez (`NULL`, `HISTORICAL_GAP`, `NOT_FOUND`). Kaynaklar yerel bakanlık, sınır muhafaza, göç idaresi ve istatistik kurumlarından doğrudan çekilir.

## 2. Dizin Hiyerarşisi
- `01_RAW_DATA/`: Ham indirmeler (ülke ISO3 kodlu klasörler halinde).
- `02_PROCESSED_DATA/`: Standartlaştırılmış DuckDB/Parquet tabloları (bitemporal `valid_time`, `available_at`).
- `03_METADATA_ATLAS/`: Kurum kayıtları, veri atlası ve eksiklik kütükleri.
- `04_SCRIPTS_HARVESTERS/`: Otomatik veri çekim scriptleri (Python/PowerShell/API harvesters).
- `05_REPORTS_AUDIT/`: Adli veri doğrulama ve denetim raporları.

## 3. Sensör Eşleme ve Zorunlu Metrikler
### Alt Aile 1: Turizm ve Kısa Süreli Sınır Hareketleri (TUR_*)
- `TUR_ARR_TOTAL`: Toplam uluslararası gelen ziyaretçi sayısı (Aylık/Yıllık)
- `TUR_DEP_TOTAL`: Toplam yurt dışına çıkan vatandaş/yabancı sayısı
- `TUR_RECEIPTS_USD`: Turizm gelirleri (Cari USD ve yerel para)
- `TUR_EXP_USD`: Turizm giderleri (Dış seyahat harcamaları)
- `TUR_ACCOMM_OCCUP`: Konaklama tesisleri doluluk oranı (%)
- `TUR_AIR_PAX_INT`: Uluslararası havalimanı yolcu trafiği

### Alt Aile 2: Göç, İltica ve Havale Akışları (MIG_*)
- `MIG_IMM_FLOW`: Ülkeye yasal göçmen girişi (Net / Brüt)
- `MIG_EMM_FLOW`: Ülkeden göç edenler
- `MIG_ASYLUM_APP`: İltica ve sığınma başvurusu sayısı
- `MIG_WORK_PERMIT`: Verilen yabancı çalışma izinleri sayısı
- `MIG_REMIT_IN_USD`: Ülkeye giren işçi dövizi (Remittances received, USD)
- `MIG_REMIT_OUT_USD`: Ülkeden çıkan işçi dövizi (Remittances sent, USD)
- `MIG_BORDER_REFUSALS`: Sınır kapılarından geri çevrilenler / yetkisiz giriş engellemeleri

## 4. İcra Partileri (37 Ülke)
- **Parti 1:** MEX, TUR, COL, ECU, ARG
- **Parti 2:** BRA, CHL, PER, VEN, GTM, HND, SLV, HTI
- **Parti 3:** NGA, AGO, ZAF, KEN, ETH, SDN, COD, MOZ
- **Parti 4:** EGY, TUN, DZA, LBN, IRQ, KAZ, AZE
- **Parti 5:** PAK, BGD, LKA, IND, IDN, PHL, THA, VNM
- **Parti 6:** TBD_37, Kapsam kontrolleri ve boşluk yamaları


## 📈 2. EKONOFİZİKSEL AKTARIM MEKANİZMASI
1. **İşçi Havaleleri (`MIG_REMIT_IN_USD`):** Dış borç ödemeleri ve cari açık krizlerinde merkez bankası rezervlerine giren en esnek nakit akışıdır.
2. **Net Göç (`MIG_NET_MIGRATION`):** Kriz öncesi ve sırasında nitelikli işgücü kaybı (Brain Drain) katsayısını ve kognitif erozyonu doğrudan modeller.
3. **Turizm Gelirleri (`TUR_RECEIPTS_USD`):** Ani duruş (Sudden Stop) fazlarında iç piyasayı ayakta tutan birincil net döviz girdisidir.
