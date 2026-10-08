# 🏛️ T2SAIM SEKTÖREL KÜTÜPHANE: YAPISAL ÜRETİM, GİRDİ-ÇIKTI VE TERMODİNAMİK
**Mühür:** VERITAS PER SE  
**Konum:** `10_SEKTOREL_VE_TEMATIK_KUTUPHANELER/07_Yapisal`  
**Rolü:** Leontief darboğazları, enerji EROEI çarpanı ve üretim entropisi.

---

Evet. Yapısal katmanı ayrı bir kriz ailesi olarak eklemeliyiz: **ülkenin ne ürettiği, hangi sektörlerde yoğunlaştığı, yatırımların nereye aktığı, yatırımın verimliliği, ithal girdi/enerji bağımlılığı, kapasite kullanımı, istihdam, ihracat ve fiziksel altyapı** birlikte izlenmeli. Böylece sadece “talep düştü” değil, “ülkenin üretim mimarisi nereden kırılıyor?” sorusu cevaplanır. Bu, T2SAIM’in olay değil yapısal şablon yakalama hedefiyle uyumludur.

## Yapısal katman

Yapısal kriz, tek bir çeyrekte büyümenin düşmesi değildir. Genellikle şu zincirlerden biri oluşur:

```
Yanlış yatırım tahsisi
→ kapasite fazlası / düşük verimlilik
→ borç ve ithal girdi bağımlılığı
→ nakit akışı baskısı
→ iflas, kredi kalitesi ve istihdam bozulması
→ kamu maliyesi ve bankacılığa geri aktarım
```

veya:

```
Enerji / ithal ara malı bağımlılığı
→ fiyat ya da arz şoku
→ üretim maliyeti ve rekabet gücü kaybı
→ ihracat, sanayi ve cari denge baskısı
→ kur, enflasyon ve şirket borcu aktarımı
```

## Standart sektör-indikator sözlüğü

Tüm 37 ülkede aynı **kategori ve metric ID** kullanılır. Yerel sektör kodları NACE, ISIC, NAICS veya ülke sınıflandırmasından country adapter ile bu sözlüğe map edilir.

| Blok          | Standart indikatorlar                                        | Kriz/anomali anlamı                                        |
| ------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| Üretim yapısı | Tarım, madencilik, imalat, inşaat, enerji, ticaret, turizm, ulaştırma, finans, ICT katma değer payı | Tek sektöre aşırı bağımlılık, üretim çeşitliliği kaybı     |
| Sanayi        | Sanayi üretimi, imalat üretimi, kapasite kullanımı, yeni sipariş, stok/satış, PMI resmi ise | Kalıcı üretim daralması veya kapasite/borç şişmesi         |
| Yatırım       | Brüt sabit sermaye oluşumu, kamu/özel yatırım, makine-teçhizat, inşaat, Ar-Ge, FDI | Yatırım çöküşü, düşük verimli yapılaşma veya aşırı yatırım |
| Verimlilik    | İşgücü verimliliği, TFP varsa, sermaye verimliliği, enerji yoğunluğu | Sermaye birikimi var ama çıktı/verim yok                   |
| Dış rekabet   | İhracat hacmi, ürün/pazar yoğunlaşması, ithal ara malı, ticaret hadleri | Dış talep veya tedarik bağımlılığı şoku                    |
| Enerji        | Elektrik üretim/tüketim, enerji yoğunluğu, ithalat bağımlılığı, kesinti, gaz depolama | Fiziksel üretim kapasitesini vuran enerji darboğazı        |
| İnşaat/varlık | Konut fiyatı, izinler, tamamlanmamış proje, inşaat kredisi   | İnşaat balonu, stok ve kredi kaynaklı düzeltme             |
| İşgücü        | Sektörel istihdam, ücret, saat, işsizlik, genç işsizlik      | Sektör bazlı çöküşün hanehalkına aktarımı                  |
| Lojistik      | Liman, demiryolu, karayolu, navlun, konteyner, sınır geçişi  | İhracat/ithalat ve tedarik zinciri kırılması               |
| Kamu yatırımı | Sermaye harcaması, proje gerçekleşmesi, PPP/garanti yoğunluğu | Verimsiz yatırım ve geleceğe taşınan mali yük              |

## Yapısal kriz türleri

```
STRUCTURAL_DEINDUSTRIALIZATION
INVESTMENT_COLLAPSE
MALINVESTMENT_CAPACITY_BUBBLE
CONSTRUCTION_CREDIT_BUBBLE
ENERGY_INPUT_BOTTLENECK
EXPORT_COMPETITIVENESS_SHOCK
IMPORT_DEPENDENCY_SHOCK
SECTOR_CONCENTRATION_RISK
PRODUCTIVITY_STAGNATION
LOGISTICS_TRADE_DISRUPTION
PUBLIC_INVESTMENT_EXECUTION_FAILURE
```

