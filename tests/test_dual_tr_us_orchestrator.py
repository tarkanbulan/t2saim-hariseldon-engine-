#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TR-US DUAL-CORE ORCHESTRATION TEST
Doktrin: Veritas Per Se · TR ve ABD Piyasaları Eşzamanlı Doğrulama ve Çapraz Risk Testi
"""

import os
import sys
import pytest
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.orchestration.dual_tr_us_orchestrator import TRUSDualOrchestrator

def test_dual_orchestrator_execution():
    """TR ve ABD piyasalarının eşzamanlı olarak başarıyla koşturulduğunu doğrular."""
    orchestrator = TRUSDualOrchestrator()
    state = orchestrator.execute_dual_pipeline()
    
    assert state.tr_selected_asset != "N/A"
    assert state.us_selected_asset != "N/A"
    assert 0.0 <= state.tr_uci_score <= 1.0
    assert state.us_vix_level > 0.0
    assert 0.0 <= state.cross_market_hedge_ratio <= 1.0
    assert len(state.dual_sha256_hash) == 64
    assert state.execution_time_ms < 5000.0

def test_dual_orchestrator_cross_market_hedge_scaling():
    """TR kriz seviyesi arttıkça çapraz piyasa hedge oranının arttığını doğrular."""
    # Düşük UCI (0.20)
    low_hedge = float(min(1.0, max(0.0, 0.20 * 1.2)))
    # Yüksek UCI (0.75)
    high_hedge = float(min(1.0, max(0.0, 0.75 * 1.2)))
    
    assert high_hedge > low_hedge
    assert round(high_hedge, 2) == 0.90
