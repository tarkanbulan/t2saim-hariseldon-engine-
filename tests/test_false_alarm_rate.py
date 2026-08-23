import os
import sys
import pytest
import numpy as np
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from t2saim_crisis_engine.engine.sensor import UnifiedCrisisSensor
from t2saim_crisis_engine.core.schemas import TelemetryInput

def test_false_alarm_rate_under_calibrated_threshold():
    """Normal piyasa koşullarında yanlış alarm oranının %7.3'ün altında kaldığını test eder."""
    sensor = UnifiedCrisisSensor()
    
    n_days = 200
    false_alarms = 0
    
    # 200 günlük normal / düşük stresli sentetik piyasa akışı
    for i in range(n_days):
        telemetry = TelemetryInput(
            timestamp=datetime.now(),
            m2_nir_ratio=8.0 + np.random.uniform(0, 2.0),
            net_nir_usd_billion=5.0 + np.random.uniform(0, 3.0),
            reer_cpi=52.0 + np.random.uniform(0, 3.0),
            ext_debt_service_1y_billion=191.0,
            dolgap_premium_pct=0.20 + np.random.uniform(0, 0.3),
            ldr_ratio=0.92 + np.random.uniform(0, 0.05),
            npl_real_ratio=1.9,
            npl_official_ratio=1.7,
            ted_spread_pct=1.5 + np.random.uniform(0, 0.5),
            uyap_active_cases_million=18.0,
            bounced_checks_billion_tl=40.0,
            sigma_20_60_ratio=1.0,
            v_run=0.15,
            h_herd=0.20,
            fatalism_buffer=1.1,
            cds_5y=210.0,
            tcmb_trust_deficit=0.25,
            procurement_hhi=1600.0,
            kik_21b_ratio=0.12,
            rent_to_mfg_credit=1.3,
            lm1_caliper_cv=0.22,
            tr_dei_score=0.30
        )
        
        output = sensor.evaluate(telemetry)
        if output.recommended_action == "CASH_100_VIOP_HEDGE":
            false_alarms += 1

    false_alarm_rate = (false_alarms / n_days) * 100.0
    print(f"Normal Piyasa Yanlış Alarm Oranı: %{false_alarm_rate:.2f}")
    assert false_alarm_rate <= 7.3

def test_full_crisis_trigger_sensitivity():
    """Derin kriz telemetrisinde sistemin %100 alarm verdiğini doğrular."""
    sensor = UnifiedCrisisSensor()
    
    crisis_telemetry = TelemetryInput(
        timestamp=datetime.now(),
        m2_nir_ratio=22.0,
        net_nir_usd_billion=-58.0,
        reer_cpi=74.0,
        ext_debt_service_1y_billion=191.0,
        dolgap_premium_pct=4.8,
        ldr_ratio=1.28,
        npl_real_ratio=5.5,
        npl_official_ratio=1.6,
        ted_spread_pct=6.5,
        uyap_active_cases_million=28.0,
        bounced_checks_billion_tl=90.0,
        sigma_20_60_ratio=1.8,
        v_run=0.88,
        h_herd=0.85,
        fatalism_buffer=0.60,
        cds_5y=380.0,
        tcmb_trust_deficit=0.85,
        procurement_hhi=3800.0,
        kik_21b_ratio=0.45,
        rent_to_mfg_credit=2.9,
        lm1_caliper_cv=0.08,
        tr_dei_score=0.85
    )
    
    # 3 adımda bellek yükünü biriktir
    for _ in range(3):
        out = sensor.evaluate(crisis_telemetry)
        
    assert out.uci_score > 0.65
    assert out.recommended_action == "CASH_100_VIOP_HEDGE"
    assert out.tactical_state_d14 == "TACTICAL_CRISIS_ALARM"