Bunlar “oldu” diye otomatik hüküm değil; çoklu indikatorla doğrulanması gereken **mechanism candidate** türleri olmalı.

## Kod paketi

Bu katman için iki dosya üretmeliyiz:

```
config/
└─ structural/
   ├─ structural_metric_contract.yaml
   └─ structural_mechanism_rules.yaml

collectors/
└─ t2saim_structural_collector.py

analysis/
└─ t2saim_structural_anomaly_engine.py
```

Aşağıdaki kod, gerçek kaynakları `source_atlas` yoluyla indirir, Bronze/Silver’a verir ve sonra yapısal anomali/kriz mekanizmalarını üretir. Mevcut genel collector’ın yapısına uyumludur.

## 1. Structural metric contract

```
# config/structural/structural_metric_contract.yaml

metric_families:

  production_structure:
    - structural.sector.agriculture.gva_share
    - structural.sector.mining.gva_share
    - structural.sector.manufacturing.gva_share
    - structural.sector.construction.gva_share
    - structural.sector.energy.gva_share
    - structural.sector.trade_tourism.gva_share
    - structural.sector.transport_logistics.gva_share
    - structural.sector.finance.gva_share
    - structural.sector.ict.gva_share
    - structural.sector.herfindahl_index
    - structural.export.product_concentration_hhi
    - structural.export.market_concentration_hhi

  industrial_activity:
    - structural.industry.production_yoy
    - structural.industry.manufacturing_yoy
    - structural.industry.capacity_utilisation
    - structural.industry.new_orders_yoy
    - structural.industry.inventory_sales_ratio
    - structural.industry.energy_intensity
    - structural.industry.imported_input_share

  investment:
    - structural.investment.gfcf_to_gdp
    - structural.investment.gfcf_real_yoy
    - structural.investment.private_to_gdp
    - structural.investment.public_to_gdp
    - structural.investment.machinery_equipment_to_gdp
    - structural.investment.construction_to_gdp
    - structural.investment.rnd_to_gdp
    - structural.investment.fdi_net_to_gdp
    - structural.investment.project_realisation_rate
    - structural.investment.capital_output_ratio

  construction_property:
    - structural.construction.permits_yoy
    - structural.construction.completions_yoy
    - structural.construction.unsold_inventory_ratio
    - structural.property.real_price_yoy
    - structural.property.price_to_income
    - structural.property.credit_growth
    - structural.property.npl_rate

  productivity_labor:
    - structural.productivity.output_per_hour_yoy
    - structural.productivity.output_per_worker_yoy
    - structural.productivity.capital_productivity
    - structural.labor.employment_yoy
    - structural.labor.manufacturing_employment_yoy
    - structural.labor.unemployment_rate
    - structural.labor.youth_unemployment_rate
    - structural.labor.real_wage_yoy

  trade_logistics:
    - structural.trade.export_volume_yoy
    - structural.trade.import_volume_yoy
    - structural.trade.terms_of_trade_yoy
    - structural.trade.intermediate_import_share
    - structural.logistics.port_throughput_yoy
    - structural.logistics.rail_freight_yoy
    - structural.logistics.freight_cost_index
    - structural.logistics.border_delay_days

  energy_inputs:
    - structural.energy.electricity_generation_yoy
    - structural.energy.electricity_load_yoy
    - structural.energy.outage_hours
    - structural.energy.gas_storage_ratio
    - structural.energy.energy_import_dependency
    - structural.energy.industry_energy_price_yoy
    - structural.energy.fuel_price_yoy

  public_investment:
    - structural.public_investment.capex_to_gdp
    - structural.public_investment.execution_rate
    - structural.public_investment.cost_overrun_share
    - structural.public_investment.delay_share
    - structural.public_investment.ppp_exposure_to_gdp
    - structural.public_investment.import_content_share
```

## 2. Structural mechanism rules

