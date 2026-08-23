#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRISIS ENGINE E2E SENSOR INTEGRATION TEST
Doktrin: Veritas Per Se · Sensör, Yönlendirici, DuckDB ve SQLite Entegrasyon Doğrulaması
"""

import os
import pytest
from datetime import datetime
from t2saim_crisis_engine.engine.sensor import UnifiedCrisisSensor
from t2saim_crisis_engine.engine.execution_router import ExecutionRouter
from t2saim_crisis_engine.core.schemas import TelemetryInput
from t2saim_crisis_engine.database.duckdb_store import CrisisDuckDBStore
from t2saim_crisis_engine.database.sqlite_telemetry import SQLiteTelemetryLogger

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_full_crisis_sensor_e2e_pipeline():
    """Tüm kriz boru hattının E2E çalıştığını doğrular."""
    sensor = UnifiedCrisisSensor()
    router = ExecutionRouter()
    
    test_duckdb = os.path.join(ROOT_DIR, "data_lakehouse", "test_sensor_temp.duckdb")
    test_sqlite = os.path.join(ROOT_DIR, "data_lakehouse", "test_sensor_temp.sqlite")
    
    duckdb_store = CrisisDuckDBStore(db_path=test_duckdb)
    sqlite_logger = SQLiteTelemetryLogger(db_path=test_sqlite)
    
    telemetry = TelemetryInput(
        timestamp=datetime.now(),
        m2_nir_ratio=15.5,
        net_nir_usd_billion=-45.0,
        reer_cpi=68.5,
        ext_debt_service_1y_billion=191.0,
        dolgap_premium_pct=1.8,
        ldr_ratio=1.16,
        npl_real_ratio=4.5,
        npl_official_ratio=1.8,
        ted_spread_pct=3.8,
        uyap_active_cases_million=25.0,
        bounced_checks_billion_tl=70.0,
        sigma_20_60_ratio=1.35,
        v_run=0.65,
        h_herd=0.60,
        fatalism_buffer=0.85,
        cds_5y=265.0,
        tcmb_trust_deficit=0.60,
        procurement_hhi=2850.0,
        kik_21b_ratio=0.35,
        rent_to_mfg_credit=2.5,
        lm1_caliper_cv=0.12,
        tr_dei_score=0.68
    )
    
    output = sensor.evaluate(telemetry)
    assert 0.0 <= output.uci_score <= 1.0
    assert output.confidence_interval_p0 <= output.confidence_interval_p1
    assert len(output.top_shap_factors) == 5
    
    routing = router.route_portfolio(output)
    assert "target_allocation" in routing
    assert sum(routing["target_allocation"].values()) == 1.0
    
    duckdb_store.save_crisis_output(output)
    sqlite_logger.log_evaluation(telemetry, output)
    
    # Güvenli temizlik (dosya silme hatası testi engellemez)
    try:
        if os.path.exists(test_duckdb):
            os.remove(test_duckdb)
        if os.path.exists(test_sqlite):
            os.remove(test_sqlite)
    except Exception:
        pass
