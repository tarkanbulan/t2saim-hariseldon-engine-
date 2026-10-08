# 🏛️ T2SAIM SEKTÖREL KÜTÜPHANE: PİYASALAR, KREDİ DÖNGÜLERİ VE MİKROYAPI
**Mühür:** VERITAS PER SE  
**Konum:** `10_SEKTOREL_VE_TEMATIK_KUTUPHANELER/04_Piyasalar`  
**Rolü:** Bankacılık likiditesi, kaldıraç açığı, Kyle's Lambda ve ani borsa çöküşleri.

---

Evet. **Credit-to-GDP gap, Debt Service Ratio ve Market Stress Indicator hesaplayan; ayrıca tarihsel kriz etiketlerine karşı point-in-time backtest yapabilen Python scriptini yazdım.** Kod, T2SAIM’in Silver bitemporal panelini kullanır; eksik veriyi doldurmaz, gelecekteki veriyi geçmiş hesaplara sızdırmaz ve sonuçları yatırım sinyali değil, analitik risk göstergesi olarak üretir.

Oluşturulan dosyalar:

| Dosya                                  | İşlev                                                        |
| -------------------------------------- | ------------------------------------------------------------ |
| `t2saim_macro_financial_backtester.py` | Credit-to-GDP gap, hanehalkı/firma DSR, market-stress hesaplama ve kriz backtest’i |
| `README_macro_financial_backtester.md` | Metric sözleşmesi, formüller, canonical metric ID’ler ve çalışma komutları |

Kod Python derlemesinden başarıyla geçti.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/ab15c8f7-b23b-4ad1-be79-ac9c8dd751fd/ews_v25_engine.py)][[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/66b8a03a-7615-437e-9915-8e0806b8ad37/t2saim_v25_master_ews_2.py)][[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/156be71c-235c-4593-b762-a0f2d5ee84c4/t2saim_master_ews_v25_engine-2.py)]

## Hesaplanan göstergeler

### 1. Credit-to-GDP gap

Kredi genişlemesinin tarihsel trendinin ne kadar üzerine çıktığını ölçer:

```
CreditGap_t
=
100 \times
\frac{PrivateCredit_t}{NominalGDP_t}
-
Trend_t
```

Trend, iki taraflı ve geleceği gören bir filtreyle değil, **one-sided recursive HP filter** ile hesaplanır:

```
tarih t için trend
=
yalnızca t tarihinde erişilebilir kredi/GSYH geçmişiyle hesaplanan trend
```

Bu kritik: 2018’de 2025 verisini bilerek trend üretmez.

Varsayılan HP parametreleri:

| Frekans   | Varsayılan lambda |
| --------- | ----------------- |
| Quarterly | 400,000           |
| Monthly   | 129,600           |