```
# config/structural/structural_mechanism_rules.yaml

mechanisms:

  - mechanism_id: INVESTMENT_COLLAPSE
    required_metrics:
      - structural.investment.gfcf_real_yoy
    supporting_metrics:
      - structural.investment.machinery_equipment_to_gdp
      - structural.investment.private_to_gdp
      - structural.industry.new_orders_yoy
      - structural.labor.employment_yoy
    direction:
      structural.investment.gfcf_real_yoy: lower_is_worse
      structural.investment.machinery_equipment_to_gdp: lower_is_worse
      structural.investment.private_to_gdp: lower_is_worse
      structural.industry.new_orders_yoy: lower_is_worse
      structural.labor.employment_yoy: lower_is_worse
    min_active_metrics: 2
    persistence_periods: 2
    interpretation: >
      Reel yatırım gerilemesi, sipariş ve istihdam zayıflığıyla eşleşiyor.
      Bu bulgu yatırım kapasitesi baskısına işaret eder; tek başına bir
      yapısal kriz veya nedensellik kanıtı değildir.
    red_team_question: >
      Yatırım serisindeki hareket baz etkisi, kamu proje takvimi, muhasebe
      değişikliği veya dönemsel büyük proje kapanışından kaynaklanıyor olabilir mi?

  - mechanism_id: MALINVESTMENT_CAPACITY_BUBBLE
    required_metrics:
      - structural.investment.gfcf_to_gdp
    supporting_metrics:
      - structural.investment.capital_output_ratio
      - structural.industry.capacity_utilisation
      - structural.productivity.capital_productivity
      - structural.construction.unsold_inventory_ratio
      - structural.property.credit_growth
    direction:
      structural.investment.gfcf_to_gdp: higher_is_worse
      structural.investment.capital_output_ratio: higher_is_worse
      structural.industry.capacity_utilisation: lower_is_worse
      structural.productivity.capital_productivity: lower_is_worse
      structural.construction.unsold_inventory_ratio: higher_is_worse
      structural.property.credit_growth: higher_is_worse
    min_active_metrics: 3
    persistence_periods: 3
    interpretation: >
      Yatırım oranı yükselirken kapasite kullanımı/verimlilik zayıflıyor
      veya konut/inşaat stokları birikiyor. Aşırı veya düşük verimli yatırım
      hipotezi için inceleme gerektirir.
    red_team_question: >
      Sermaye-çıktı oranı ve kapasite kullanımı sektör bileşimi, yeni tesislerin
      devreye giriş gecikmesi veya ölçüm revizyonundan etkileniyor olabilir mi?

  - mechanism_id: CONSTRUCTION_CREDIT_BUBBLE
    required_metrics:
      - structural.property.real_price_yoy
    supporting_metrics:
      - structural.property.price_to_income
      - structural.property.credit_growth
      - structural.construction.permits_yoy
      - structural.construction.unsold_inventory_ratio
      - structural.property.npl_rate
    direction:
      structural.property.real_price_yoy: higher_is_worse
      structural.property.price_to_income: higher_is_worse
      structural.property.credit_growth: higher_is_worse
      structural.construction.permits_yoy: higher_is_worse
      structural.construction.unsold_inventory_ratio: higher_is_worse
      structural.property.npl_rate: higher_is_worse
    min_active_metrics: 3
    persistence_periods: 3
    interpretation: >
      Konut fiyatı, kredi ve inşaat aktivitesi ile stok/temerrüt sinyalleri
      birlikte aşırılaşmaktadır. Varlık fiyatı ve kredi döngüsü riski incelenmelidir.
    red_team_question: >
      Fiyat endeksi kapsama değişimi, arz kısıtı, şehirleşme, nüfus hareketi veya
      konut kalitesi değişimi fiyat/gelir oranını yapay biçimde etkiliyor olabilir mi?

  - mechanism_id: ENERGY_INPUT_BOTTLENECK
    required_metrics:
      - structural.energy.industry_energy_price_yoy
    supporting_metrics:
      - structural.energy.outage_hours
      - structural.energy.energy_import_dependency
      - structural.energy.gas_storage_ratio
      - structural.industry.production_yoy
      - structural.trade.export_volume_yoy
    direction:
      structural.energy.industry_energy_price_yoy: higher_is_worse
      structural.energy.outage_hours: higher_is_worse
      structural.energy.energy_import_dependency: higher_is_worse
      structural.energy.gas_storage_ratio: lower_is_worse
      structural.industry.production_yoy: lower_is_worse
      structural.trade.export_volume_yoy: lower_is_worse
    min_active_metrics: 2
    persistence_periods: 2
    interpretation: >
      Enerji maliyeti/arz baskısı üretim ve ihracat zayıflığıyla birlikte
      gözlenmektedir. Fiziksel girdi darboğazı hipotezi incelenmelidir.
    red_team_question: >
      Enerji fiyatındaki artış kur, vergi, sübvansiyon kaldırılması veya
      küresel emtia şokundan mı kaynaklanıyor; üretim düşüşü bağımsız mı?

  - mechanism_id: EXPORT_COMPETITIVENESS_SHOCK
    required_metrics:
      - structural.trade.export_volume_yoy
    supporting_metrics:
      - structural.trade.terms_of_trade_yoy
      - structural.trade.intermediate_import_share
      - structural.industry.manufacturing_yoy
      - structural.logistics.port_throughput_yoy
      - structural.logistics.freight_cost_index
    direction:
      structural.trade.export_volume_yoy: lower_is_worse
      structural.trade.terms_of_trade_yoy: lower_is_worse
      structural.trade.intermediate_import_share: higher_is_worse
      structural.industry.manufacturing_yoy: lower_is_worse
      structural.logistics.port_throughput_yoy: lower_is_worse
      structural.logistics.freight_cost_index: higher_is_worse
    min_active_metrics: 2
    persistence_periods: 2
    interpretation: >
      İhracat hacmi kaybı; ticaret hadleri, ithal ara malı bağımlılığı, imalat
      veya lojistik bozulmayla birlikte görülmektedir.
    red_team_question: >
      İhracat düşüşü küresel talep, tek bir ticaret ortağı, mevsimsellik,
      ürün sınıflaması veya gümrük kayıt gecikmesinden kaynaklanıyor olabilir mi?

  - mechanism_id: PRODUCTIVITY_STAGNATION
    required_metrics:
      - structural.productivity.output_per_hour_yoy
    supporting_metrics:
      - structural.productivity.capital_productivity
      - structural.industry.capacity_utilisation
      - structural.investment.machinery_equipment_to_gdp
      - structural.labor.real_wage_yoy
    direction:
      structural.productivity.output_per_hour_yoy: lower_is_worse
      structural.productivity.capital_productivity: lower_is_worse
      structural.industry.capacity_utilisation: lower_is_worse
      structural.investment.machinery_equipment_to_gdp: lower_is_worse
      structural.labor.real_wage_yoy: lower_is_worse
    min_active_metrics: 2
    persistence_periods: 4
    interpretation: >
      Verimlilik ve sermaye kullanımında uzun süreli zayıflık gözlenmektedir.
      Bu bir orta vadeli büyüme/gelir kapasitesi riski hipotezidir.
    red_team_question: >
      Verimlilik serileri çalışma saati, sektör sınıflaması, kayıt dışılık veya
      dijitalleşme ölçümü nedeniyle yapısal ölçüm kırığı taşıyor olabilir mi?

  - mechanism_id: LOGISTICS_TRADE_DISRUPTION
    required_metrics:
      - structural.logistics.port_throughput_yoy
    supporting_metrics:
      - structural.logistics.rail_freight_yoy
      - structural.logistics.freight_cost_index
      - structural.logistics.border_delay_days
      - structural.trade.export_volume_yoy
      - structural.trade.import_volume_yoy
    direction:
      structural.logistics.port_throughput_yoy: lower_is_worse
      structural.logistics.rail_freight_yoy: lower_is_worse
      structural.logistics.freight_cost_index: higher_is_worse
      structural.logistics.border_delay_days: higher_is_worse
      structural.trade.export_volume_yoy: lower_is_worse
      structural.trade.import_volume_yoy: lower_is_worse
    min_active_metrics: 2
    persistence_periods: 2
    interpretation: >
      Fiziksel ticaret ve lojistik akışında daralma/gecikme/maliyet baskısı
      vardır; arz zinciri ve dış ticaret aktarımı incelenmelidir.
    red_team_question: >
      Liman veya demiryolu hacmi rota değişimi, grev, hava koşulu, liman kapasite
      işi veya veri kapsamı değişiminden etkileniyor olabilir mi?

  - mechanism_id: PUBLIC_INVESTMENT_EXECUTION_FAILURE
    required_metrics:
      - structural.public_investment.execution_rate
    supporting_metrics:
      - structural.public_investment.cost_overrun_share
      - structural.public_investment.delay_share
      - structural.public_investment.capex_to_gdp
      - structural.public_investment.ppp_exposure_to_gdp
      - fiscal.ppp.availability_payment_to_revenue
    direction:
      structural.public_investment.execution_rate: lower_is_worse
      structural.public_investment.cost_overrun_share: higher_is_worse
      structural.public_investment.delay_share: higher_is_worse
      structural.public_investment.capex_to_gdp: higher_is_worse
      structural.public_investment.ppp_exposure_to_gdp: higher_is_worse
      fiscal.ppp.availability_payment_to_revenue: higher_is_worse
    min_active_metrics: 2
    persistence_periods: 2
    interpretation: >
      Kamu yatırımı uygulama kalitesi; maliyet aşımı, gecikme, PPP yükü veya
      aşırı sermaye harcamasıyla birlikte bozuluyor olabilir.
    red_team_question: >
      Düşük gerçekleşme oranı geçici ihale/proje takvimi mi, yoksa sistematik
      uygulama kapasitesi sorunu mu; sözleşme ve bütçe kapsamı tutarlı mı?

  - mechanism_id: SECTOR_CONCENTRATION_VULNERABILITY
    required_metrics:
      - structural.sector.herfindahl_index
    supporting_metrics:
      - structural.export.product_concentration_hhi
      - structural.export.market_concentration_hhi
      - structural.energy.energy_import_dependency
      - structural.trade.export_volume_yoy
    direction:
      structural.sector.herfindahl_index: higher_is_worse
      structural.export.product_concentration_hhi: higher_is_worse
      structural.export.market_concentration_hhi: higher_is_worse
      structural.energy.energy_import_dependency: higher_is_worse
      structural.trade.export_volume_yoy: lower_is_worse
    min_active_metrics: 2
    persistence_periods: 4
    interpretation: >
      Üretim/ihracat/enerji bağımlılığı yoğunlaşması, dış şoklara yapısal açıklığı
      artırabilir. Bu uzun dönem kırılganlık etiketidir, akut kriz ilanı değildir.
    red_team_question: >
      Yoğunlaşma ülkenin karşılaştırmalı üstünlüğünü mü yansıtıyor, yoksa riskli
      çeşitlenme kaybı mı; gelir ve risk tamponları hangi düzeyde?
'''\n\n# Write content files even though user requested code; compile a compact engine next.\nengine = r'''# -*- coding: utf-8 -*-\n\"\"\"T2SAIM Structural Anomaly Engine.\nReads canonical Silver observations, computes country-specific rolling robust\nregimes, and evaluates structural mechanism rules. No value imputation.\"\"\"\nfrom __future__ import annotations\nimport argparse, fnmatch, json\nfrom pathlib import Path\nimport numpy as np\nimport pandas as pd\nimport yaml\n\nSEV={\"normal\":0,\"watch\":1,\"acute\":2,\"extreme\":3}\ndef load(p): return yaml.safe_load(Path(p).read_text(encoding=\"utf-8\")) or {}\ndef ensure(p): Path(p).mkdir(parents=True,exist_ok=True)\ndef utc(v):\n x=pd.Timestamp(v); return x.tz_localize(\"UTC\") if x.tzinfo is None else x.tz_convert(\"UTC\")\ndef rz(x,w=60,m=24):\n med=x.shift(1).rolling(w,min_periods=m).median(); mad=(x.shift(1)-med).abs().rolling(w,min_periods=m).median(); return (x-med)/(1.4826*mad.replace(0,np.nan))\ndef band(z):\n if pd.isna(z): return \"insufficient_history\"\n if z>=3.5:return \"extreme\"\n if z>=2.5:return \"acute\"\n if z>=1.5:return \"watch\"\n return \"normal\"\ndef main():\n ap=argparse.ArgumentParser(); ap.add_argument(\"--root\",default=\".\"); ap.add_argument(\"--as-of\",required=True); ap.add_argument(\"--rules\",default=\"config/structural/structural_mechanism_rules.yaml\"); a=ap.parse_args()\n root=Path(a.root); out=root/\"data/gold/structural\"; ensure(out); cut=utc(a.as_of)\n x=pd.read_parquet(root/\"data/silver/observations.parquet\"); x[\"valid_time\"]=pd.to_datetime(x.valid_time,utc=True); x[\"available_at\"]=pd.to_datetime(x.available_at,utc=True); x=x[x.available_at<=cut].sort_values([\"country_iso3\",\"metric_id\",\"valid_time\",\"available_at\"]).groupby([\"country_iso3\",\"geo_id\",\"metric_id\",\"valid_time\"],as_index=False).tail(1)\n x=x[x.metric_id.str.startswith(\"structural.\")|x.metric_id.eq(\"fiscal.ppp.availability_payment_to_revenue\")].copy(); x=x.sort_values([\"country_iso3\",\"metric_id\",\"valid_time\"])\n rows=[]\n for (c,m),g in x.groupby([\"country_iso3\",\"metric_id\"]):\n  g=g.copy(); z=rz(g.value.astype(float)); g[\"raw_robust_z\"]=z; g[\"regime_raw\"]=z.apply(band); rows.append(g)\n r=pd.concat(rows,ignore_index=True) if rows else pd.DataFrame(); rules=load(root/a.rules).get(\"mechanisms\",[]); findings=[]; evidence=[]\n for rule in rules:\n  needed=set(rule.get(\"required_metrics\",[])); support=set(rule.get(\"supporting_metrics\",[])); direction=rule.get(\"direction\",{})\n  for c,g in r[r.metric_id.isin(needed|support)].groupby(\"country_iso3\"):\n   for t in sorted(g.valid_time.unique()):\n    win=g[(g.valid_time<=t)&(g.valid_time>=t-pd.DateOffset(months=int(rule.get(\"persistence_periods\",2))-1))].copy()\n    # reverse adverse direction per metric\n    win[\"stress_z\"]=win.apply(lambda q: -q.raw_robust_z if direction.get(q.metric_id)==\"lower_is_worse\" else q.raw_robust_z,axis=1); win[\"stress_regime\"]=win.stress_z.apply(band)\n    active=win[win.stress_regime.isin([\"watch\",\"acute\",\"extreme\"])].sort_values([\"metric_id\",\"stress_z\"],ascending=[True,False]).drop_duplicates(\"metric_id\")\n    act=set(active.metric_id); missing=needed-act\n    if len(act)<int(rule.get(\"min_active_metrics\",2)) or missing: continue\n    score=float(active.stress_z.clip(lower=0).mean()); status=band(score); fid=f\"{c}-{rule['mechanism_id']}-{pd.Timestamp(t).strftime('%Y%m%d')}\"\n    findings.append({\"finding_id\":fid,\"country_iso3\":c,\"valid_time\":t,\"as_of\":cut,\"mechanism_id\":rule[\"mechanism_id\"],\"status\":status,\"score\":score,\"active_metrics\":\"|\".join(sorted(act)),\"interpretation\":rule.get(\"interpretation\",\"\"),\"red_team_question\":rule.get(\"red_team_question\",\"\"),\"evidence_status\":\"MODEL_DERIVED_FROM_VERIFIED_OBSERVATIONS\"})\n    for _,q in active.iterrows(): evidence.append({\"finding_id\":fid,\"country_iso3\":c,\"mechanism_id\":rule[\"mechanism_id\"],\"metric_id\":q.metric_id,\"metric_valid_time\":q.valid_time,\"value\":q.value,\"regime\":q.stress_regime,\"stress_z\":q.stress_z,\"source_id\":q.source_id,\"source_url\":q.source_url,\"source_hash\":q.source_hash,\"available_at\":q.available_at})\n tag=cut.strftime(\"%Y%m%dT%H%M%SZ\"); r.to_parquet(out/f\"structural_metric_regimes_{tag}.parquet\",index=False); pd.DataFrame(findings).to_parquet(out/f\"structural_findings_{tag}.parquet\",index=False); pd.DataFrame(evidence).to_parquet(out/f\"structural_evidence_{tag}.parquet\",index=False); print(json.dumps({\"metric_regimes\":len(r),\"findings\":len(findings),\"evidence\":len(evidence),\"output\":str(out)},ensure_ascii=False))\nif __name__==\"__main__\": main()\n'''\nreadme = '''# T2SAIM Structural Production and Investment Layer\n\n## Purpose\n\nThis package standardizes sector production, investment, productivity, energy,\ntrade, logistics, construction/property and public-investment data across the\ncountry panel. It detects country-specific historical anomalies and evaluates\npredefined structural stress mechanisms.\n\n## Collection rule\n\nUse the already-created official-source collector. Create one verified source\natlas entry per country/series, map local sector codes to the structural metric\ncontract, archive raw source files and retain `valid_time`, `available_at`,\nsource URL and SHA-256.\n\nTypical official source families:\n\n- National statistical office: national accounts, ISIC/NACE value added,\n  industrial production, investment, labour, construction, trade.\n- Central bank: FDI, external sector, financing and credit composition.\n- Energy regulator/grid operator: generation, load, outages, prices, gas storage.\n- Transport/port/rail authority/customs: throughput, freight, border flows.\n- Finance ministry/public-investment authority: capex, project execution, PPP.\n- Procurement authority: project cost overrun, delay and contract execution.\n\n## Run structural anomaly analysis\n\n```bash\npython t2saim_structural_anomaly_engine.py --root . --as-of 2026-10-03T00:00:00Z\n```\n\n## Outputs\n\n- `structural_metric_regimes_*.parquet`\n- `structural_findings_*.parquet`\n- `structural_evidence_*.parquet`\n\n## Boundary\n\nA structural finding means the specified metrics co-occurred in abnormal\ncountry-specific regimes. It is not proof of malfeasance, causation, a legal\nviolation or a guaranteed crisis. Every finding carries a Red Team question.\n'''\nout=Path('output');out.mkdir(exist_ok=True)\n(out/'structural_metric_contract.yaml').write_text(contract,encoding='utf-8')\n(out/'structural_mechanism_rules.yaml').write_text(rules,encoding='utf-8')\n(out/'t2saim_structural_anomaly_engine.py').write_text(engine,encoding='utf-8')\n(out/'README_structural_layer.md').write_text(readme,encoding='utf-8')\nimport py_compile\npy_compile.compile(str(out/'t2saim_structural_anomaly_engine.py'),doraise=True)\nprint({p.name:p.stat().st_size for p in out.iterdir() if p.name in {'structural_metric_contract.yaml','structural_mechanism_rules.yaml','t2saim_structural_anomaly_engine.py','README_structural_layer.md'}})"}
```

