# 🏛️ T2SAIM SEKTÖREL KÜTÜPHANE: ULAŞTIRMA, TAŞIMACILIK VE FİZİKSEL LOJİSTİK
**Mühür:** VERITAS PER SE  
**Konum:** `10_SEKTOREL_VE_TEMATIK_KUTUPHANELER/06_Ulastirma_Transport`  
**Rolü:** Fiziksel ekonomi telemetrisi; para piyasalarından önce kriz sinyali veren lojistik akışlar.

---

Bu PDF, 37 ülke × 30 yıl için kuracağımız sektör bazlı CCI/CLI katmanına güçlü bir metodolojik temel sağlıyor. Özellikle ulaştırma sektöründe fiziksel çıktı, reel bordro, reel tüketim ve istihdamın ortak çevrim hareketi; Harding–Pagan concordance, Stock–Watson dinamik faktör ve Kim–Nelson rejim değişimiyle birlikte ele alınıyor.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/e3b5ffae-0dbb-43b2-a417-5303b12050db/CONTRIBUTIONS_TO_ECONOMIC_ANALYSISTRA_z_library_sk-_1lib_sk.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=ASIA2F3EMEYE5NO54L36%2F20261003%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261003T223853Z&X-Amz-Expires=1536&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGYYzZmruXWC3WnvQsVS73NmBmjE6nwRF5lm7lW5dA7hAiBr56fhafs2kuhvVlii4VHmhVlWjyoq0FkinJlhCFftoCqJBQi3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDY5OTc1MzMwOTcwNSIMHDG6tiV8zzZYwgF%2FKt0EMq9IYs3MObp5DlJE7SiS08ln1S2n1bGK9s1PaAN6WTh2Tlx%2FFm1bnZhhomZBThLIAMgrAJ6kGDsCAheas7mTsXFyFBjXmT59GCQyp2QNukvfGyQr3GBH%2Fyxd38v4NKMxPTC72YoIhZPen4mj85ppSm%2BXle61u%2BPZ%2BGFr4Dsy3H10XvzHW4qPcaOf6crVZhspiW7jfpR%2FEQ5Co70zwRv4PsWwZgxXEofT1h5aZqsn0mRPdQcAoxBEiV62DBP%2BvR44PW68TyVkADWoDPJx0zcPN6iZziiDJ8eb4kQwFrKOJ2Azepa%2BLIvmVM4KzXmrIJbo9bhMcQ4fr5TaH%2FR5P2L21QtXuXQuvtO1YHeQmJtjzHoPcuok%2Fh33fZYFIk%2FKlyG0so6MvuyqjvsVoDOVTiz9vj1VGw%2B%2Bq59SLkU53UBtzkymfPODa3AHr%2BeS8%2BrUQO4Ho9a50Da7i1xn0rDJGoi5VKeT7gOEF1VLpLuygnfMsLtaSLPUscSeGbSQmxKcyBcjzAR5CTPgsMAV65jMnGhv57M0s0BgcSnYnCrk6sDHVDeD31RluAh2Vw7S2tdJEGlT0ECy0KpeF2qvZSsIQh%2B5%2BBsMC62ce%2FMsg3TpBX08cSsm2NuYw4GQ5Rerre%2B7wnIEuic7GdZ%2Fkgd48ip0oVY3NZEmuzR22P5fDcQ2WNPFdqkPB3khKz%2BBRNb6JYk9PbgCB6jvLtt5%2BLohTzJAOOC2eVxOrz3%2F951QJbX2lHS4hFdw9jecM7nDd3JAwEzJEn%2F6ytUNp5fd6p7W0ms07UQYHKvk0mbfr3XWNiZ65AkwqviF1gY6mQE0i3RGj2UjUdPpSOCjYn6GBfkFVcYVpHgLRxiXKBrZ0xEorNr2PFTf7XIbtOR1RqjJBzeiBvle7PLb3j6v8AxhdVEmrr2TJiZtsmOGlLxNf9RlskgIEZsyPmE10v7uEyGRJ3UBbLw%2F%2FJtU7793qo63GuWAVlnJ2fMdIbAjcEcUJcIOzVWwMXtgW6TwjeUxmuIlkIxk1%2BewsUg%3D&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=8d496df441e60facab6bf12d078411f59841de06600a7e4cad8bead95e8e2215)]

Aşağıdaki çerçeve ve kod, bu yöntemi T2SAIM’de **gerçek veri zorunluluğuyla** 37 ülkeye uyarlamak içindir.

## Teorik çerçeve

### Temel hipotez

Her ülkede sektör çevrimi, tek bir seriden değil; aynı ekonomik aktiviteyi farklı kanallardan ölçen serilerin ortak hareketinden çıkarılır:

```
\text{Sektörel Aktivite}_t
=
f(
\text{output},
\text{income/payroll},
\text{consumption/sales},
\text{employment},
\text{investment},
\text{credit},
\text{trade/logistics}
)
```

Ulaştırma örneğinde PDF şu dört eşzamanlı seriyle çalışıyor:

