#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM US MARKET MASTER RUNNER & ORCHESTRATOR (TICKET-US-05)
Doktrin: Veritas Per Se · SPY/QQQ Pusulası, <$1000 ABD Asimetrik Liderleri ve Kaptan Onay Kartı
"""

import os
import sys
import hashlib
import json
import numpy as np
from datetime import datetime

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.common.t2saim_logger import get_logger, log_audit_event
from modules.markets.us.us_duckdb_manager import USDuckDBManager, USCandleRecord
from modules.markets.us.us_decomposer import USDecomposer, US_TARGET_SYMBOLS
from modules.markets.us.vix_volatility_shield import VIXVolatilityShield
from modules.markets.us.us_crisis_engine import USCrisisEngine

logger = get_logger("US_MASTER_RUNNER")

class USPodRunner:
    def __init__(self):
        self.duckdb_mgr = USDuckDBManager()
        self.decomposer = USDecomposer()
        self.vix_shield = VIXVolatilityShield()
        self.crisis_engine = USCrisisEngine()

    def seed_initial_demo_us_if_empty(self):
        """Veritabanı boşsa örnek ABD hisselerini yükler."""
        df = self.duckdb_mgr.get_causal_us_window("PLTR", datetime.now(), lookback_days=5)
        if df.empty:
            logger.info("us_market.duckdb boş, temel başlangıç verileri yükleniyor...")
            now = datetime.now()
            
            sample_data = [
                ("PLTR", 32.40, "DEFENSE_AI", 15.2),
                ("VST", 125.80, "NUCLEAR_POWER", 15.2),
                ("CEG", 260.50, "CLEAN_NUCLEAR", 15.2),
                ("NVDA", 128.50, "AI_HARDWARE", 15.2),
                ("LLY", 945.00, "BIOTECH_HEALTH", 15.2),
                ("CRWD", 285.00, "CYBER_DEFENSE", 15.2),
                ("TOO_EXPENSIVE_STOCK", 3450.0, "EXCLUDED", 15.2) # >= $1000 elenecek
            ]
            
            records = []
            for sym, price, sec, vix in sample_data:
                records.append(USCandleRecord(
                    timestamp=now,
                    symbol=sym,
                    open=price * 0.99,
                    high=price * 1.02,
                    low=price * 0.98,
                    close=price,
                    volume=25_000_000.0,
                    sector=sec,
                    vix_level=vix
                ))
            self.duckdb_mgr.insert_us_candles(records)

    def execute_daily_pipeline(self) -> dict:
        """
        ABD Podu Günlük Uçtan Uca Analiz Boru Hattı:
        1. SPY / QQQ / VIX Makro Yön Pusulası
        2. <$1000 Sektörel Asimetrik Alfa Hisseleri (Hurst H >= 0.60)
        3. VIX Volatilite ve Panik Sıçraması Kalkanı
        4. 1M ABD MCMC Simülasyonu ve Reel USD Kârı
        5. Kaptan ABD İcra Onay Kartı
        """
        logger.info("=== ABD PODU GÜNLÜK İCRA BORU HATTI BAŞLADI ===")
        self.seed_initial_demo_us_if_empty()

        # 1. SPY / QQQ / VIX Makro Pusulası
        spy_synth = np.array([550.0 + i*0.8 + np.random.normal(0, 0.5) for i in range(20)])
        qqq_synth = np.array([475.0 + i*1.0 + np.random.normal(0, 0.8) for i in range(20)])
        current_vix = 15.4
        prev_vix = 15.8

        compass_regime, compass_weight = self.decomposer.compass.compute_regime(spy_synth, qqq_synth, current_vix)

        # 2. VIX Kalkanı Denetimi
        vix_audit = self.vix_shield.audit_us_market(current_vix=current_vix, previous_vix=prev_vix)
        if not vix_audit.is_cleared:
            logger.error(f"🚨 ABD PİYASASI VIX TARAFINDAN VETOLANDI: {vix_audit.rejection_code}")
            return {"status": "VETOED_BY_VIX", "reason": vix_audit.rejection_code}

        # 3. Aday Hisseleri Değerlendir
        candidates_to_test = [
            ("PLTR", 32.40),
            ("VST", 125.80),
            ("CEG", 260.50),
            ("NVDA", 128.50),
            ("LLY", 945.00),
            ("CRWD", 285.00),
            ("TOO_EXPENSIVE_STOCK", 3450.0) # >= $1000 elenecek
        ]

        scored_candidates = []
        for sym, price in candidates_to_test:
            prices = np.array([price * (1.0 + i*0.007 + np.random.normal(0, 0.015)) for i in range(30)])
            score = self.decomposer.evaluate_us_stock(
                symbol=sym,
                price_usd=price,
                price_series=prices,
                compass_regime=compass_regime,
                compass_weight=compass_weight
            )
            scored_candidates.append(score)

        ranked_alphas = self.decomposer.rank_top_us_alphas(scored_candidates)
        if not ranked_alphas:
            logger.error("🚨 TÜM ABD HİSSELERİ ELENDİ!")
            return {"status": "NO_VALID_STOCKS"}

        selected_leader = ranked_alphas[0]

        # 4. 1M ABD MCMC Simülasyonu
        mcmc_res = self.crisis_engine.run_1m_us_mcmc(
            symbol=selected_leader.symbol,
            current_price_usd=selected_leader.price_usd,
            expected_drift=0.30,
            historical_volatility=0.35,
            horizon_days=30
        )

        # 5. Kaptan ABD İcra Onay Kartı
        card_payload = {
            "timestamp": datetime.now().isoformat(),
            "asset_class": "US_EQUITY_SUB1000",
            "symbol": selected_leader.symbol,
            "name": US_TARGET_SYMBOLS.get(selected_leader.symbol, {}).get("name", selected_leader.symbol),
            "price_usd": selected_leader.price_usd,
            "sector": selected_leader.sector,
            "thesis": US_TARGET_SYMBOLS.get(selected_leader.symbol, {}).get("thesis", "Asimetrik Sektörel Büyüme"),
            "hurst_exponent": selected_leader.hurst_exponent,
            "compass_regime": compass_regime,
            "vix_level": vix_audit.vix_level,
            "horizon_days": mcmc_res.horizon_days,
            "nominal_roi_pct": mcmc_res.nominal_mean_roi_pct,
            "real_net_usd_roi_pct": mcmc_res.real_net_usd_roi_pct,
            "worst_case_p05_pct": mcmc_res.worst_p05_pct,
            "status": "PENDING_CAPTAIN_APPROVAL"
        }

        card_json = json.dumps(card_payload, sort_keys=True)
        sha256_hash = hashlib.sha256(card_json.encode("utf-8")).hexdigest()
        card_payload["sha256_hash"] = sha256_hash

        self.render_captain_us_card(card_payload)
        log_audit_event("CAPTAIN_US_CARD_GENERATED", card_payload, raw_payload=card_json)

        return card_payload

    def render_captain_us_card(self, data: dict):
        """Kaptan ABD Onay Kartını terminale basar."""
        print("\n" + "=" * 80)
        print("🏛️ T2SAIM & HARI SELDON: KAPTAN İCRA ONAY KARTI (ABD PİYASALARI PODU)")
        print("=" * 80)
        print(f"🇺🇸 VARLIK / ŞİRKET : 🚀 {data['symbol']} (${data['price_usd']:.2f}) ──► {data['name']}")
        print(f"🔬 SEKTÖR / TEZ     : {data['sector']} | {data['thesis']}")
        print(f"📈 HURST ÜSSÜ (H)   : {data['hurst_exponent']} (H >= 0.60 Kurumsal Momentum)")
        print(f"🧭 MAKRO PUSULA     : {data['compass_regime']} (VIX: {data['vix_level']})")
        print(f"⏳ UFUK (HORIZON)   : D+{data['horizon_days']} Gün")
        print(f"📈 NOMİNAL GETİRİ   : +%{data['nominal_roi_pct']:.2f}")
        print(f"💰 REEL USD NET KÂR : +%{data['real_net_usd_roi_pct']:.2f} (Enflasyon & Komisyon Arındırılmış)")
        print(f"🛡️ VIX KALKANI      : %100 ONAYLI (Sistemik Likidasyon Şoku Yok)")
        print(f"🔒 SHA256 MÜHRÜ     : {data['sha256_hash'][:32]}...")
        print("-" * 80)
        print("                 [ 🟢 KAPTAN ONAYLA ]    [ 🔴 VETO ET / BEKLE ]")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    runner = USPodRunner()
    runner.execute_daily_pipeline()