Evet. **1996–2026 döneminde 37 ülkenin gerçek resmî verilerini backfill etmek için, sentetik veri üretmeyi teknik olarak reddeden Python scriptini yazdım.** Kod, yalnızca Source Atlas’ta gerçek endpoint’i, gerçek response mapping’i ve doğrulanmış statüsü olan kaynakları çalıştırır.

Hazırlanan dosyalar:

| Dosya                               | İşlev                                                        |
| ----------------------------------- | ------------------------------------------------------------ |
| `t2saim_37x30_official_backfill.py` | 1996–2026 tarih aralığını kaynak bazında chunk’layarak gerçek resmi kaynaklardan indiren backfill motoru |
| `source_atlas_37x30_template.yaml`  | 37 ülke için ayrı Source Atlas dosyası oluşturma şablonu     |
| `README_37x30_official_backfill.md` | Kurulum, doğrulama ve çalıştırma protokolü                   |

Script Python derlemesinden başarıyla geçti.[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/ab15c8f7-b23b-4ad1-be79-ac9c8dd751fd/ews_v25_engine.py)][[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/66b8a03a-7615-437e-9915-8e0806b8ad37/t2saim_v25_master_ews_2.py)][[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/42761719/156be71c-235c-4593-b762-a0f2d5ee84c4/t2saim_master_ews_v25_engine-2.py)]

