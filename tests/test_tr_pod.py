#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TURKEY POD PYTEST SUITE (TDD & SCIENTIFIC VERIFICATION)
Doktrin: Veritas Per Se · Mekanik Amnezi, Hurst Doğrulaması ve %0 Stopaj Testi
"""

import os
import sys
import pytest
import numpy as np
from datetime import datetime, timedelta

# Path ekleme
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.markets.tr.bist_decomposer import compute_hurst_fast, BISTDecomposer
from modules.markets.tr.takas_fraud_shield import TakasFraudShield
from modules.markets.tr.tr_crisis_engine import TRCrisisEngine
from modules.markets.tr.tr_duckdb_manager import TRDuckDBManager, BISTCandleRecord

def test_hurst_computation():
    """Hızlı Hurst üssünün geçerlilik aralığını (0.05 <= h <= 0.95) test eder."""
    # 1. Kalıcı trend serisi (Persistent)
    trend_series = np.linspace(10, 100, 100) + np.random.normal(0, 1, 100)
    h_trend = compute_hurst_fast(trend_series)
    assert 0.05 <= h_trend <= 0.95
    assert h_trend > 0.40  # Trend serisinde h yüksek çıkmalı

    # 2. Rastgele yürüyüş (Random walk)
    rw_series = np.cumsum(np.random.normal(0, 1, 100))
    h_rw = compute_hurst_fast(rw_series)
    assert 0.05 <= h_rw <= 0.95

def test_takas_fraud_shield_veto():
    """Sahte tahta (C_takas >= 0.70 ve R_cancel >= 0.85) manipülasyonunun vetolandığını test eder."""
    shield = TakasFraudShield()
    
    # Manipülatif tahta
    bad_audit = shield.audit_bist_equity(
        symbol="SPOOF_HISSE",
        c_takas=0.82,
        r_cancel=0.91,
        vpin=0.55
    )
    assert bad_audit.is_cleared is False
    assert "C_TAKAS_EXCEEDED" in bad_audit.rejection_code
    assert "R_CANCEL_SPOOFING" in bad_audit.rejection_code

def test_takas_fraud_shield_pass():
    """Temiz ve organik tahtanın filtreden geçtiğini test eder."""
    shield = TakasFraudShield()
    
    good_audit = shield.audit_bist_equity(
        symbol="ASELS",
        c_takas=0.45,
        r_cancel=0.20,
        vpin=0.15
    )
    assert good_audit.is_cleared is True
    assert good_audit.rejection_code is None
    assert good_audit.risk_score < 0.50

def test_1m_mcmc_latency_and_distribution():
    """1 Milyon simülasyonun 500 ms altında çalıştığını ve uç değer sıralamasını test eder."""
    engine = TRCrisisEngine()
    
    result = engine.run_1m_vectorized_mcmc(
        symbol="ASELS",
        current_price=58.50,
        expected_drift=0.20,
        historical_volatility=0.25,
        psi_tr=0.65,
        horizon_days=20,
        n_simulations=1_000_000
    )
    
    # Hız doğrulaması (<500 ms)
    assert result.execution_time_ms < 500.0
    # Sıralama doğrulaması (p05 <= mean <= p95)
    assert result.nominal_p05_worst <= result.nominal_mean_roi <= result.nominal_p95_best
    assert result.gvk_tax_deduction == 0.0

def test_gvk_67_zero_tax_real_profit():
    """GVK Geçici 67 %0 Stopaj kuralını ve reel alım gücü getirisini garanti altına alır."""
    engine = TRCrisisEngine(friction=0.0006)
    
    # %15 nominal getiri, %2.5 aylık enflasyon, %1.5 kur artışı
    res = engine.run_1m_vectorized_mcmc(
        symbol="THYAO",
        current_price=300.0,
        expected_drift=0.30,
        historical_volatility=0.20,
        psi_tr=0.30,
        horizon_days=20,
        monthly_inflation=0.025,
        monthly_fx_change=0.015
    )
    
    assert res.gvk_tax_deduction == 0.0
    # Reel kâr hesabı matematiksel olarak doğrulanmalı
    nominal_frac = res.nominal_mean_roi / 100.0
    expected_real = ((1.0 + nominal_frac) / (1.0 + 0.040)) - 1.0 - 0.0006
    assert abs((res.real_net_profit / 100.0) - expected_real) < 0.01

def test_duckdb_causal_window():
    """Mekanik Amnezi: Gelecek sızıntısı olmadığını test eder."""
    test_db = os.path.join(ROOT_DIR, "data_lakehouse", "test_temp.duckdb")
    mgr = TRDuckDBManager(db_path=test_db)
    
    now = datetime.now()
    candles = [
        BISTCandleRecord(
            timestamp=now - timedelta(days=5),
            symbol="TEST_SYM",
            sector="TECH",
            open=10.0, high=12.0, low=9.5, close=11.0, volume=1000.0
        ),
        BISTCandleRecord(
            timestamp=now + timedelta(days=5), # Gelecek verisi
            symbol="TEST_SYM",
            sector="TECH",
            open=20.0, high=22.0, low=19.5, close=21.0, volume=2000.0
        )
    ]
    mgr.insert_bist_candles(candles)
    
    # now anındaki sorgu sadece geçmişteki 1 kaydı getirmeli, gelecekteki 2. kaydı GÖRMEMELİ
    causal_df = mgr.get_causal_bist_window("TEST_SYM", target_date=now, lookback_days=10)
    assert len(causal_df) == 1
    assert causal_df.iloc[0]["close"] == 11.0
    
    # Temizlik
    if os.path.exists(test_db):
        os.remove(test_db)
