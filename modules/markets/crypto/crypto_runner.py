#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRYPTO MARKET MASTER RUNNER & ORCHESTRATOR (TICKET-CRYPTO-05)
Doktrin: Veritas Per Se · BTC/ETH Makro Pusula, <$2000 Asimetrik Alfa ve Kaptan Onay Kartı
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
from modules.markets.crypto.crypto_duckdb_manager import CryptoDuckDBManager, CryptoCandleRecord
from modules.markets.crypto.crypto_decomposer import CryptoDecomposer, TARGET_SUB2000_SYMBOLS
from modules.markets.crypto.tas_gnn_wash_shield import TASGNNWashShield
from modules.markets.crypto.crypto_crisis_engine import CryptoCrisisEngine

logger = get_logger("CRYPTO_MASTER_RUNNER")

class CryptoPodRunner:
    def __init__(self):
        self.duckdb_mgr = CryptoDuckDBManager()
        self.decomposer = CryptoDecomposer()
        self.wash_shield = TASGNNWashShield()
        self.crisis_engine = CryptoCrisisEngine()

    def seed_initial_demo_crypto_if_empty(self):
        """Veritabanı boşsa örnek kripto mumlarını yükler."""
        df = self.duckdb_mgr.get_causal_crypto_window("SOL", datetime.now(), lookback_days=5)
        if df.empty:
            logger.info("crypto_market.duckdb boş, temel başlangıç verileri yükleniyor...")
            now = datetime.now()
            
            sample_data = [
                ("SOL", 145.20, 0.00015, 0.12),
                ("AVAX", 24.80, 0.00010, 0.14),
                ("LINK", 11.50, 0.00012, 0.08),
                ("POL", 0.38, 0.00020, 0.18),
                ("XRP", 0.58, 0.00008, 0.15),
                ("BTC", 62500.0, 0.00010, 0.05),  # >=2000 olduğu için alım dışı
                ("FAKE_WASH_COIN", 2.40, 0.00050, 0.65) # Sahte hacim tuzağı
            ]
            
            records = []
            for sym, price, funding, wash in sample_data:
                records.append(CryptoCandleRecord(
                    timestamp=now,
                    symbol=sym,
                    open=price * 0.98,
                    high=price * 1.03,
                    low=price * 0.97,
                    close=price,
                    volume=50_000_000.0,
                    funding_rate=funding,
                    open_interest=100_000_000.0,
                    wash_trading_score=wash
                ))
            self.duckdb_mgr.insert_crypto_candles(records)

    def execute_daily_pipeline(self) -> dict:
        """
        Kripto Podu Günlük Uçtan Uca Analiz Boru Hattı:
        1. BTC/ETH Makro Rejim Tespiti (QuantEcon Markov Chain)
        2. <$2000 Asimetrik Altcoin Skorlaması
        3. TAS-GNN Wash-Trading Kalkanı
        4. 1M Kripto MCMC Simülasyonu ve Reel USD Kârı
        5. Kaptan İcra Onay Kartı
        """
        logger.info("=== KRİPTO PODU GÜNLÜK İCRA BORU HATTI BAŞLADI ===")
        self.seed_initial_demo_crypto_if_empty()

        # 1. BTC / ETH Makro Pusula Rejimi
        btc_synth = np.array([60000.0 + i*150.0 + np.random.normal(0, 200) for i in range(20)])
        eth_synth = np.array([2600.0 + i*10.0 + np.random.normal(0, 15) for i in range(20)])
        regime, macro_weight = self.decomposer.regime_detector.detect_regime(btc_synth, eth_synth)

        # 2. Aday Varlıkları Değerlendir
        candidates_to_test = [
            ("SOL", 145.20, 0.00015, 0.12),
            ("AVAX", 24.80, 0.00010, 0.14),
            ("LINK", 11.50, 0.00012, 0.08),
            ("POL", 0.38, 0.00020, 0.18),
            ("BTC", 62500.0, 0.00010, 0.05), # Disqualified (>=2000)
            ("FAKE_WASH_COIN", 2.40, 0.00050, 0.65) # Disqualified (Wash trading)
        ]

        scored_candidates = []
        for sym, price, funding, wash in candidates_to_test:
            prices = np.array([price * (1.0 + i*0.01 + np.random.normal(0, 0.02)) for i in range(30)])
            score = self.decomposer.evaluate_altcoin(
                symbol=sym,
                price_usd=price,
                price_series=prices,
                funding_rate_8h=funding,
                wash_trading_score=wash,
                macro_regime=regime,
                macro_weight=macro_weight
            )
            scored_candidates.append(score)

        top_cryptos = self.decomposer.select_top_asymmetric_cryptos(scored_candidates)

        # 3. TAS-GNN Wash Trading Kalkanı
        cleared_cryptos = []
        for c in top_cryptos:
            audit = self.wash_shield.audit_crypto_asset(
                symbol=c.symbol,
                wash_trading_score=c.wash_trading_score
            )
            if audit.is_cleared:
                cleared_cryptos.append(c)
            else:
                logger.warning(f"Kripto elendi: {c.symbol} ({audit.rejection_code})")

        if not cleared_cryptos:
            logger.error("🚨 TÜM KRİPTO VARLIKLAR VETOLANDI!")
            return {"status": "VETOED_ALL"}

        selected_leader = cleared_cryptos[0]

        # 4. 1M MCMC Simülasyonu
        mcmc_res = self.crisis_engine.run_1m_crypto_mcmc(
            symbol=selected_leader.symbol,
            current_price_usd=selected_leader.price_usd,
            expected_drift=0.35,
            historical_volatility=0.45,
            funding_rate_8h=0.00015,
            macro_regime=regime,
            horizon_days=14
        )

        # 5. Kaptan Kripto İcra Onay Kartı
        card_payload = {
            "timestamp": datetime.now().isoformat(),
            "asset_class": "CRYPTO_SUB2000",
            "symbol": selected_leader.symbol,
            "price_usd": selected_leader.price_usd,
            "macro_regime": regime,
            "horizon_days": mcmc_res.horizon_days,
            "nominal_roi_pct": mcmc_res.nominal_mean_roi_pct,
            "funding_basis_annual_pct": mcmc_res.funding_basis_annual_pct,
            "real_net_usd_roi_pct": mcmc_res.real_net_usd_roi_pct,
            "worst_case_p05_pct": mcmc_res.worst_p05_pct,
            "status": "PENDING_CAPTAIN_APPROVAL"
        }

        card_json = json.dumps(card_payload, sort_keys=True)
        sha256_hash = hashlib.sha256(card_json.encode("utf-8")).hexdigest()
        card_payload["sha256_hash"] = sha256_hash

        self.render_captain_crypto_card(card_payload)
        log_audit_event("CAPTAIN_CRYPTO_CARD_GENERATED", card_payload, raw_payload=card_json)

        return card_payload

    def render_captain_crypto_card(self, data: dict):
        """Kaptan Kripto Onay Kartını terminale basar."""
        print("\n" + "=" * 80)
        print("🏛️ T2SAIM & HARI SELDON: KAPTAN İCRA ONAY KARTI (KRİPTO PODU)")
        print("=" * 80)
        print(f"🪙 VARLIK / TÜR     : 🚀 {data['symbol']} (${data['price_usd']:.2f}) ──► <$2000 ASİMETRİK ALFA")
        print(f"🧭 MAKRO PUSULA     : BTC/ETH Markov Rejimi ──► {data['macro_regime']}")
        print(f"⏳ UFUK (HORIZON)   : D+{data['horizon_days']} Gün")
        print(f"📈 NOMİNAL GETİRİ   : +%{data['nominal_roi_pct']:.2f}")
        print(f"💵 FONLAMA YILLIK   : +%{data['funding_basis_annual_pct']:.2f} (Delta-Neutral Arbitraj)")
        print(f"💰 REEL USD NET KÂR : +%{data['real_net_usd_roi_pct']:.2f} (Enflasyon & Komisyon Arındırılmış)")
        print(f"🛡️ TAŞ-GNN DENETİMİ : %100 ONAYLI (Yapay Hacim & Döngüsel Transfer Yok)")
        print(f"🔒 SHA256 MÜHRÜ     : {data['sha256_hash'][:32]}...")
        print("-" * 80)
        print("                 [ 🟢 KAPTAN ONAYLA ]    [ 🔴 VETO ET / BEKLE ]")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    runner = CryptoPodRunner()
    runner.execute_daily_pipeline()
