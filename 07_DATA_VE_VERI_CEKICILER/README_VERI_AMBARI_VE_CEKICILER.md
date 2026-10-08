# T2SAIM CORE-20 KANONİK VERİ AMBARI VE ÇEKİCİLER (07_DATA_VE_VERI_CEKICILER)

Bu dizin, T2SAIM Erken Uyarı Sistemi (EWS) ve Core-20 Kokpit Platformu'nun dayandığı **yalnızca fiilen kullanılan ve fiziksel kanıt niteliği taşıyan** birincil veri tabanlarını içerir. Eski, kullanılmayan veya 37 ülkelik deneme CSV'leri ana arşivde muhafaza edilmiş, bu operasyonel kaleye yalnızca filtrelenmiş Core-20 kanonik veri setleri aktarılmıştır.

## 📊 KANONİK VERİ AMBARI ENVANTERİ (MUTLAK KANIT MÜHRÜ)

| Dosya Adı | Boyut (Byte) | SHA-256 (İlk 16 Hane) | Birincil Kaynak Yolu | Açıklama ve Model Rolü |
| :--- | :--- | :--- | :--- | :--- |
| anking_stress_observations.csv | 1,730,125 | a5f79228fc0cc3cb | REAL_EVIDENCE_CORE20/silver/ | 20 ülkenin bankacılık stres ve sistemik likidite gözlemleri (Bank Run, NPL, Sermaye Yeterliliği). |
| ml_observations.csv | 1,151,687 | c8a7f7ecc887728b | REAL_EVIDENCE_CORE20/silver/ | Kara para aklama, sermaye kaçışı ve gri liste adli gözlemleri (FATF, Basel AML). |
| harm_observations.csv | 482,285 | fcec81bf69fef2ff | REAL_EVIDENCE_CORE20/silver/ | Hanehalkı ve reel sektör hasar/çöküş dinamikleri (Satın alma gücü erozyonu, iflaslar). |
| 	2saim_evidence_core20.duckdb | 1,060,864 | e1873ec3d1ac0c51 | REAL_EVIDENCE_CORE20/ | Core-20 analitik kanıt veri tabanı (Bitemporal Point-in-Time DuckDB motoru). |
| country_market_watch_20261003T000000Z.csv | 39,930 | 634bfb4609c2e075 | data/gold/market_transmission/ | Ulusal borsa, FX, CDS ve tahvil piyasa aktarım kanalları izleme verisi. |
| country_mechanism_summary_20261003T000000Z.csv | 142,842 | ae71aced5dd412a9 | data/gold/mechanism_engine/ | 88 formüllü mekanizma motorunun ülke bazlı kriz tetikleyici özet tablosu. |

## 🛡️ SIFIR SENTETİK VERİ VE ARŞİV KORUMA PROTOKOLÜ
1. Hiçbir veri sentetik veya uydurma değildir ([VERIFIED]).
2. Orijinal kaynak dosyaları E:\Tarkan_Analiz\New_Page_Ews hiyerarşisinde güvenle korunmaktadır; hiçbir orijinal dosya silinmemiştir.
3. Kokpit ve model bu kanonik tablolardan beslenir.