```
Fiziksel ulaştırma çıktısı
Reel ulaştırma bordrosu
Reel ulaştırma hizmet tüketimi
Ulaştırma sektörü istihdamı
```

Kaynak, bu dört serinin turning point çevrimlerinin güçlü biçimde senkronize olduğunu; ikili concordance değerlerinin yaklaşık 0.8–0.9 aralığında olduğunu bildiriyor. Aynı çalışmada CCI için NBER tipi bileşik endeks, Stock–Watson dinamik faktör modeli ve Kim–Nelson Markov-switching yaklaşımı karşılaştırılıyor.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/e3b5ffae-0dbb-43b2-a417-5303b12050db/CONTRIBUTIONS_TO_ECONOMIC_ANALYSISTRA_z_library_sk-_1lib_sk.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=ASIA2F3EMEYE5NO54L36%2F20261003%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261003T223853Z&X-Amz-Expires=1536&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGYYzZmruXWC3WnvQsVS73NmBmjE6nwRF5lm7lW5dA7hAiBr56fhafs2kuhvVlii4VHmhVlWjyoq0FkinJlhCFftoCqJBQi3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDY5OTc1MzMwOTcwNSIMHDG6tiV8zzZYwgF%2FKt0EMq9IYs3MObp5DlJE7SiS08ln1S2n1bGK9s1PaAN6WTh2Tlx%2FFm1bnZhhomZBThLIAMgrAJ6kGDsCAheas7mTsXFyFBjXmT59GCQyp2QNukvfGyQr3GBH%2Fyxd38v4NKMxPTC72YoIhZPen4mj85ppSm%2BXle61u%2BPZ%2BGFr4Dsy3H10XvzHW4qPcaOf6crVZhspiW7jfpR%2FEQ5Co70zwRv4PsWwZgxXEofT1h5aZqsn0mRPdQcAoxBEiV62DBP%2BvR44PW68TyVkADWoDPJx0zcPN6iZziiDJ8eb4kQwFrKOJ2Azepa%2BLIvmVM4KzXmrIJbo9bhMcQ4fr5TaH%2FR5P2L21QtXuXQuvtO1YHeQmJtjzHoPcuok%2Fh33fZYFIk%2FKlyG0so6MvuyqjvsVoDOVTiz9vj1VGw%2B%2Bq59SLkU53UBtzkymfPODa3AHr%2BeS8%2BrUQO4Ho9a50Da7i1xn0rDJGoi5VKeT7gOEF1VLpLuygnfMsLtaSLPUscSeGbSQmxKcyBcjzAR5CTPgsMAV65jMnGhv57M0s0BgcSnYnCrk6sDHVDeD31RluAh2Vw7S2tdJEGlT0ECy0KpeF2qvZSsIQh%2B5%2BBsMC62ce%2FMsg3TpBX08cSsm2NuYw4GQ5Rerre%2B7wnIEuic7GdZ%2Fkgd48ip0oVY3NZEmuzR22P5fDcQ2WNPFdqkPB3khKz%2BBRNb6JYk9PbgCB6jvLtt5%2BLohTzJAOOC2eVxOrz3%2F951QJbX2lHS4hFdw9jecM7nDd3JAwEzJEn%2F6ytUNp5fd6p7W0ms07UQYHKvk0mbfr3XWNiZ65AkwqviF1gY6mQE0i3RGj2UjUdPpSOCjYn6GBfkFVcYVpHgLRxiXKBrZ0xEorNr2PFTf7XIbtOR1RqjJBzeiBvle7PLb3j6v8AxhdVEmrr2TJiZtsmOGlLxNf9RlskgIEZsyPmE10v7uEyGRJ3UBbLw%2F%2FJtU7793qo63GuWAVlnJ2fMdIbAjcEcUJcIOzVWwMXtgW6TwjeUxmuIlkIxk1%2BewsUg%3D&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=8d496df441e60facab6bf12d078411f59841de06600a7e4cad8bead95e8e2215)]

### 37 ülkeye uyarlama

Aynı seri isimlerini bütün ülkelere zorla kullanmayacağız. Bunun yerine her ülke için gerçek yerel resmi eşdeğerler bulunacak:

| Global canonical seri         | Yerel resmi eşdeğer                                          |
| ----------------------------- | ------------------------------------------------------------ |
| `transport.output.real_index` | Ulaştırma/depolama üretim endeksi, yük ton-km, yolcu-km, lojistik output endeksi |
| `transport.payroll.real`      | Ulaştırma sektör ücret/bordro endeksi, işgücü maliyeti veya reel ücret toplamı |
| `transport.consumption.real`  | Ulaştırma hizmetleri reel tüketimi, ulaştırma harcaması veya yolcu geliri |
| `transport.employment.total`  | Ulaştırma/depolama sektörü istihdamı                         |
| `transport.investment.real`   | Araç, filo, lojistik tesis veya ulaştırma ekipmanı yatırımı  |
| `transport.trade_flow.real`   | Liman, demiryolu, hava kargo, konteyner, navlun, sınır geçişi |

