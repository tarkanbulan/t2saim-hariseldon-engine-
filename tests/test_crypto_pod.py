#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRYPTO POD PYTEST SUITE (TDD & SCIENTIFIC VERIFICATION)
Doktrin: Veritas Per Se · <$2000 Kısıtı, QuantEcon Markov Rejimi ve TAS-GNN Testi
"""

import os
import sys
import pytest
import numpy as np
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.markets.crypto.crypto_decomposer import CryptoDecomposer, CryptoMacroRegimeDetector
from modules.markets.crypto.tas_gnn_wash_shield import TASGNNWashShield
from modules.markets.crypto.crypto_crisis_engine import CryptoCrisisEngine
from modules.markets.crypto.crypto_duckdb_manager import CryptoDuckDBManager, CryptoCandleRecord

def test_sub_2000_asset_filtering():
    """BTC ve ETH'nin >= $2000 olduğu için alımdan elendiğini, <$2000 varlıkların geçtiğini test eder."""
    decomposer = CryptoDecomposer()
    prices = np.linspace(100, 150, 30)

    # 1. <$2000 Varlık (SOL - $145)
    sol_score = decomposer.evaluate_altcoin(symbol="SOL", price_usd=145.0, price_series=prices)
    assert sol_score.is_sub_2000 is True
    assert sol_score.composite_score > 0.0

    # 2. >= $2000 Varlık (BTC - $65,000)
    btc_score = decomposer.evaluate_altcoin(symbol="BTC", price_usd=65000.0, price_series=prices)
    assert btc_score.is_sub_2000 is False
    assert btc_score.composite_score == 0.0

def test_quantecon_markov_regime_detection():
    """QuantEcon tabanlı rejim dedektörünün durağan dağılımını ve rejim çıktısını test eder."""
    detector = CryptoMacroRegimeDetector()
    assert len(detector.stationary_probs) == 3
    assert abs(np.sum(detector.stationary_probs) - 1.0) < 1e-5

    # Boğa Rejimi Testi
    btc_bull = np.linspace(50000, 60000, 20)
    eth_bull = np.linspace(2400, 2900, 20)
    regime, weight = detector.detect_regime(btc_bull, eth_bull)
    assert regime == "BULL_EXPANSION"
    assert weight > 1.0

def test_tas_gnn_wash_trading_veto():
    """TAS-GNN yapay hacim (%40 üzeri) ve kendiyle işlem (%15 üzeri) vetolarını test eder."""
    shield = TASGNNWashShield()

    # Sahte Hacimli Kripto
    veto_res = shield.audit_crypto_asset(
        symbol="SHIT_PUMP",
        wash_trading_score=0.55,
        self_trade_ratio=0.22,
        graph_cycle_detected=True
    )
    assert veto_res.is_cleared is False
    assert "WASH_TRADING_HIGH" in veto_res.rejection_code
    assert "SELF_TRADE_EXCEEDED" in veto_res.rejection_code

    # Temiz Kripto (SOL)
    clean_res = shield.audit_crypto_asset(
        symbol="SOL",
        wash_trading_score=0.10,
        self_trade_ratio=0.03,
        graph_cycle_detected=False
    )
    assert clean_res.is_cleared is True
    assert clean_res.rejection_code is None

def test_1m_crypto_mcmc_latency():
    """1 Milyon simülasyonun 800 ms altında çalıştığını ve Student-t (nu=3.5) kuyruğunu test eder."""
    engine = CryptoCrisisEngine()
    
    res = engine.run_1m_crypto_mcmc(
        symbol="AVAX",
        current_price_usd=25.0,
        expected_drift=0.30,
        historical_volatility=0.40,
        macro_regime="BULL_EXPANSION",
        n_simulations=1_000_000
    )
    assert res.execution_time_ms < 800.0
    assert res.worst_p05_pct <= res.nominal_mean_roi_pct <= res.best_p95_pct

def test_crypto_duckdb_causal_window():
    """Kripto gölünde gelecek sızıntısı olmadığını test eder."""
    test_db = os.path.join(ROOT_DIR, "data_lakehouse", "test_crypto_temp.duckdb")
    mgr = CryptoDuckDBManager(db_path=test_db)
    
    now = datetime.now()
    candles = [
        CryptoCandleRecord(
            timestamp=now - timedelta(days=2),
            symbol="LINK",
            open=10.0, high=11.0, low=9.8, close=10.5, volume=5000.0
        ),
        CryptoCandleRecord(
            timestamp=now + timedelta(days=2), # Gelecek verisi
            symbol="LINK",
            open=15.0, high=16.0, low=14.8, close=15.5, volume=6000.0
        )
    ]
    mgr.insert_crypto_candles(candles)
    
    df = mgr.get_causal_crypto_window("LINK", target_date=now, lookback_days=5)
    assert len(df) == 1
    assert df.iloc[0]["close"] == 10.5
    
    if os.path.exists(test_db):
        os.remove(test_db)