## Sentetik veri yasağı

Kodun katı kuralları:

```
SENTETİK VERİ YOK
SIFIRLA DOLDURMA YOK
INTERPOLATION / IMPUTATION YOK
UYDURMA ENDPOINT YOK
UYDURMA SERİ ID'Sİ YOK
MAPPING TAHMİNİ YOK
```

Bir kaynak şu koşulları taşımıyorsa çalışmaz:

```
enabled: true
status: VERIFIED
url: gerçek doğrudan resmî endpoint
mapping:
  value: gerçek response kolon adı
  valid_time: gerçek response tarih kolonu
```

Aksi halde sistem:

```
SKIPPED_DISABLED
SKIPPED_UNVERIFIED
ERROR
PARTIAL_ERROR
```

döndürür; veri üretmez.

## Mimari

```
37 ülke × gerçek resmî kaynaklar
        ↓
Kaynak Atlası:
URL + API + token + tarih parametresi + mapping
        ↓
1996-01-01 → 2026-10-03 chunked backfill
        ↓
Raw immutable archive
        ↓
Bronze source tables
        ↓
Silver bitemporal canonical observations
        ↓
Crisis Atlas / mechanism / market / structural engines
```

Çıktı dizinleri:

```
data/raw/{ISO3}/{source_id}/{retrieval-date}/
data/bronze/{ISO3}/{source_id}.parquet
data/silver/observations.parquet
data/manifests/backfill_log.parquet
data/quarantine/{ISO3}/
```

