#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRYPTO ASYMMETRIC DECOMPOSITION & QUANTECON MARKOV REGIME (TICKET-CRYPTO-02)
Doktrin: Veritas Per Se · BTC/ETH Makro Pusula & <$2000 Asimetrik Altcoin Seçimi
"""

import numpy as np
import quantecon as qe
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event
from modules.markets.tr.bist_decomposer import compute_hurst_fast

logger = get_logger("CRYPTO_DECOMPOSER")

# Varlık Evreni
MACRO_COMPASS_SYMBOLS = ["BTC", "ETH"]  # Sadece yön takibi
TARGET_SUB2000_SYMBOLS = ["SOL", "AVAX", "LINK", "POL", "XRP", "NEAR", "SUI", "APT", "RENDER", "FET"]

class CryptoCandidateScore(BaseModel):
    symbol: str
    price_usd: float
    is_sub_2000: bool
    hurst_exponent: float
    funding_rate_annual_pct: float
    wash_trading_score: float
    macro_regime: str
    composite_score: float
    expected_roi_pct: float
    rank: int

# =====================================================================
# QUANTECON TABANLI MAKRO KRİPTO MARKOV REJİM MOTORU
# =====================================================================

class CryptoMacroRegimeDetector:
    def __init__(self):
        # 3 Durumlu Kripto Rejim Geçiş Matrisi: [BULL, CHOPPY, BEAR_LIQUIDATION]
        self.P = np.array([
            [0.80, 0.15, 0.05],  # BULL
            [0.20, 0.65, 0.15],  # CHOPPY
            [0.08, 0.22, 0.70]   # BEAR_LIQUIDATION
        ])
        self.states = ["BULL_EXPANSION", "CHOPPY_ACCUMULATION", "BEAR_LIQUIDATION"]
        self.mc = qe.MarkovChain(self.P, state_values=self.states)
        self.stationary_probs = self.mc.stationary_distributions[0]

    def detect_regime(self, btc_price_series: np.ndarray, eth_price_series: np.ndarray) -> Tuple[str, float]:
        """BTC ve ETH momentumundan piyasanın anlık rejimini ve makro çarpanını döner."""
        if len(btc_price_series) < 10:
            return "CHOPPY_ACCUMULATION", 1.00

        btc_ret = (btc_price_series[-1] - btc_price_series[0]) / btc_price_series[0]
        eth_ret = (eth_price_series[-1] - eth_price_series[0]) / eth_price_series[0]
        avg_macro_ret = (btc_ret + eth_ret) / 2.0

        if avg_macro_ret > 0.08:
            regime = "BULL_EXPANSION"
            weight = 1.35
        elif avg_macro_ret < -0.06:
            regime = "BEAR_LIQUIDATION"
            weight = 0.60
        else:
            regime = "CHOPPY_ACCUMULATION"
            weight = 1.00

        logger.info(f"Kripto Makro Rejimi: {regime} (Ağırlık: {weight}, BTC/ETH Getiri: {avg_macro_ret*100:.2f}%)")
        return regime, weight

# =====================================================================
# <$2000 ASİMETRİK ALFA SEÇİCİ
# =====================================================================

class CryptoDecomposer:
    def __init__(self):
        self.regime_detector = CryptoMacroRegimeDetector()

    def evaluate_altcoin(
        self,
        symbol: str,
        price_usd: float,
        price_series: np.ndarray,
        funding_rate_8h: float = 0.0001,
        wash_trading_score: float = 0.15,
        macro_regime: str = "CHOPPY_ACCUMULATION",
        macro_weight: float = 1.00,
        epsilon: float = 1e-4
    ) -> CryptoCandidateScore:
        """
        <$2000 Asimetrik Altcoin Skorlama Formülü:
        Score = ((Momentum * (1 + FundingArbitrage)) / (DownsideVol + eps)) * (1 - WashRisk) * W_macro * (h / 0.50)
        """
        is_sub_2000 = price_usd < 2000.0
        
        # Eğer fiyat >= 2000 ise alım listesinden elenir (Skor 0)
        if not is_sub_2000:
            return CryptoCandidateScore(
                symbol=symbol,
                price_usd=price_usd,
                is_sub_2000=False,
                hurst_exponent=0.50,
                funding_rate_annual_pct=0.0,
                wash_trading_score=wash_trading_score,
                macro_regime=macro_regime,
                composite_score=0.0,
                expected_roi_pct=0.0,
                rank=999
            )

        h = compute_hurst_fast(price_series)
        funding_annual_pct = funding_rate_8h * 3 * 365 * 100.0  # Yıllık fonlama arbitraj getirisi (%)
        
        # Aşağı yönlü volatilite
        returns = np.diff(price_series) / price_series[:-1]
        downside_returns = returns[returns < 0]
        downside_vol = float(np.std(downside_returns)) if len(downside_returns) > 2 else float(np.std(returns))
        downside_vol = max(0.02, downside_vol)

        momentum = (price_series[-1] - price_series[0]) / price_series[0]
        momentum_factor = max(0.05, 1.0 + momentum)
        
        # Arbitraj ve Sahtekarlık İndirimi
        arbitrage_factor = 1.0 + max(-0.5, min(0.5, (funding_annual_pct / 100.0)))
        wash_discount = max(0.01, (1.0 - wash_trading_score))
        fractal_factor = max(0.2, (h / 0.50))

        # Bileşik Asimetrik Skor
        composite_score = (momentum_factor * arbitrage_factor / (downside_vol + epsilon)) * wash_discount * macro_weight * fractal_factor
        expected_roi = composite_score * 8.5  # Normalize edilmiş beklenen ROI (%)

        return CryptoCandidateScore(
            symbol=symbol,
            price_usd=round(price_usd, 4),
            is_sub_2000=True,
            hurst_exponent=round(h, 4),
            funding_rate_annual_pct=round(funding_annual_pct, 2),
            wash_trading_score=round(wash_trading_score, 4),
            macro_regime=macro_regime,
            composite_score=round(composite_score, 4),
            expected_roi_pct=round(expected_roi, 2),
            rank=0
        )

    def select_top_asymmetric_cryptos(self, candidates: List[CryptoCandidateScore]) -> List[CryptoCandidateScore]:
        """Yalnızca <$2000 varlıkları skora göre sıralar ve Top listeyi üretir."""
        valid_candidates = [c for c in candidates if c.is_sub_2000]
        sorted_cryptos = sorted(valid_candidates, key=lambda x: x.composite_score, reverse=True)
        
        for idx, c in enumerate(sorted_cryptos, start=1):
            c.rank = idx
            
        logger.info(f"Top Asimetrik Kripto Seçimi Tamamlandı. Lider: {sorted_cryptos[0].symbol} (Skor: {sorted_cryptos[0].composite_score})")
        log_audit_event("TOP_ASYMMETRIC_CRYPTO_SELECTED", {
            "top_1": sorted_cryptos[0].symbol if sorted_cryptos else "NONE",
            "symbols": [c.symbol for c in sorted_cryptos[:5]]
        })
        return sorted_cryptos
