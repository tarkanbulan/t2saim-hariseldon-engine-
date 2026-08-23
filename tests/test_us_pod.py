#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM US POD PYTEST SUITE (TDD & SCIENTIFIC VERIFICATION)
Doktrin: Veritas Per Se · <$1000 Kısıtı, VIX Volatilite Kalkanı ve 1M MCMC Testi
"""

import os
import sys
import pytest
import numpy as np
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.markets.us.us_decomposer import USDecomposer, USMacroCompass
from modules.markets.us.vix_volatility_shield import VIXVolatilityShield
from modules.markets.us.us_crisis_engine import USCrisisEngine
from modules.markets.us.us_duckdb_manager import USDuckDBManager, USCandleRecord

def test_us_sub_1000_filtering():
    """$1000 üzeri hisselerin elendiğini, <$1000 hisselerin puanlandığını test eder."""
    decomposer = USDecomposer()
    prices = np.linspace(30, 45, 30)

    # 1. <$1000 Hisse (PLTR - $35)
    pltr_score = decomposer.evaluate_us_stock(symbol="PLTR", price_usd=35.0, price_series=prices)
    assert pltr_score.is_sub_1000 is True
    assert pltr_score.composite_score > 0.0

    # 2. >= $1000 Hisse (Örn: $3,500)
    exp_score = decomposer.evaluate_us_stock(symbol="EXPENSIVE", price_usd=3500.0, price_series=prices)
    assert exp_score.is_sub_1000 is False
    assert exp_score.composite_score == 0.0

def test_vix_volatility_shield_veto():
    """VIX >= 28.5 ve Delta_VIX >= %20 durumlarında kalkanın veto verdiğini test eder."""
    shield = VIXVolatilityShield()

    # 1. Mutlak Yüksek VIX (32.0)
    high_vix = shield.audit_us_market(current_vix=32.0, previous_vix=30.0)
    assert high_vix.is_cleared is False
    assert "VIX_ABSOLUTE_CRITICAL" in high_vix.rejection_code

    # 2. Ani VIX Sıçraması (15.0'dan 21.0'a -> +%40 artış)
    spike_vix = shield.audit_us_market(current_vix=21.0, previous_vix=15.0)
    assert spike_vix.is_cleared is False
    assert "VIX_DAILY_SPIKE_EXCEEDED" in spike_vix.rejection_code

    # 3. Sakin Piyasa (VIX = 14.5)
    calm_vix = shield.audit_us_market(current_vix=14.5, previous_vix=14.8)
    assert calm_vix.is_cleared is True
    assert calm_vix.market_state == "CALM_FLOW"

def test_us_macro_compass():
    """SPY/QQQ/VIX rejim tespitini doğrular."""
    compass = USMacroCompass()
    spy = np.linspace(540, 560, 20)
    qqq = np.linspace(460, 480, 20)
    
    regime, weight = compass.compute_regime(spy, qqq, vix_level=14.5)
    assert regime == "RISK_ON_AI_EXPANSION"
    assert weight > 1.0

def test_1m_us_mcmc_latency():
    """1 Milyon ABD hisse simülasyonunun 800 ms altında çalıştığını test eder."""
    engine = USCrisisEngine()
    
    res = engine.run_1m_us_mcmc(
        symbol="VST",
        current_price_usd=125.0,
        expected_drift=0.30,
        historical_volatility=0.35,
        horizon_days=30,
        n_simulations=1_000_000
    )
    assert res.execution_time_ms < 800.0
    assert res.worst_p05_pct <= res.nominal_mean_roi_pct <= res.best_p95_pct

def test_us_duckdb_causal_window():
    """ABD veri gölünde nedensellik ve sıfır gelecek sızıntısı olduğunu test eder."""
    test_db = os.path.join(ROOT_DIR, "data_lakehouse", "test_us_temp.duckdb")
    mgr = USDuckDBManager(db_path=test_db)
    
    now = datetime.now()
    candles = [
        USCandleRecord(
            timestamp=now - timedelta(days=5),
            symbol="NVDA",
            open=120.0, high=125.0, low=119.0, close=124.0, volume=1000000.0, sector="AI_HARDWARE"
        ),
        USCandleRecord(
            timestamp=now + timedelta(days=5), # Gelecek verisi
            symbol="NVDA",
            open=140.0, high=145.0, low=139.0, close=144.0, volume=1000000.0, sector="AI_HARDWARE"
        )
    ]
    mgr.insert_us_candles(candles)
    
    df = mgr.get_causal_us_window("NVDA", target_date=now, lookback_days=10)
    assert len(df) == 1
    assert df.iloc[0]["close"] == 124.0
    
    if os.path.exists(test_db):
        os.remove(test_db)