Ülkede güvenilir “reel tüketim” serisi yoksa bunu sentetik hesaplamayacağız. `UNOBSERVED` kalacak. Model en az üç ayrı gerçek seriyle çalışabilir; ancak dört seri yoksa veri yeterliliği rapora yazılır.

## CCI metodolojisi

### 1. Veri dönüşümü

Her seri için:

```
- Mevsimsellikten arındırılmış olmalı veya kaynakta bu açıkça belirtilmeli.
- Nominal gelir/bordro/harcama serileri, yalnız gerçek resmi deflatör varsa reel hale getirilmeli.
- Ham seviye yerine log fark ya da büyüme oranı kullanılmalı.
- Eksik tarih sentetik olarak oluşturulmamalı.
- Revizyon ve release tarihleri available_at alanında tutulmalı.
```

Temel dönüşüm:

```
g_{i,t} = 100 \times [\ln(X_{i,t}) - \ln(X_{i,t-1})]
```

### 2. Harding–Pagan concordance

Her seri için Bry–Boschan turning-point algoritmasıyla veya açıkça tanımlanmış bir faz kuralıyla:

```
S_{i,t}
=
\begin{cases}
1, & \text{genişleme}\\
0, & \text{daralma}
\end{cases}
```

İki seri arasındaki uyum:

```
I_{xy}
=
\frac{1}{T}
\sum_{t=1}^{T}
[
S_{x,t}S_{y,t}
+
(1-S_{x,t})(1-S_{y,t})
]
```

Bu endeks 0–1 arasındadır. PDF’de, ulaştırma eşzamanlı serileri için `I` değerleri yaklaşık 0.8–0.9 aralığında bulunuyor; bu, ortak çevrim için güçlü eş-hareket kanıtı olarak yorumlanıyor.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/e3b5ffae-0dbb-43b2-a417-5303b12050db/CONTRIBUTIONS_TO_ECONOMIC_ANALYSISTRA_z_library_sk-_1lib_sk.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=ASIA2F3EMEYE5NO54L36%2F20261003%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261003T223853Z&X-Amz-Expires=1536&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGYYzZmruXWC3WnvQsVS73NmBmjE6nwRF5lm7lW5dA7hAiBr56fhafs2kuhvVlii4VHmhVlWjyoq0FkinJlhCFftoCqJBQi3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDY5OTc1MzMwOTcwNSIMHDG6tiV8zzZYwgF%2FKt0EMq9IYs3MObp5DlJE7SiS08ln1S2n1bGK9s1PaAN6WTh2Tlx%2FFm1bnZhhomZBThLIAMgrAJ6kGDsCAheas7mTsXFyFBjXmT59GCQyp2QNukvfGyQr3GBH%2Fyxd38v4NKMxPTC72YoIhZPen4mj85ppSm%2BXle61u%2BPZ%2BGFr4Dsy3H10XvzHW4qPcaOf6crVZhspiW7jfpR%2FEQ5Co70zwRv4PsWwZgxXEofT1h5aZqsn0mRPdQcAoxBEiV62DBP%2BvR44PW68TyVkADWoDPJx0zcPN6iZziiDJ8eb4kQwFrKOJ2Azepa%2BLIvmVM4KzXmrIJbo9bhMcQ4fr5TaH%2FR5P2L21QtXuXQuvtO1YHeQmJtjzHoPcuok%2Fh33fZYFIk%2FKlyG0so6MvuyqjvsVoDOVTiz9vj1VGw%2B%2Bq59SLkU53UBtzkymfPODa3AHr%2BeS8%2BrUQO4Ho9a50Da7i1xn0rDJGoi5VKeT7gOEF1VLpLuygnfMsLtaSLPUscSeGbSQmxKcyBcjzAR5CTPgsMAV65jMnGhv57M0s0BgcSnYnCrk6sDHVDeD31RluAh2Vw7S2tdJEGlT0ECy0KpeF2qvZSsIQh%2B5%2BBsMC62ce%2FMsg3TpBX08cSsm2NuYw4GQ5Rerre%2B7wnIEuic7GdZ%2Fkgd48ip0oVY3NZEmuzR22P5fDcQ2WNPFdqkPB3khKz%2BBRNb6JYk9PbgCB6jvLtt5%2BLohTzJAOOC2eVxOrz3%2F951QJbX2lHS4hFdw9jecM7nDd3JAwEzJEn%2F6ytUNp5fd6p7W0ms07UQYHKvk0mbfr3XWNiZ65AkwqviF1gY6mQE0i3RGj2UjUdPpSOCjYn6GBfkFVcYVpHgLRxiXKBrZ0xEorNr2PFTf7XIbtOR1RqjJBzeiBvle7PLb3j6v8AxhdVEmrr2TJiZtsmOGlLxNf9RlskgIEZsyPmE10v7uEyGRJ3UBbLw%2F%2FJtU7793qo63GuWAVlnJ2fMdIbAjcEcUJcIOzVWwMXtgW6TwjeUxmuIlkIxk1%2BewsUg%3D&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=8d496df441e60facab6bf12d078411f59841de06600a7e4cad8bead95e8e2215)]