Credit-to-GDP gap, BIS tarafından aşırı kredi büyümesini ölçmek ve olası bankacılık krizi/ağır finansal stres için erken uyarı göstergesi olarak kullanılan bir ölçüdür.  BIS değerlendirmeleri, kredi/GSYH açığının daha uzun ufukta; debt-service ratio’nun ise daha kısa vadede bankacılık stresi için faydalı olabildiğini belirtir.[[data.bis](https://data.bis.org/topics/CREDIT_GAPS)][[ideas.repec](https://ideas.repec.org/p/bis/biswps/421.html)][[mfw4a](https://www.mfw4a.org/publication/evaluating-early-warning-indicators-banking-crisis-satisfying-policy-requirements)]

### 2. Household Debt Service Ratio

Hanehalkının ana para ve faiz ödemelerinin gelirine oranını tahmin eder:

```
DSR^{HH}_t
=
100 \times
\frac{
Debt^{HH}_t
\times
\left(
EffectiveRate_t
+
\frac{1}{Maturity^{HH}}
\right)
}{
DisposableIncome^{HH}_t
}
```

Varsayılan amortisman vadesi:

```
Hanehalkı: 20 dönem/yıl varsayımı
```

Bu varsayım **açık şekilde outputa yazılır**. Ülke bazında gerçek vade ve itfa verisi bulunursa varsayımı kaldırıp gerçek geri ödeme profili kullanılmalıdır.

### 3. Non-Financial Corporate DSR

Finans dışı firmaların borç servis yükü:

```
DSR^{NFC}_t
=
100 \times
\frac{
Debt^{NFC}_t
\times
\left(
EffectiveRate_t
+
\frac{1}{Maturity^{NFC}}
\right)
}{
NominalGDP_t
}
```

Varsayılan firma amortisman dönemi:

```
12 dönem/yıl
```

Bu, şirket kârı veya EBITDA erişilebilir değilse kullanılan makro oran yaklaşımıdır. Daha iyi ülke adaptöründe payda şu şekilde iyileştirilebilir:

```
firm.debt_service / corporate.gross_operating_surplus
```

veya:

```
firm.debt_service / corporate.cashflow
```

### 4. Market Stress Indicator

Market Stress Indicator, kullanılabilir piyasa bileşenlerinin ülke içi tarihsel bandına göre hesaplanan pozitif stres z-skorlarının ortalamasıdır:

```
MSI_t
=
\frac{1}{N_t}
\sum_{j=1}^{N_t}
\max(0,z_{j,t}^{robust})
```

Burada:

- `N_t`, o tarihte gerçekten mevcut bileşen sayısıdır.
- Olmayan bileşen sıfır yapılmaz.
- Her bileşen ülkenin kendi geçmişine göre normalize edilir.
- Aynı piyasa verisi olmayan ülke “sakin” görünmez; yalnız daha az kapsanmış görünür.

Kullanılan piyasa bileşenleri:

```
market.fx.realized_volatility
market.sovereign.yield_spread
market.sovereign.bid_ask_spread
market.bank.equity_volatility
market.bank.funding_spread
market.equity.drawdown
market.fx.reserves_change
```

## Çalıştırma

Quarterly veri için:

```
python t2saim_macro_financial_backtester.py `
  --root "." `
  --as-of "2026-10-03T00:00:00Z" `
  --frequency quarterly
```

Aylık veri için:

```
python t2saim_macro_financial_backtester.py `
  --root "." `
  --as-of "2026-10-03T00:00:00Z" `
  --frequency monthly
```

Dış kriz registry’sine karşı backtest:

```
python t2saim_macro_financial_backtester.py `
  --root "." `
  --as-of "2026-10-03T00:00:00Z" `
  --frequency quarterly `
  --labels "config/crisis_registry/external_crisis_labels_1996_2026.parquet"
```

Çıktılar:

```
data/gold/macro_financial/
├─ credit_to_gdp_gap_{asof}.parquet
├─ household_dsr_{asof}.parquet
├─ nfc_dsr_{asof}.parquet
├─ market_stress_{asof}.parquet
└─ backtest_credit_gap_{asof}.parquet
```

## Gerekli canonical metric ID’ler

Bu scriptin çalışması için gerçek kaynak serilerini ülke adapter’lerinde şu canonical adlara map etmelisin:

```
macro.private_credit.nominal
macro.gdp.nominal

household.debt.nominal
household.disposable_income.nominal

firm.debt.nominal

money.policy_rate

market.fx.realized_volatility
market.sovereign.yield_spread
market.sovereign.bid_ask_spread
market.bank.equity_volatility
market.bank.funding_spread
market.equity.drawdown
market.fx.reserves_change
```

Ülke prefix’i kullanıyorsanız, örneğin:

```
TUR.macro.private_credit.nominal
TUR.macro.gdp.nominal
TUR.money.policy_rate
```

scriptte bu isimleri parametreyle verirsiniz:

```
python t2saim_macro_financial_backtester.py `
  --root "." `
  --as-of "2026-10-03T00:00:00Z" `
  --credit-metric "TUR.macro.private_credit.nominal" `
  --gdp-metric "TUR.macro.gdp.nominal" `
  --hh-debt-metric "TUR.household.debt.nominal" `
  --rate-metric "TUR.money.policy_rate"
```

Ancak 37 ülke için daha doğru sürüm, country adapter’ın metric alias’ları `macro.private_credit.nominal` gibi global canonical isimlere çevirmesidir. Böylece script her ülke için ayrı parametre istemeden çalışır.

## Riskli piyasa kanalları

Aşağıdaki kanallar, makro-fiskal stresin piyasa fiyatlarına dönüşebileceği ana geçiş mekanizmalarıdır. Bunlar “fiyat kesin böyle gider” iddiası değildir; hangi piyasa verisinin yakından izlenmesi gerektiğini söyler.

| Kanal                             | Başlatan indikatorlar                                        | Piyasa aktarımı                                              | İzlenecek gözlem                                             |
| --------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Kur–rezerv kanalı**             | FX pressure, rezerv kaybı, kısa vadeli dış borç/rezerv, cari açık | Döviz likiditesi ve kur risk primi değişebilir               | Spot/forward kur, implied vol, FX basis, bid-ask             |
| **Egemen borç–faiz kanalı**       | İtfa/gelir, faiz/gelir, ihale maliyeti, FX borç, garanti/PPP | Tahvil getirisi, vade primi ve ihale talebi hassaslaşabilir  | Getiri eğrisi, bid-cover, ihale faizi, CDS, spread, yabancı payı |
| **Banka fonlama kanalı**          | NPL, sermaye, kredi/mevduat, mevduat yavaşlaması, hane/firma DSR | Banka fonlama maliyeti ve kredi marjları etkilenebilir       | Interbank spread, mevduat faizi, banka tahvil spreadi, bank equity vol |
| **Kredi–temerrüt kanalı**         | Credit gap, DSR, firma iflası, ödeme gecikmesi, KOBİ NPL     | Kurumsal risk primi, yeni ihraç koşulu ve kredi arzı hassaslaşabilir | Corporate spread, default rate, issuance volume, lending margin |
| **Enflasyon–faiz eğrisi kanalı**  | TÜFE, gıda/enerji, FX geçişkenliği, mali sübvansiyon baskısı | Politika faizi beklentisi, reel faiz ve nominal eğri yeniden fiyatlanabilir | Breakeven, swap, OIS, tahvil eğrisi, faiz vol                |
| **Hanehalkı–tüketim kanalı**      | Kart gecikmesi, DSR, reel ücret, kira/fatura borcu           | İç talep ve banka varlık kalitesi etkilenebilir              | Perakende satış, tüketici hisseleri, banka hisseleri, tüketici kredi spreadi |
| **PPP/KİT–mali risk kanalı**      | Garanti, PPP ödeme yükü, KİT borcu, kamu bankası kredi riski | Görünmeyen mali risk, egemen spread ve bankacılık bağlantısına geçebilir | Hazine tahvili, KİT tahvili, banka spreadi, bütçe revizyonu  |
| **Likidite–çapraz varlık kanalı** | Birden çok mekanizmanın eş zamanlı akutlaşması               | Piyasa derinliği azalabilir, korelasyonlar yükselip risk iştahı düşebilir | Bid-ask, işlem hacmi, order-book depth, fon akımı, cross-asset correlation |
| **Dış ticaret–emtia kanalı**      | Enerji fiyatı, ihracat düşüşü, navlun, ithalat maliyeti      | Cari denge, enflasyon ve şirket nakit akışı üzerinden etkiler | Emtia futures, shipping cost, FX, sektör hisseleri, trade-credit göstergeleri |
| **Politika güvenilirliği kanalı** | Bütçe tahmin hatası, şeffaflık düşüşü, ani düzenleme, veri revizyonu | Risk primi ve piyasa likiditesi değişebilir                  | Tahvil spreadi, kur volatilitesi, ihale katılımı, sermaye akımı |

## Backtest mantığı

Backtester, her dış kriz etiketi için örneğin 1–12 ay öncesine bakar:

```
Krizin başlangıcı: 2001-02
İncelenen lead window: 2000-02 → 2001-01
Credit gap eşik üstüne çıktı mı?
İlk alarm hangi tarihte geldi?
Krizden kaç ay önce alarm verdi?
```

Çıktı:

```
episode_id
country_iso3
episode_type
start_date
indicator
threshold
alerted
first_alert_date
lead_months
```

Bu sayede her indikator için:

```
Precision,\ Recall,\ NoiseToSignal,\ MedianLeadTime
```

hesaplanabilir.

## Kritik sınırlar

- Credit-to-GDP gap yalnız güvenilir nominal kredi ve nominal GSYH tanımı varsa anlamlıdır.
- DSR’de gerçek ana para itfa planı yoksa kullanılan amortisman varsayımı raporda açıkça kalmalıdır.
- Market Stress Indicator, eksik piyasa bileşenini sıfır saymaz; `active_market_components` sayısını mutlaka raporlar.
- Piyasa serilerinin lisans ve kullanım şartları ülke/sağlayıcı bazında kontrol edilmelidir.
- Eşikler, tüm ülkelerde sabitlenmemeli; 1996–2026 kriz registry’si üzerinde ülke ve kriz-türü bazında walk-forward test ile kalibre edilmelidir.
- Bu sistem piyasa **analizi** üretir; otomatik işlem, yatırım tavsiyesi veya fiyat tahmini üretmez.

---

# T2SAIM Market Transmission Engine

Maps verified macro/fiscal/structural stress patterns into **market-sensitive
transmission channels**. It provides a transparent analytical watchlist, not
trading signals or predictions.

## Design boundary

- A `watch`, `acute`, or `extreme` result means a pre-defined macro-financial
  pattern is present.
- It does **not** mean a market must move in one direction.
- It does **not** provide investment advice, price targets, or causal attribution.
- Actual market price, volatility, liquidity and spread data should be collected
  as a separate verified market-data layer, then evaluated against this layer.

## Run

```bash
python t2saim_market_transmission_engine.py \
  --root . \
  --as-of 2026-10-03T00:00:00Z
```

## Outputs

- `market_channel_findings_*.parquet`
- `market_evidence_links_*.parquet`
- `country_market_watch_*.csv`

Every output links back to mechanism findings and then to original Silver
source hashes and URLs.


## ⚡ 3. PİYASA MİKROYAPISI VE LİKİDİTE ŞOKU DENKLEMLERİ
1. **Kyle's Lambda (Fiyat Etkisi):**
   $$\lambda = \frac{Cov(\Delta P, Q)}{Var(Q)}$$
   Likidite kuruduğunda $\lambda$ fırlar; küçük bir satış emri ($Q$) devasa fiyat çöküşlerine ($\Delta P$) yol açar.
2. **BIS Kredi/GSYİH Açığı (Basel III Buffer):**
   Trendden sapma $> %10$ olduğunda bankacılık krizi ihtimali %80'in üzerine çıkar.
