#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM US MARKET DECOMPOSER & ASYMMETRIC ALPHA ENGINE (TICKET-US-02)
Doktrin: Veritas Per Se · SPY/QQQ/VIX Makro Pusulası ve <$1000 ABD Asimetrik Liderleri
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.common.t2saim_logger import get_logger

logger = get_logger("US_DECOMPOSER")

# Hedef ABD Asimetrik Alfa Evreni (<$1000)
US_TARGET_SYMBOLS = {
    "PLTR": {"sector": "DEFENSE_AI", "name": "Palantir Technologies", "thesis": "AI Savunma & İstihbarat Platformu"},
    "VST": {"sector": "NUCLEAR_POWER", "name": "Vistra Corp", "thesis": "AI Veri Merkezleri için Nükleer & Bağımsız Güç"},
    "CEG": {"sector": "CLEAN_NUCLEAR", "name": "Constellation Energy", "thesis": "ABD'nin En Büyük Nükleer Enerji Üreticisi"},
    "NVDA": {"sector": "AI_HARDWARE", "name": "Nvidia Corporation", "thesis": "Yapay Zeka Hızlandırılmış Hesaplama"},
    "LLY": {"sector": "BIOTECH_HEALTH", "name": "Eli Lilly and Company", "thesis": "Metabolik & Biyofarmasötik İnovasyon"},
    "CRWD": {"sector": "CYBER_DEFENSE", "name": "CrowdStrike Holdings", "thesis": "Uç Nokta & Bulut Siber Güvenlik Kalkanı"}
}

COMPASS_SYMBOLS = ["SPY", "QQQ", "VIX"]

class USAlphaScore(BaseModel):
    symbol: str
    price_usd: float
    sector: str
    hurst_exponent: float = Field(..., ge=0.0, le=1.0)
    momentum_20d_pct: float
    compass_alignment: str
    composite_score: float
    is_sub_1000: bool

class USMacroCompass:
    """
    SPY, QQQ ve VIX endekslerini yalnızca yönsel piyasa pusulası olarak izler.
    """
    def compute_regime(
        self,
        spy_prices: np.ndarray,
        qqq_prices: np.ndarray,
        vix_level: float
    ) -> Tuple[str, float]:
        if len(spy_prices) < 5 or len(qqq_prices) < 5:
            return "NEUTRAL_CHOPPY", 1.0

        spy_ret = (spy_prices[-1] - spy_prices[0]) / spy_prices[0]
        qqq_ret = (qqq_prices[-1] - qqq_prices[0]) / qqq_prices[0]

        if vix_level > 28.5:
            return "HIGH_VOLATILITY_RISK_OFF", 0.50
        elif vix_level < 16.0 and spy_ret > 0.01 and qqq_ret > 0.01:
            return "RISK_ON_AI_EXPANSION", 1.30
        elif spy_ret > 0.0 and qqq_ret <= 0.0:
            return "ROTATION_TO_DEFENSIVE", 1.10
        elif spy_ret < -0.02 or qqq_ret < -0.02:
            return "CORRECTION_PRESSURE", 0.80
        else:
            return "BALANCED_BULLISH", 1.0

class USDecomposer:
    def __init__(self):
        self.compass = USMacroCompass()

    def compute_fast_hurst(self, time_series: np.ndarray) -> float:
        """
        ABD Hisseleri için Hızlı Hurst (H) Hesabı:
        H >= 0.60 -> Kalıcı Momentum / Kurumsal Birikim
        """
        N = len(time_series)
        if N < 16:
            return 0.50
        
        returns = np.diff(time_series)
        if len(returns) == 0 or np.std(returns) == 0:
            return 0.50
            
        mean_r = np.mean(returns)
        deviations = returns - mean_r
        cum_deviations = np.cumsum(deviations)
        r_range = np.max(cum_deviations) - np.min(cum_deviations)
        s_std = np.std(returns)
        
        if s_std == 0 or r_range == 0:
            return 0.50
            
        rs = r_range / s_std
        hurst = np.log(rs) / np.log(N)
        return float(np.clip(hurst, 0.05, 0.95))

    def evaluate_us_stock(
        self,
        symbol: str,
        price_usd: float,
        price_series: np.ndarray,
        compass_regime: str = "BALANCED_BULLISH",
        compass_weight: float = 1.0
    ) -> USAlphaScore:
        is_sub_1000 = price_usd < 1000.0
        
        if not is_sub_1000:
            return USAlphaScore(
                symbol=symbol,
                price_usd=price_usd,
                sector="EXCLUDED_EXPENSIVE",
                hurst_exponent=0.50,
                momentum_20d_pct=0.0,
                compass_alignment=compass_regime,
                composite_score=0.0,
                is_sub_1000=False
            )

        hurst = self.compute_fast_hurst(price_series)
        mom_20d = ((price_series[-1] - price_series[0]) / price_series[0]) * 100.0 if len(price_series) > 1 else 0.0
        
        sector_info = US_TARGET_SYMBOLS.get(symbol, {"sector": "GENERAL"})["sector"]
        
        # Skorlama:
        # 1. Hurst Trend Gücü (%40)
        # 2. 20 Günlük Momentum (%30)
        # 3. Makro Pusula Ağırlığı (%30)
        mom_norm = max(0.0, min(1.0, 0.5 + (mom_20d / 50.0)))
        
        comp_score = (
            (0.40 * (hurst / 0.95)) +
            (0.30 * mom_norm) +
            (0.30 * (compass_weight / 1.30))
        ) * 100.0

        return USAlphaScore(
            symbol=symbol,
            price_usd=price_usd,
            sector=sector_info,
            hurst_exponent=round(hurst, 4),
            momentum_20d_pct=round(mom_20d, 2),
            compass_alignment=compass_regime,
            composite_score=round(comp_score, 4),
            is_sub_1000=True
        )

    def rank_top_us_alphas(self, scores: List[USAlphaScore]) -> List[USAlphaScore]:
        valid = [s for s in scores if s.is_sub_1000 and s.composite_score > 0.0]
        ranked = sorted(valid, key=lambda x: x.composite_score, reverse=True)
        if ranked:
            logger.info(f"Top ABD Alfa Seçimi Tamamlandı. Lider: {ranked[0].symbol} (Skor: {ranked[0].composite_score})")
        return ranked

if __name__ == "__main__":
    dec = USDecomposer()
    print("US Decomposer hazır.")