### 3. Stock–Watson dinamik faktör

```
y_{i,t} = \lambda_i F_t + \epsilon_{i,t}
F_t = \phi_1 F_{t-1} + \phi_2 F_{t-2} + u_t
```

- `y_{i,t}`: sektörün standardize edilmiş gerçek büyüme serileri.
- `F_t`: sektörün ortak gizil aktivite faktörü.
- `\lambda_i`: her gözlemin ortak faktöre yükü.
- `\epsilon_{i,t}`: seri-spesifik şoklar.

Kaynak, state-space biçimindeki bu modellerin Kalman filtresi ile tahmin edildiğini; Kim–Nelson modelinin ise aynı faktöre Markov rejim geçişi eklediğini anlatıyor.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/e3b5ffae-0dbb-43b2-a417-5303b12050db/CONTRIBUTIONS_TO_ECONOMIC_ANALYSISTRA_z_library_sk-_1lib_sk.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=ASIA2F3EMEYE5NO54L36%2F20261003%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261003T223853Z&X-Amz-Expires=1536&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGYYzZmruXWC3WnvQsVS73NmBmjE6nwRF5lm7lW5dA7hAiBr56fhafs2kuhvVlii4VHmhVlWjyoq0FkinJlhCFftoCqJBQi3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDY5OTc1MzMwOTcwNSIMHDG6tiV8zzZYwgF%2FKt0EMq9IYs3MObp5DlJE7SiS08ln1S2n1bGK9s1PaAN6WTh2Tlx%2FFm1bnZhhomZBThLIAMgrAJ6kGDsCAheas7mTsXFyFBjXmT59GCQyp2QNukvfGyQr3GBH%2Fyxd38v4NKMxPTC72YoIhZPen4mj85ppSm%2BXle61u%2BPZ%2BGFr4Dsy3H10XvzHW4qPcaOf6crVZhspiW7jfpR%2FEQ5Co70zwRv4PsWwZgxXEofT1h5aZqsn0mRPdQcAoxBEiV62DBP%2BvR44PW68TyVkADWoDPJx0zcPN6iZziiDJ8eb4kQwFrKOJ2Azepa%2BLIvmVM4KzXmrIJbo9bhMcQ4fr5TaH%2FR5P2L21QtXuXQuvtO1YHeQmJtjzHoPcuok%2Fh33fZYFIk%2FKlyG0so6MvuyqjvsVoDOVTiz9vj1VGw%2B%2Bq59SLkU53UBtzkymfPODa3AHr%2BeS8%2BrUQO4Ho9a50Da7i1xn0rDJGoi5VKeT7gOEF1VLpLuygnfMsLtaSLPUscSeGbSQmxKcyBcjzAR5CTPgsMAV65jMnGhv57M0s0BgcSnYnCrk6sDHVDeD31RluAh2Vw7S2tdJEGlT0ECy0KpeF2qvZSsIQh%2B5%2BBsMC62ce%2FMsg3TpBX08cSsm2NuYw4GQ5Rerre%2B7wnIEuic7GdZ%2Fkgd48ip0oVY3NZEmuzR22P5fDcQ2WNPFdqkPB3khKz%2BBRNb6JYk9PbgCB6jvLtt5%2BLohTzJAOOC2eVxOrz3%2F951QJbX2lHS4hFdw9jecM7nDd3JAwEzJEn%2F6ytUNp5fd6p7W0ms07UQYHKvk0mbfr3XWNiZ65AkwqviF1gY6mQE0i3RGj2UjUdPpSOCjYn6GBfkFVcYVpHgLRxiXKBrZ0xEorNr2PFTf7XIbtOR1RqjJBzeiBvle7PLb3j6v8AxhdVEmrr2TJiZtsmOGlLxNf9RlskgIEZsyPmE10v7uEyGRJ3UBbLw%2F%2FJtU7793qo63GuWAVlnJ2fMdIbAjcEcUJcIOzVWwMXtgW6TwjeUxmuIlkIxk1%2BewsUg%3D&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=8d496df441e60facab6bf12d078411f59841de06600a7e4cad8bead95e8e2215)]

### 4. Kim–Nelson rejim modeli

```
F_t = \mu_{S_t} + \phi_1 F_{t-1} + \phi_2 F_{t-2} + u_t
S_t \in \{0,1\}
P(S_t=0 \mid S_{t-1}=0)=p_{00}
P(S_t=1 \mid S_{t-1}=1)=p_{11}
```

Rejim olasılığı:

```
P(recession_t | gerçek sektör verileri)
```

T2SAIM’de şu şekilde kullanılır:

```
P(daralma) < 0.30       → normal
0.30–0.50               → watch
0.50–0.70               → elevated
0.70–0.85               → acute
> 0.85                  → severe sector contraction candidate
```

Bu eşikler başlangıç parametresidir; her ülkenin gerçek kriz registry’siyle walk-forward backtest sonrası kalibre edilir.

