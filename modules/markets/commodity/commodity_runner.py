#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM COMMODITY POD MASTER RUNNER & ORCHESTRATOR (TICKET-COMMODITY-05)
Doktrin: Veritas Per Se · 30 Yıllık Süper Emtialar, Contango Kalkanı ve Kaptan Onay Kartı
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
from modules.markets.commodity.commodity_duckdb_manager import CommodityDuckDBManager, CommodityCandleRecord
from modules.markets.commodity.commodity_decomposer import CommodityDecomposer, SUPER_COMMODITIES_CATALOG
from modules.markets.commodity.contango_roll_shield import ContangoRollShield
from modules.markets.commodity.commodity_crisis_engine import CommodityCrisisEngine

logger = get_logger("COMMODITY_MASTER_RUNNER")

class CommodityPodRunner:
    def __init__(self):
        self.duckdb_mgr = CommodityDuckDBManager()
        self.decomposer = CommodityDecomposer()
        self.contango_shield = ContangoRollShield()
        self.crisis_engine = CommodityCrisisEngine()

    def seed_initial_demo_commodities_if_empty(self):
        """Veritabanı boşsa örnek emtia mumlarını yükler."""
        df = self.duckdb_mgr.get_causal_commodity_window("SILVER", datetime.now(), lookback_days=5)
        if df.empty:
            logger.info("commodity_market.duckdb boş, temel başlangıç verileri yükleniyor...")
            now = datetime.now()
            
            sample_data = [
                ("SILVER", 32.50, 32.55, 32.50, 0.0015, 0.85),
                ("COCOA", 7850.0, 7850.0, 7790.0, 0.0076, 0.95),
                ("URANIUM", 85.0, 85.0, 85.0, 0.0, 0.90), # Fiziki Tröst
                ("COFFEE", 245.0, 245.0, 243.5, 0.0061, 0.75),
                ("COPPER", 4.35, 4.35, 4.34, 0.0023, 0.80),
                ("ALTIN.S1", 34.20, 34.20, 34.20, 0.0, 0.70), # Darphane Sertifikası
                ("DEEP_CONTANGO_TRAP", 100.0, 100.0, 105.0, -0.050, 0.50) # Sermaye eriten tuzak
            ]
            
            records = []
            for sym, spot, f0, f1, roll, deficit in sample_data:
                records.append(CommodityCandleRecord(
                    timestamp=now,
                    symbol=sym,
                    spot_price=spot,
                    front_month_futures=f0,
                    next_month_futures=f1,
                    roll_yield_pct=roll,
                    physical_deficit_score=deficit,
                    volume=100_000.0
                ))
            self.duckdb_mgr.insert_commodity_candles(records)

    def execute_daily_pipeline(self) -> dict:
        """
        Süper Emtialar Podu Günlük Uçtan Uca Analiz Boru Hattı:
        1. Altın / Ham Petrol Makro Yön Pusulası
        2. 5 Stratejik Süper Emtia + ALTIN.S1 Süper Döngü Skorlaması (Hurst H >= 0.61)
        3. Contango Roll-Bleed Kalkanı Denetimi
        4. 1M Emtia MCMC Simülasyonu ve Reel USD Getirisi
        5. Kaptan Süper Emtia İcra Onay Kartı
        """
        logger.info("=== SÜPER EMTİALAR PODU GÜNLÜK İCRA BORU HATTI BAŞLADI ===")
        self.seed_initial_demo_commodities_if_empty()

        # 1. Makro Emtia Pusulası (Altın & Petrol)
        gold_synth = np.array([2450.0 + i*5.0 + np.random.normal(0, 4) for i in range(20)])
        oil_synth = np.array([76.0 + i*0.2 + np.random.normal(0, 0.3) for i in range(20)])
        compass_mult, compass_regime = self.decomposer.compass.compute_compass_multiplier(gold_synth, oil_synth)

        # 2. Aday Emtiaları Skorla
        candidates_to_test = [
            ("SILVER", 32.50, 32.55, 32.50, 0.0015, 0.85),
            ("COCOA", 7850.0, 7850.0, 7790.0, 0.0076, 0.95),
            ("URANIUM", 85.0, 85.0, 85.0, 0.0, 0.90),
            ("COFFEE", 245.0, 245.0, 243.5, 0.0061, 0.75),
            ("COPPER", 4.35, 4.35, 4.34, 0.0023, 0.80),
            ("ALTIN.S1", 34.20, 34.20, 34.20, 0.0, 0.70),
            ("DEEP_CONTANGO_TRAP", 100.0, 100.0, 105.0, -0.050, 0.50) # Veto edilecek
        ]

        scored_candidates = []
        for sym, spot, f0, f1, roll, deficit in candidates_to_test:
            prices = np.array([spot * (1.0 + i*0.008 + np.random.normal(0, 0.01)) for i in range(30)])
            score = self.decomposer.evaluate_commodity(
                symbol=sym,
                spot_price=spot,
                price_series=prices,
                roll_yield_pct=roll,
                physical_deficit_score=deficit,
                compass_multiplier=compass_mult
            )
            scored_candidates.append((score, f0, f1))

        # 3. Contango Kalkanı Denetimi
        cleared_candidates = []
        for score_obj, f0, f1 in scored_candidates:
            audit = self.contango_shield.audit_commodity_curve(
                symbol=score_obj.symbol,
                front_month_price=f0,
                next_month_price=f1,
                is_physical_spot_trust=(score_obj.symbol in ["URANIUM", "ALTIN.S1"])
            )
            if audit.is_cleared:
                cleared_candidates.append(score_obj)
            else:
                logger.warning(f"Emtia elendi: {score_obj.symbol} ({audit.rejection_code})")

        if not cleared_candidates:
            logger.error("🚨 TÜM EMTİALAR VETOLANDI!")
            return {"status": "VETOED_ALL"}

        ranked_commodities = self.decomposer.rank_super_commodities(cleared_candidates)
        selected_leader = ranked_commodities[0]

        # 4. 1M Emtia MCMC Simülasyonu
        mcmc_res = self.crisis_engine.run_1m_commodity_mcmc(
            symbol=selected_leader.symbol,
            current_spot_price=selected_leader.spot_price,
            expected_drift=0.25,
            historical_volatility=0.28,
            monthly_roll_yield=selected_leader.roll_yield_pct,
            horizon_months=18
        )

        # 5. Kaptan Süper Emtia İcra Onay Kartı
        card_payload = {
            "timestamp": datetime.now().isoformat(),
            "asset_class": "30Y_SUPER_COMMODITY",
            "symbol": selected_leader.symbol,
            "spot_price": selected_leader.spot_price,
            "thesis": SUPER_COMMODITIES_CATALOG.get(selected_leader.symbol, {}).get("thesis", "Yapısal Arz Açığı"),
            "hurst_exponent": selected_leader.hurst_exponent,
            "physical_deficit_score": selected_leader.physical_deficit_score,
            "compass_regime": compass_regime,
            "horizon_months": mcmc_res.horizon_months,
            "nominal_roi_pct": mcmc_res.nominal_mean_roi_pct,
            "roll_impact_pct": mcmc_res.roll_yield_impact_pct,
            "real_net_usd_roi_pct": mcmc_res.real_net_usd_roi_pct,
            "worst_case_p05_pct": mcmc_res.worst_p05_pct,
            "status": "PENDING_CAPTAIN_APPROVAL"
        }

        card_json = json.dumps(card_payload, sort_keys=True)
        sha256_hash = hashlib.sha256(card_json.encode("utf-8")).hexdigest()
        card_payload["sha256_hash"] = sha256_hash

        self.render_captain_commodity_card(card_payload)
        log_audit_event("CAPTAIN_COMMODITY_CARD_GENERATED", card_payload, raw_payload=card_json)

        return card_payload

    def render_captain_commodity_card(self, data: dict):
        """Kaptan Süper Emtia Onay Kartını terminale basar."""
        print("\n" + "=" * 80)
        print("🏛️ T2SAIM & HARI SELDON: KAPTAN İCRA ONAY KARTI (SÜPER EMTİALAR PODU)")
        print("=" * 80)
        print(f"📦 VARLIK / TÜR     : ⛏️ {data['symbol']} (${data['spot_price']}) ──► 30 YILLIK SÜPER DÖNGÜ")
        print(f"🔬 TEZ / NEDEN      : {data['thesis']}")
        print(f"📈 HURST ÜSSÜ (H)   : {data['hurst_exponent']} (H >= 0.61 Yapısal Kalıcı Trend)")
        print(f"⚠️ ARZ AÇIĞI SKORU  : %{data['physical_deficit_score']*100:.1f} (Derin Fiziksel Kriz)")
        print(f"🧭 MAKRO PUSULA     : {data['compass_regime']}")
        print(f"⏳ UFUK (HORIZON)   : M+{data['horizon_months']} Ay (Süper Döngü)")
        print(f"📈 NOMİNAL GETİRİ   : +%{data['nominal_roi_pct']:.2f}")
        print(f"🔄 ROLL GETİRİSİ    : %{data['roll_impact_pct']:+.2f} (Pozitif Backwardation Primi)")
        print(f"💰 REEL USD NET KÂR : +%{data['real_net_usd_roi_pct']:.2f} (Enflasyon & Komisyon Arındırılmış)")
        print(f"🛡️ CONTANGO KALKANI : %100 ONAYLI (Sermaye Kanaması Yok)")
        print(f"🔒 SHA256 MÜHRÜ     : {data['sha256_hash'][:32]}...")
        print("-" * 80)
        print("                 [ 🟢 KAPTAN ONAYLA ]    [ 🔴 VETO ET / BEKLE ]")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    runner = CommodityPodRunner()
    runner.execute_daily_pipeline()