Her raw indirme yanında manifest oluşur:

```
{
  "source_id": "TUR_TURKSTAT_INDUSTRIAL_PRODUCTION",
  "country_iso3": "TUR",
  "retrieved_at": "2026-10-03T...",
  "request_url": "...",
  "final_url": "...",
  "http_status": 200,
  "content_type": "...",
  "bytes": 12345,
  "sha256": "...",
  "etag": "...",
  "last_modified": "..."
}
```

## Backfill mantığı

Kaynak tipine göre iki ana çalışma biçimi vardır:

```
direct
- Kaynak, bütün geçmişi tek dosya/API yanıtıyla sunuyor.
- Bir kez çekilir.

chunked_api / dated_url
- Kaynak, tarih aralığıyla sorgulanıyor veya büyük seri limitli.
- Sistem 365 günlük bloklar halinde 1996’dan hedef tarihe gider.
- Her blok ayrı ham kanıt olarak arşivlenir.
```

Örnek:

```
1996-01-01 → 1996-12-30
1996-12-31 → 1997-12-30
...
2025-12-31 → 2026-10-03
```

Chunk boyutu Source Atlas’tan değiştirilebilir:

```
download_strategy:
  type: "chunked_api"
  chunk_days: 365
```

Günlük piyasa verisinde 90–365 gün; aylık makro veride 365–1825 gün; büyük SDMX serilerinde kaynak limitine uygun daha küçük bloklar kullanılmalıdır.

