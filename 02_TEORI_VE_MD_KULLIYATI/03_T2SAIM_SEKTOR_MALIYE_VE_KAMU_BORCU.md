# 🏛️ T2SAIM SEKTÖREL KÜTÜPHANE: MALİYE, KAMU BORCU VE VERGİ KAPASİTESİ
**Mühür:** VERITAS PER SE  
**Konum:** `10_SEKTOREL_VE_TEMATIK_KUTUPHANELER/03_Maliye`  
**Rolü:** Devlet mali alanı (Fiscal Space), Ponzi borç dinamikleri ve iflas eşikleri.

---

## 📑 1. MALİ METRİK SÖZLEŞMESİ (FISCAL METRIC CONTRACT)
```yaml
# T2SAIM global Fiscal, Public-Risk, Household and Refinancing metric contract
# Preserve absent series as missing; do not substitute non-equivalent sources.
metric_families:
  fiscal_revenue_quality:
    - fiscal.tax_revenue.to_gdp
    - fiscal.tax_collection.collection_to_assessment
    - fiscal.tax_collection.tax_arrears_to_tax_revenue
    - fiscal.tax_collection.average_days
    - fiscal.tax_composition.indirect_tax_share
    - fiscal.tax_composition.top3_concentration_hhi
    - fiscal.tax_oneoff_revenue.to_total_revenue
    - fiscal.tax_expenditure.to_gdp
    - fiscal.vat_refund.stock_to_gdp
    - fiscal.vat_refund.average_days
    - fiscal.revenue_forecast.error
  fiscal_balance_debt:
    - fiscal.balance.overall_to_gdp
    - fiscal.balance.primary_to_gdp
    - fiscal.debt.general_government_to_gdp
    - fiscal.debt.net_to_gdp
    - fiscal.debt.interest_expense_to_revenue
    - fiscal.debt.short_term_share
    - fiscal.debt.fx_share
    - fiscal.debt.variable_rate_share
    - fiscal.debt.average_residual_maturity_years
    - fiscal.debt.maturing_12m_to_revenue
    - fiscal.debt.maturing_12m_external_to_reserves
    - fiscal.debt.auction_yield_spread
    - fiscal.debt.nonresident_holder_share
  contingent_ppp_offbudget:
    - fiscal.guarantee.explicit_stock_to_gdp
    - fiscal.guarantee.called_amount_to_gdp
    - fiscal.guarantee.expected_loss_to_gdp
    - fiscal.ppp.total_exposure_to_gdp
    - fiscal.ppp.availability_payment_to_revenue
    - fiscal.ppp.minimum_revenue_guarantee_to_gdp
    - fiscal.soe.debt_to_gdp
    - fiscal.soe.losses_to_gdp
    - fiscal.public_bank.directed_credit_to_gdp
    - fiscal.local_government.debt_to_gdp
    - fiscal.offbudget_fund.assets_to_gdp
    - fiscal.offbudget_fund.liabilities_to_gdp
    - fiscal.legal_claims.exposure_to_gdp
  procurement_execution:
    - procurement.open_tender_share
    - procurement.single_bid_share
    - procurement.direct_award_share
    - procurement.contract_amendment_share
    - procurement.supplier_concentration_hhi
    - procurement.payment_delay_days
    - procurement.incomplete_project_share
  household_distribution:
    - household.debt.to_disposable_income
    - household.debt_service_ratio
    - household.variable_rate_debt_share
    - household.credit_card_debt.to_disposable_income
    - household.credit_card.delinquency_rate
    - household.consumer_credit.delinquency_rate
    - household.mortgage.delinquency_rate
    - household.utility_arrears_rate
    - household.rent_arrears_rate
    - household.enforcement_filings_rate
    - household.liquid_savings_to_income
    - distribution.gini_disposable_income
    - distribution.bottom40.real_income_growth
    - distribution.real_wage_growth
    - distribution.essential_basket_inflation
  firm_legal_cashflow:
    - firm.npl_sme_rate
    - firm.payment_delay_days
    - firm.bankruptcy_rate
    - firm.restructuring_filings_rate
    - legal.insolvency_filings_rate
    - legal.concordat_filings_rate
    - legal.enforcement_case_inflow_rate
    - legal.enforcement_case_stock_rate
mechanisms:
  - TAX_BASE_EROSION
  - PUBLIC_CASHFLOW_STRESS
  - HIDDEN_FISCAL_LIABILITY
  - PPP_FISCAL_TRANSFER_RISK
  - STATE_BANK_CORPORATE_NEXUS
  - HOUSEHOLD_DEBT_DISTRESS
  - DISTRIBUTIONAL_CONSUMPTION_STRESS
  - REFINANCING_WALL
  - FX_DEBT_VULNERABILITY
  - INTEREST_RATE_REFIXING_RISK

```

---

## 🔬 2. ADLİ KAMU BORCU VE VERGİ BASKISI FORMÜLLERİ
1. **Borç Dinamiği (Domar Şartı):**
   $$\Delta d_t = (r_t - g_t) d_{t-1} - pb_t$$
   Reel faiz ($r$) ekonomik büyümenin ($g$) üzerine çıktığında, faiz dışı fazla ($pb$) verilmezse kamu borcu geometrik olarak patlar.
2. **Vergi Çarpıstırması ve Bütçe Sürtünmesi ($\Phi$):**
   İdeolojik/verimsiz kamu harcamalarının üretken Ar-Ge ve beşeri sermaye yatırımlarını ezme katsayısı:
   $$\Phi = \frac{\text{İdeolojik/Cari Tüketim Bütçesi}}{\text{TÜBİTAK + Üniversite Ar-Ge Bütçesi}}$$
   $\Phi > 1.0$ aşıldığında sistemik üretkenlik erozyonu kaçınılmazdır.
