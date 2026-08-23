#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TURKEY CRISIS ENGINE MASTER ENTRYPOINT & FASTMCP SERVER
Doktrin: Veritas Per Se · Port 39300 & Uçtan Uca Telemetri Değerlendiricisi
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from t2saim_crisis_engine.engine.sensor import UnifiedCrisisSensor
from t2saim_crisis_engine.engine.execution_router import ExecutionRouter
from t2saim_crisis_engine.core.schemas import TelemetryInput
from t2saim_crisis_engine.database.duckdb_store import CrisisDuckDBStore
from t2saim_crisis_engine.database.sqlite_telemetry import SQLiteTelemetryLogger

def run_sample_evaluation():
    sensor = UnifiedCrisisSensor()
    router = ExecutionRouter()
    duckdb_store = CrisisDuckDBStore()
    sqlite_logger = SQLiteTelemetryLogger()

    # Örnek Güncel Telemetri Verisi (Prometheus & EVDS Eşleşmesi)
    sample_input = TelemetryInput(
        timestamp=datetime.now(),
        m2_nir_ratio=16.8,
        net_nir_usd_billion=-48.5,
        reer_cpi=69.2,
        ext_debt_service_1y_billion=191.0,
        dolgap_premium_pct=1.45,
        ldr_ratio=1.18,
        npl_real_ratio=4.8,
        npl_official_ratio=1.7,
        ted_spread_pct=4.2,
        uyap_active_cases_million=25.4,
        bounced_checks_billion_tl=72.0,
        sigma_20_60_ratio=1.45,
        v_run=0.72,
        h_herd=0.68,
        fatalism_buffer=0.80,
        cds_5y=270.0,
        tcmb_trust_deficit=0.65,
        procurement_hhi=2950.0,
        kik_21b_ratio=0.38,
        rent_to_mfg_credit=2.6,
        lm1_caliper_cv=0.11,
        tr_dei_score=0.72
    )

    output = sensor.evaluate(sample_input)
    routing = router.route_portfolio(output)
    
    duckdb_store.save_crisis_output(output)
    sqlite_logger.log_evaluation(sample_input, output)

    print("\n" + "=" * 80)
    print("🛰️ T2SAIM TÜRKİYE BİRLEŞİK KRİZ ERKEN UYARI SENSÖRÜ (v5.0)")
    print("=" * 80)
    print(f"📊 BİRLEŞİK KRİZ İNDEKSİ (UCI) : %{output.uci_score * 100:.2f} (Aralık: [%{output.confidence_interval_p0*100:.1f} - %{output.confidence_interval_p1*100:.1f}])")
    print(f"⚡ TAKTİKSEL DURUM (D+14 Gün) : {output.tactical_state_d14}")
    print(f"🏛️ STRATEJİK DURUM (M+3 Ay)   : {output.strategic_state_m3}")
    print(f"🛡️ PORTFÖY EYLEM TAVSİYESİ    : {output.recommended_action} ──► {routing['hedge_status']}")
    print(f"💰 ÇEYREK KELLY KATSAYISI     : {output.quarter_kelly_fraction}")
    print("-" * 80)
    print("📈 5 BOYUTLU FAZ SKORLARI:")
    print(f"   • Phi_Macro   : {output.phi_macro} (Minsky & Rezerv)")
    print(f"   • Phi_Bank    : {output.phi_bank} (Likidite & Hayalet Kredi)")
    print(f"   • Phi_Neuro   : {output.phi_neuro} (Amigdala & Kaçış Hızı)")
    print(f"   • Phi_Gullini : {output.phi_gullini} (Güvensizlik & 18 Kasım Tekilliği)")
    print(f"   • Phi_Acemoglu: {output.phi_acemoglu} (TR-DEI & İhale Kilitlenmesi)")
    print("-" * 80)
    print("🔍 TREESHAP ETKİ DAĞILIMI:")
    for f in output.top_shap_factors:
        print(f"   - {f.factor_name:<36}: %{f.weight_pct:.1f} (Katkı: {f.contribution_score:.4f})")
    print("=" * 80 + "\n")

    return output

if __name__ == "__main__":
    run_sample_evaluation()