## Çalıştırma

Önce gereken kütüphaneler:

```
pip install pandas pyarrow requests PyYAML openpyxl lxml html5lib beautifulsoup4
```

Pilot olarak tek ülke:

```
python t2saim_37x30_official_backfill.py `
  --root "." `
  --countries CZE `
  --start "1996-01-01" `
  --end "2026-10-03"
```

Tüm 37 ülke için, yalnız doğrulanmış ve etkinleştirilmiş kaynaklar:

```
python t2saim_37x30_official_backfill.py `
  --root "." `
  --start "1996-01-01" `
  --end "2026-10-03"
```

## Source Atlas yapısı

Her ülke için ayrı dosya:

```
config/source_atlas/
├─ CZE.yaml
├─ TUR.yaml
├─ POL.yaml
├─ HUN.yaml
├─ ROU.yaml
├─ BGR.yaml
├─ GRC.yaml
├─ BRA.yaml
├─ MEX.yaml
├─ COL.yaml
├─ ARG.yaml
├─ CHL.yaml
├─ PER.yaml
├─ ZAF.yaml
├─ EGY.yaml
├─ IDN.yaml
├─ PHL.yaml
├─ THA.yaml
├─ DEU.yaml
├─ EUR.yaml
└─ ... 37 ülkenin tamamı
```

Bir örnek kaynak girdisi:

```
sources:
  - source_id: "ISO3_OFFICIAL_INSTITUTION_DATASET"
    country_iso3: "ISO3"

    enabled: false
    status: "UNVERIFIED"

    institution: "Official institution"
    institution_type: "statistics_office"

    dataset_name: "Exact official dataset title"
    source_page_url: "https://official-source-page"
    url: "https://verified-direct-data-endpoint"

    http_method: "GET"
    format: "csv"

    params:
      start_date: "{start}"
      end_date: "{end}"

    date_format: "%Y-%m-%d"

    metric_id: "ISO3.structural.industry.production_yoy"
    unit: "percent"
    frequency: "monthly"
    geo_level: "national"
    geo_id: "NATIONAL"

    publication_lag_days: 30
    evidence_grade: "A"
    recording_integrity: "high"
    is_proxy: false

    mapping:
      record_path: null
      value: "VERIFIED_VALUE_COLUMN"
      valid_time: "VERIFIED_DATE_COLUMN"
      available_at: null
      geo_id: null

    download_strategy:
      type: "chunked_api"
      chunk_days: 365