## 37 ülke için sektör şeması

```
production/
├─ manufacturing
├─ construction
├─ transport_logistics
├─ agriculture
├─ mining
├─ energy
├─ trade_tourism
├─ ICT
└─ financial_services

structural/
├─ investment
├─ employment
├─ wages
├─ productivity
├─ export_dependency
├─ import_input_dependency
├─ energy_dependency
├─ logistics_capacity
└─ public_investment_execution
```

Her sektör için temel CCI dört seriden üretilebilir:

```
1. Real output / activity
2. Employment
3. Real income, wages, payroll or sales
4. Investment, orders, consumption, exports or capacity use
```

## Gerçek veri indirme sözleşmesi

Her ülke için aşağıdaki gibi gerçek Source Atlas kaydı gerekir:

```
sources:
  - source_id: "TUR_TURKSTAT_TRANSPORT_EMPLOYMENT"
    country_iso3: "TUR"
    enabled: false
    status: "UNVERIFIED"

    institution: "Türkiye İstatistik Kurumu"
    source_page_url: "GERÇEK_RESMI_KAYNAK_SAYFASI"
    url: "GERÇEK_DOĞRUDAN_API_CSV_XLSX_ENDPOINT"

    format: "csv"
    metric_id: "TUR.transport.employment.total"
    unit: "persons"
    frequency: "monthly"

    mapping:
      value: "GERÇEK_DEĞER_KOLONU"
      valid_time: "GERÇEK_TARİH_KOLONU"

    download_strategy:
      type: "chunked_api"
      chunk_days: 365
```

Gerçek endpoint, gerçek kolon ve gerçek resmi kaynak doğrulanmadan `enabled: true` yapılmaz.

## Python: sektör CCI / CLI hesaplayıcı

Aşağıdaki script, daha önce indirdiğiniz gerçek Silver paneli okur. Veri indirme işlemi yapmaz; indirilmiş ve hash’lenmiş gerçek veriden CCI/CLI hesaplar.

Dosya adı:

