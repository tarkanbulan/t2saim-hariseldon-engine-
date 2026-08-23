#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM COMMODITY POD PYTEST SUITE (TDD & SCIENTIFIC VERIFICATION)
Doktrin: Veritas Per Se · Süper Döngü Hurst, Contango Kalkanı ve 1M MCMC Testi
"""

import os
import sys
import pytest
import numpy as np
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.markets.commodity.commodity_decomposer import CommodityDecomposer, CommodityMacroCompass
from modules.markets.commodity.contango_roll_shield import ContangoRollShield
from modules.markets.commodity.commodity_crisis_engine import CommodityCrisisEngine
from modules.markets.commodity.commodity_duckdb_manager import CommodityDuckDBManager, CommodityCandleRecord

def test_super_commodity_ranking_and_hurst():
    """Süper emtia Hurst hesabı ve puanlamasını test eder."""
    decomposer = CommodityDecomposer()
    
    # Kalıcı süper döngü trendi (Hurst >= 0.60)
    prices_trending = np.array([100.0 * (1.005**i) for i in range(50)])
    h_trend = decomposer.compute_fast_hurst(prices_trending)
    assert h_trend >= 0.55

    score = decomposer.evaluate_commodity(
        symbol="COCOA",
        spot_price=7800.0,
        price_series=prices_trending,
        roll_yield_pct=0.008,
        physical_deficit_score=0.95
    )
    assert score.is_super_cycle_active is True
    assert score.composite_score > 60.0

def test_contango_roll_bleed_veto():
    """Contango kalkanının sermaye kanamasını vetoladığını ve fiziksel tröstleri koruduğunu test eder."""
    shield = ContangoRollShield()

    # 1. Derin Contango Sermaye Tuzağı (F1 = 105, F0 = 100 -> %-5.0 Roll)
    veto_res = shield.audit_commodity_curve(
        symbol="NAT_GAS_TRAP",
        front_month_price=100.0,
        next_month_price=105.0
    )
    assert veto_res.is_cleared is False
    assert "CONTANGO_ROLL_BLEED_EXCEEDED" in veto_res.rejection_code

    # 2. Backwardation / Pozitif Taşıma (F1 = 98, F0 = 100)
    pass_res = shield.audit_commodity_curve(
        symbol="SILVER",
        front_month_price=100.0,
        next_month_price=98.0
    )
    assert pass_res.is_cleared is True
    assert pass_res.curve_state == "BACKWARDATION"

    # 3. Darphane Altın Sertifikası (Fiziki Spot - Roll Maliyeti Sıfır)
    gold_res = shield.audit_commodity_curve(
        symbol="ALTIN.S1",
        front_month_price=34.0,
        next_month_price=34.0
    )
    assert gold_res.is_cleared is True
    assert gold_res.curve_state == "PHYSICAL_SPOT_BACKED"

def test_macro_compass_multiplier():
    """Altın ve Petrol pusulasının enflasyon / gerilim katsayısını test eder."""
    compass = CommodityMacroCompass()
    
    gold_bull = np.linspace(2400, 2550, 20)
    oil_bull = np.linspace(75, 82, 20)
    
    mult, regime = compass.compute_compass_multiplier(gold_bull, oil_bull)
    assert mult > 1.0
    assert regime == "GLOBAL_INFLATION_SURGE"

def test_1m_commodity_mcmc_latency():
    """1 Milyon emtia simülasyonunun 800 ms altında çalıştığını test eder."""
    engine = CommodityCrisisEngine()
    
    res = engine.run_1m_commodity_mcmc(
        symbol="URANIUM",
        current_spot_price=85.0,
        expected_drift=0.25,
        historical_volatility=0.30,
        horizon_months=18,
        n_simulations=1_000_000
    )
    assert res.execution_time_ms < 800.0
    assert res.worst_p05_pct <= res.nominal_mean_roi_pct <= res.best_p95_pct

def test_commodity_duckdb_causal_window():
    """Emtia veri gölünde nedensellik ve sıfır gelecek sızıntısı olduğunu test eder."""
    test_db = os.path.join(ROOT_DIR, "data_lakehouse", "test_commodity_temp.duckdb")
    mgr = CommodityDuckDBManager(db_path=test_db)
    
    now = datetime.now()
    candles = [
        CommodityCandleRecord(
            timestamp=now - timedelta(days=5),
            symbol="COPPER",
            spot_price=4.20, front_month_futures=4.20, next_month_futures=4.19
        ),
        CommodityCandleRecord(
            timestamp=now + timedelta(days=5), # Gelecek verisi
            symbol="COPPER",
            spot_price=5.00, front_month_futures=5.00, next_month_futures=4.99
        )
    ]
    mgr.insert_commodity_candles(candles)
    
    df = mgr.get_causal_commodity_window("COPPER", target_date=now, lookback_days=10)
    assert len(df) == 1
    assert df.iloc[0]["spot_price"] == 4.20
    
    if os.path.exists(test_db):
        os.remove(test_db)