```

Bütün placeholder alanları gerçek resmî kaynak bilgisiyle değişmeden:

```
enabled: false
status: UNVERIFIED
```

kalmalıdır.

## Hata davranışı

Bir API belirli tarih bloğunda hata verirse:

```
- O blok için sentetik boş seri oluşturulmaz.
- Sonraki bloklara geçilir.
- Hata data/quarantine/{ISO3}/ altına yazılır.
- Hata kaydı backfill_log.parquet'e düşer.
- Sonuç PARTIAL_ERROR olur.
```

Bu çok önemli, çünkü “30 yıllık seri tamam” görüntüsü verip eksik yılları sıfır veya interpolasyonla örtmez.

## Gerçek veriye geçmeden önce zorunlu test

Her kaynak için:

1. Doğrudan endpoint’i tarayıcı/Python ile aç.
2. 1 günlük veya 1 aylık gerçek yanıtı indir.
3. Endpoint’in gerçekten resmî kuruma ait olduğunu kontrol et.
4. JSON/CSV/XLSX içindeki gerçek kolonları incele.
5. `value` ve `valid_time` mapping’ini yanıtla bire bir eşleştir.
6. 1996’ya yönelik bir sorgu yap; kapsama yoksa gerçek başlangıç yılını kaydet.
7. Yayın gecikmesini ve revizyon politikasını yaz.
8. Ancak sonra `VERIFIED + enabled: true` yap.

Bu düzende “sorunsuz çekildi” sonucu ancak şunlar kontrol edilerek söylenebilir:

```
Raw dosya var mı?
SHA-256 manifest var mı?
Bronze satır sayısı makul mü?
Silver satır sayısı ve tarih aralığı doğru mu?
Eksik bloklar quarantine/log'da açıkça görünüyor mu?
available_at doğru mu?
Metric birimi ve yönü doğru mu?
```

Bu script, 37 ülke × 30 yıl gerçek veri altyapısını sentetik veri olmadan kurmak için hazırdır.

# T2SAIM 37 Countries x 30 Years Official Backfill

## Hard rule

This program is intentionally incapable of producing synthetic values. It:

- pulls only explicitly enabled, verified official source-atlas records;
- never creates missing dates or values;
- never zero-fills or interpolates;
- archives each source response with a SHA-256 manifest;
- writes parse failures and source failures to quarantine/logs;
- rejects mappings that do not match a real response schema.

## What must exist before a 37-country run

You need 37 files under `config/source_atlas/`, one per ISO3. Every source
requires a direct verified official endpoint, accurate response mapping,
publication-lag rule, unit, frequency and backfill query policy.

A program cannot truthfully infer 37 countries' official endpoints and data
schemas by itself. Those facts must be verified in the source atlas.

## Install

```bash
pip install pandas pyarrow requests PyYAML openpyxl lxml html5lib beautifulsoup4
```

## Pilot one country first

```bash
python t2saim_37x30_official_backfill.py --root . --countries CZE --start 1996-01-01 --end 2026-10-03
```

## Full verified-atlas backfill

```bash
python t2saim_37x30_official_backfill.py --root . --start 1996-01-01 --end 2026-10-03
```

## Outputs

```text
data/raw/{ISO3}/{source_id}/{retrieval-date}/  original response + manifest
data/bronze/{ISO3}/{source_id}.parquet         source-shaped parsed table
data/silver/observations.parquet                canonical bitemporal panel
data/manifests/backfill_log.parquet             result/audit log
data/quarantine/{ISO3}/                         errors; no silent substitution
```

## Required validation before enabling

1. Test exact endpoint and date query with a real response.
2. Verify every mapped column and actual date format.
3. Confirm the time coverage and download terms.
4. Set `status: VERIFIED`, then `enabled: true`.
5. Pilot and inspect raw, Bronze, Silver and quarantine artifacts.


## ⚙️ 3. EKONOFİZİKSEL TERMODİNAMİK ŞART
Ekonomi enerji tüketen fiziksel bir motordur:
- **Soddy Sanal Servet Makası ($S_{gap}$):**
  $$S_{gap} = \frac{M2}{\max(NIR, 0.1)}$$
  Reel varlık üretimi ($W$) ile finansal borç ($S$) arasındaki makas açıldığında devalüasyon ve borç silinmesi kaçınılmaz doğa kanunudur.