```
t2saim_sector_cycle_engine.py
# -*- coding: utf-8 -*-
"""
T2SAIM Sector Cycle Engine

Creates country-specific sector CCI / CLI metrics from real source-lineaged
Silver observations.

No synthetic observations.
No zero-fill.
No interpolation.
No forward-fill.
No guessed country equivalents.
No causal attribution.

Methods:
- log growth / standardisation
- simple turning-point phase labels
- Harding-Pagan concordance
- PCA common factor as baseline CCI
- leading indicator cross-correlation screening

For full Stock-Watson / Kim-Nelson Bayesian estimation, use this engine's
clean prepared panel as input to a separately validated state-space/MCMC module.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def to_utc(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def latest_as_of(observations: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    x = observations.copy()

    for col in ["valid_time", "available_at", "retrieved_at"]:
        x[col] = pd.to_datetime(x[col], errors="coerce", utc=True)

    x = x[
        x["valid_time"].notna()
        & x["available_at"].notna()
        & (x["available_at"] <= as_of)
        & x["value"].notna()
    ].copy()

    x = x.sort_values(
        [
            "country_iso3",
            "geo_id",
            "metric_id",
            "valid_time",
            "available_at",
            "retrieved_at",
        ]
    )

    return x.groupby(
        ["country_iso3", "geo_id", "metric_id", "valid_time"],
        as_index=False,
    ).tail(1)


def log_growth(series: pd.Series) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")

    # Log transformation only valid for positive real activity measures.
    x = x.where(x > 0)

    return 100 * (np.log(x) - np.log(x.shift(1)))


def phase_from_growth(growth: pd.Series) -> pd.Series:
    """
    Conservative binary phase proxy.
    1 = non-negative growth/expansion
    0 = negative growth/contraction

    Production use should replace this with a validated Bry-Boschan routine.
    """
    return pd.Series(
        np.where(growth.notna(), np.where(growth >= 0, 1, 0), np.nan),
        index=growth.index,
    )


def concordance(a: pd.Series, b: pd.Series) -> float | None:
    pair = pd.concat([a, b], axis=1).dropna()

    if len(pair) < 24:
        return None

    x = pair.iloc[:, 0]
    y = pair.iloc[:, 1]

    value = ((x * y) + ((1 - x) * (1 - y))).mean()
    return float(value)


def extract_country_metric_panel(
    observations: pd.DataFrame,
    country: str,
    metric_ids: list[str],
) -> pd.DataFrame:
    x = observations[
        (observations["country_iso3"] == country)
        & (observations["metric_id"].isin(metric_ids))
    ].copy()

    if x.empty:
        return pd.DataFrame()

    panel = x.pivot_table(
        index="valid_time",
        columns="metric_id",
        values="value",
        aggfunc="last",
    ).sort_index()

    return panel


def compute_cci(
    panel: pd.DataFrame,
    min_components: int,
) -> tuple[pd.DataFrame, dict]:
    growth = panel.apply(log_growth)

    complete = growth.dropna(axis=0, thresh=min_components).copy()

    if complete.empty or complete.shape[1] < min_components:
        return pd.DataFrame(), {
            "status": "INSUFFICIENT_REAL_DATA",
            "reason": "Not enough overlapping real component observations.",
        }

    # Do NOT fill missing values. Keep only dates with all selected components.
    strict = complete.dropna()

    if len(strict) < 24:
        return pd.DataFrame(), {
            "status": "INSUFFICIENT_OVERLAP",
            "reason": "Fewer than 24 complete real observations.",
        }

    scaler = StandardScaler()
    z = scaler.fit_transform(strict)

    pca = PCA(n_components=1)
    factor = pca.fit_transform(z).ravel()

    output = pd.DataFrame(
        {
            "valid_time": strict.index,
            "cci_factor": factor,
            "cci_explained_variance": pca.explained_variance_ratio_[0],
            "component_count": strict.shape[1],
        }
    )

    return output, {
        "status": "OK",
        "observations": int(len(strict)),
        "components": list(strict.columns),
        "explained_variance": float(pca.explained_variance_ratio_[0]),
        "loadings": {
            metric: float(loading)
            for metric, loading in zip(strict.columns, pca.components_[0])
        },
    }


def compute_concordance_table(panel: pd.DataFrame) -> pd.DataFrame:
    growth = panel.apply(log_growth)
    phases = growth.apply(phase_from_growth)

    rows = []
    cols = list(phases.columns)

    for i, left in enumerate(cols):
        for right in cols[i + 1 :]:
            rows.append(
                {
                    "metric_left": left,
                    "metric_right": right,
                    "concordance": concordance(
                        phases[left],
                        phases[right],
                    ),
                }
            )

    return pd.DataFrame(rows)


def lead_lag_screen(
    cci: pd.DataFrame,
    leading_panel: pd.DataFrame,
    max_lead_months: int,
) -> pd.DataFrame:
    if cci.empty or leading_panel.empty:
        return pd.DataFrame()

    target = cci.set_index("valid_time")["cci_factor"]

    rows = []

    for metric in leading_panel.columns:
        growth = log_growth(leading_panel[metric])

        for lead in range(1, max_lead_months + 1):
            aligned = pd.concat(
                [
                    target,
                    growth.shift(lead).rename("leading"),
                ],
                axis=1,
            ).dropna()

            if len(aligned) < 24:
                continue

            rows.append(
                {
                    "leading_metric_id": metric,
                    "lead_months": lead,
                    "observations": len(aligned),
                    "correlation_with_future_cci": aligned.corr().iloc[0, 1],
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--sector-config",
        default="config/sector_cycles/sector_cycle_contract.yaml",
    )
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--countries", nargs="*")
    parser.add_argument("--max-lead-months", type=int, default=12)
    args = parser.parse_args()

    root = Path(args.root)
    as_of = to_utc(args.as_of)

    config = load_yaml(root / args.sector_config)

    observations = pd.read_parquet(
        root / "data" / "silver" / "observations.parquet"
    )
    observations = latest_as_of(observations, as_of)

    out_dir = root / "data" / "gold" / "sector_cycles"
    ensure_dir(out_dir)

    countries = (
        args.countries
        if args.countries
        else sorted(observations["country_iso3"].dropna().unique())
    )

    report_rows = []

    for country in countries:
        for sector in config.get("sectors", []):
            sector_id = sector["sector_id"]

            cci_metrics = sector["coincident_metrics"]
            cli_metrics = sector.get("leading_metrics", [])
            min_components = int(sector.get("min_real_components", 3))

            cci_panel = extract_country_metric_panel(
                observations,
                country,
                cci_metrics,
            )

            cci, metadata = compute_cci(
                cci_panel,
                min_components=min_components,
            )

            concordance_table = compute_concordance_table(cci_panel)

            cli_panel = extract_country_metric_panel(
                observations,
                country,
                cli_metrics,
            )

            lead_lag = lead_lag_screen(
                cci,
                cli_panel,
                max_lead_months=args.max_lead_months,
            )

            tag = as_of.strftime("%Y%m%dT%H%M%SZ")
            prefix = f"{country}_{sector_id}_{tag}"

            if not cci.empty:
                cci.assign(
                    country_iso3=country,
                    sector_id=sector_id,
                    evidence_status="MODEL_DERIVED_FROM_VERIFIED_OBSERVATIONS",
                ).to_parquet(
                    out_dir / f"{prefix}_cci.parquet",
                    index=False,
                )

            if not concordance_table.empty:
                concordance_table.assign(
                    country_iso3=country,
                    sector_id=sector_id,
                ).to_csv(
                    out_dir / f"{prefix}_concordance.csv",
                    index=False,
                )

            if not lead_lag.empty:
                lead_lag.assign(
                    country_iso3=country,
                    sector_id=sector_id,
                ).to_csv(
                    out_dir / f"{prefix}_lead_lag.csv",
                    index=False,
                )

            report_rows.append(
                {
                    "country_iso3": country,
                    "sector_id": sector_id,
                    "status": metadata.get("status"),
                    "observations": metadata.get("observations"),
                    "components": "|".join(metadata.get("components", [])),
                    "explained_variance": metadata.get("explained_variance"),
                    "loadings_json": json.dumps(
                        metadata.get("loadings", {}),
                        ensure_ascii=False,
                    ),
                    "as_of": as_of,
                    "synthetic_data_used": False,
                    "imputation_used": False,
                    "zero_fill_used": False,
                }
            )

    summary = pd.DataFrame(report_rows)

    summary.to_parquet(
        out_dir / f"sector_cycle_summary_{as_of.strftime('%Y%m%dT%H%M%SZ')}.parquet",
        index=False,
    )

    print(
        json.dumps(
            {
                "countries": len(countries),
                "sector_runs": len(report_rows),
                "output_dir": str(out_dir),
                "synthetic_data_used": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
```

## Sektör sözleşmesi

Dosya:

```
config/sector_cycles/sector_cycle_contract.yaml
# Real-data-only sector cycle contract.
#
# Every metric must be present in the Silver panel with source lineage.
# Missing metrics remain missing. The engine requires at least 3 real
# overlapping coincident components.

sectors:

  - sector_id: transport_logistics

    coincident_metrics:
      - "{ISO3}.transport.output.real_index"
      - "{ISO3}.transport.payroll.real"
      - "{ISO3}.transport.consumption.real"
      - "{ISO3}.transport.employment.total"

    leading_metrics:
      - "{ISO3}.market.transport_equity_index"
      - "{ISO3}.survey.pmi.inventory"
      - "{ISO3}.industry.transport_equipment.new_orders.real"
      - "{ISO3}.industry.transport_equipment.shipments.real"
      - "{ISO3}.industry.transport_equipment.production.real"
      - "{ISO3}.industry.transport_equipment.payroll.real"
      - "{ISO3}.survey.consumer_confidence"

    min_real_components: 3

  - sector_id: manufacturing

    coincident_metrics:
      - "{ISO3}.manufacturing.output.real_index"
      - "{ISO3}.manufacturing.employment.total"
      - "{ISO3}.manufacturing.payroll.real"
      - "{ISO3}.manufacturing.sales.real"

    leading_metrics:
      - "{ISO3}.manufacturing.new_orders.real"
      - "{ISO3}.manufacturing.inventory_sales_ratio"
      - "{ISO3}.manufacturing.capacity_utilisation"
      - "{ISO3}.trade.export_orders"
      - "{ISO3}.energy.industry_price_yoy"

    min_real_components: 3

  - sector_id: construction_property

    coincident_metrics:
      - "{ISO3}.construction.output.real_index"
      - "{ISO3}.construction.employment.total"
      - "{ISO3}.construction.payroll.real"
      - "{ISO3}.construction.investment.real"

    leading_metrics:
      - "{ISO3}.construction.permits"
      - "{ISO3}.property.real_price_yoy"
      - "{ISO3}.property.credit_growth"
      - "{ISO3}.property.unsold_inventory_ratio"
      - "{ISO3}.construction.new_orders"

    min_real_components: 3

  - sector_id: trade_tourism

    coincident_metrics:
      - "{ISO3}.trade.retail_sales.real"
      - "{ISO3}.tourism.arrivals"
      - "{ISO3}.tourism.receipts.real"
      - "{ISO3}.trade_tourism.employment.total"

    leading_metrics:
      - "{ISO3}.survey.consumer_confidence"
      - "{ISO3}.transport.passenger_volume"
      - "{ISO3}.transport.air_passengers"
      - "{ISO3}.trade.card_spending.real"
      - "{ISO3}.tourism.bookings_or_equivalent"

    min_real_components: 3
```

## Çalıştırma

```
python t2saim_sector_cycle_engine.py `
  --root "." `
  --as-of "2026-10-04T00:00:00Z"
```

Sadece belirli ülkeler:

```
python t2saim_sector_cycle_engine.py `
  --root "." `
  --countries TUR CZE BRA MEX POL `
  --as-of "2026-10-04T00:00:00Z"
```

## Kritik uygulama notu

YAML’deki `{ISO3}` ifadesi doğrudan çalışmaz; country adapter katmanında örneğin:

```
{ISO3}.transport.output.real_index
```

şu gerçek canonical ID’ye çözülmelidir:

```
TUR.transport.output.real_index
```

veya daha temiz biçimde Silver panelde ülke kodu zaten ayrı kolonda tutulduğu için metric ID ülke öneki olmadan standardize edilmelidir:

```
transport.output.real_index
transport.payroll.real
transport.consumption.real
transport.employment.total
```

Ben ikinci yaklaşımı öneririm:

```
country_iso3 = TUR
metric_id = transport.output.real_index
```

Böylece aynı sektör motoru 37 ülke için tek parametreyle çalışır.

## Bilimsel sınır

Bu PDF’den alınabilecek metodolojik dersler şunlardır:

- Ulaştırma, stok, imalat, enerji, tüketim ve ticaret çevrimleri ekonomik turning point’lerde hassas olabilir.
- Birden çok eşzamanlı seri, tek bir sektörel çıktı serisinden daha güvenilir sektör rejimi tanımlayabilir.
- CCI için ortak faktör; CLI için istikrarlı lead–lag ilişkisi gerekir.
- Sektörel yavaşlama ile tam ekonomik resesyon ayrılmalıdır.
- Bir seri “öncü” diye kabul edilmeden önce çevrim tarihleri, yanlış sinyaller ve lead-time backtest edilmelidir.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/e3b5ffae-0dbb-43b2-a417-5303b12050db/CONTRIBUTIONS_TO_ECONOMIC_ANALYSISTRA_z_library_sk-_1lib_sk.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=ASIA2F3EMEYE5NO54L36%2F20261003%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261003T223853Z&X-Amz-Expires=1536&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEO%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGYYzZmruXWC3WnvQsVS73NmBmjE6nwRF5lm7lW5dA7hAiBr56fhafs2kuhvVlii4VHmhVlWjyoq0FkinJlhCFftoCqJBQi3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDY5OTc1MzMwOTcwNSIMHDG6tiV8zzZYwgF%2FKt0EMq9IYs3MObp5DlJE7SiS08ln1S2n1bGK9s1PaAN6WTh2Tlx%2FFm1bnZhhomZBThLIAMgrAJ6kGDsCAheas7mTsXFyFBjXmT59GCQyp2QNukvfGyQr3GBH%2Fyxd38v4NKMxPTC72YoIhZPen4mj85ppSm%2BXle61u%2BPZ%2BGFr4Dsy3H10XvzHW4qPcaOf6crVZhspiW7jfpR%2FEQ5Co70zwRv4PsWwZgxXEofT1h5aZqsn0mRPdQcAoxBEiV62DBP%2BvR44PW68TyVkADWoDPJx0zcPN6iZziiDJ8eb4kQwFrKOJ2Azepa%2BLIvmVM4KzXmrIJbo9bhMcQ4fr5TaH%2FR5P2L21QtXuXQuvtO1YHeQmJtjzHoPcuok%2Fh33fZYFIk%2FKlyG0so6MvuyqjvsVoDOVTiz9vj1VGw%2B%2Bq59SLkU53UBtzkymfPODa3AHr%2BeS8%2BrUQO4Ho9a50Da7i1xn0rDJGoi5VKeT7gOEF1VLpLuygnfMsLtaSLPUscSeGbSQmxKcyBcjzAR5CTPgsMAV65jMnGhv57M0s0BgcSnYnCrk6sDHVDeD31RluAh2Vw7S2tdJEGlT0ECy0KpeF2qvZSsIQh%2B5%2BBsMC62ce%2FMsg3TpBX08cSsm2NuYw4GQ5Rerre%2B7wnIEuic7GdZ%2Fkgd48ip0oVY3NZEmuzR22P5fDcQ2WNPFdqkPB3khKz%2BBRNb6JYk9PbgCB6jvLtt5%2BLohTzJAOOC2eVxOrz3%2F951QJbX2lHS4hFdw9jecM7nDd3JAwEzJEn%2F6ytUNp5fd6p7W0ms07UQYHKvk0mbfr3XWNiZ65AkwqviF1gY6mQE0i3RGj2UjUdPpSOCjYn6GBfkFVcYVpHgLRxiXKBrZ0xEorNr2PFTf7XIbtOR1RqjJBzeiBvle7PLb3j6v8AxhdVEmrr2TJiZtsmOGlLxNf9RlskgIEZsyPmE10v7uEyGRJ3UBbLw%2F%2FJtU7793qo63GuWAVlnJ2fMdIbAjcEcUJcIOzVWwMXtgW6TwjeUxmuIlkIxk1%2BewsUg%3D&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=8d496df441e60facab6bf12d078411f59841de06600a7e4cad8bead95e8e2215)]

Bu kod, T2SAIM’de 37 ülke × 30 yıl veri atlasından sektör bazlı gerçek CCI/CLI üretmenin başlangıç katmanıdır. Statik PDF parametrelerini kopyalamaz; her ülkenin kendi gerçek verisinden, kendi sektör yapısına göre yeniden hesaplar.

## 🚢 2. FİZİKSEL LOJİSTİK ÖNCÜ GÖSTERGELERİ
- **Hava Kargo Ton-Km (`TRANS_AIR_FREIGHT`):** Küresel ticarette yüksek katma değerli yarı iletken ve endüstriyel parça akışını temsil eder. Resesyonları 3-6 ay önceden haber verir.
- **Havayolu Kalkış Sayısı (`TRANS_AIR_DEPARTURES`):** İş seyahatleri ve ekonomik hareketliliğin nabzıdır.
- **LPI Altyapı ve Gümrük Skoru (`TRANS_LPI_INFRA`):** Fiziksel darboğazların maliyet enflasyonuna dönüşme direncidir.
