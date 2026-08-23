#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM COMMODITY DECOMPOSER & SUPER-CYCLE DETECTOR (TICKET-COMMODITY-02)
Doktrin: Veritas Per Se · 5 Stratejik Süper Emtia, Altın/Petrol Pusulası ve 18-36 Aylık Arz Açığı
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

logger = get_logger("COMMODITY_DECOMPOSER")

# 5 Stratejik Süper Emtia ve Temel Spesifikasyonları
SUPER_COMMODITIES_CATALOG = {
    "SILVER": {"weight_target": 0.25, "sector": "INDUSTRIAL_PRECIOUS", "thesis": "Güneş PV & AI Çip İletkenliği"},
    "COCOA": {"weight_target": 0.25, "sector": "AGRICULTURAL_SHOCK", "thesis": "Batı Afrika 60 Yılın En Derin Arz Açığı"},
    "URANIUM": {"weight_target": 0.20, "sector": "NUCLEAR_ENERGY", "thesis": "Nükleer Rönesans & Yapay Zeka Enerji Şebekesi"},
    "COFFEE": {"weight_target": 0.15, "sector": "CLIMATE_DISRUPTION", "thesis": "Vietnam & Brezilya Don/Kuraklık Şoku"},
    "COPPER": {"weight_target": 0.15, "sector": "ELECTRIFICATION", "thesis": "Veri Merkezleri & Küresel Şebeke Dönüşümü"},
    "ALTIN.S1": {"weight_target": 0.20, "sector": "TR_LOCAL_GOLD", "thesis": "Darphane Sertifikası - GVK 67 %0 Stopaj"}
}

COMPASS_ASSETS = ["GOLD_COMPASS", "OIL_COMPASS"]

class CommoditySuperCycleScore(BaseModel):
    symbol: str
    spot_price: float
    hurst_exponent: float = Field(..., ge=0.0, le=1.0)
    physical_deficit_score: float = Field(..., ge=0.0, le=1.0)
    roll_yield_pct: float
    compass_alignment_pct: float
    composite_score: float
    is_super_cycle_active: bool

class CommodityMacroCompass:
    """
    Külçe Altın ve Ham Petrolü yalnızca yönsel makro pusula (Macro Directional Compass) olarak izler.
    Hantal sermaye bağlamaz; küresel likidite ve jeopolitik gerilim katsayısını hesaplar.
    """
    def compute_compass_multiplier(
        self,
        gold_price_series: np.ndarray,
        oil_price_series: np.ndarray
    ) -> Tuple[float, str]:
        if len(gold_price_series) < 5 or len(oil_price_series) < 5:
            return 1.0, "NEUTRAL_EXPANSION"
            
        gold_ret = (gold_price_series[-1] - gold_price_series[0]) / gold_price_series[0]
        oil_ret = (oil_price_series[-1] - oil_price_series[0]) / oil_price_series[0]
        
        # Küresel Emtia Rallisi Rejimi
        if gold_ret > 0.02 and oil_ret > 0.02:
            return 1.25, "GLOBAL_INFLATION_SURGE"
        elif gold_ret > 0.02 and oil_ret <= 0.0:
            return 1.15, "GEOPOLITICAL_FLIGHT_TO_SAFETY"
        elif gold_ret <= -0.03 and oil_ret <= -0.03:
            return 0.75, "DEFLATIONARY_CONTRACTION"
        else:
            return 1.0, "BALANCED_COMMODITY_FLOW"

class CommodityDecomposer:
    def __init__(self):
        self.compass = CommodityMacroCompass()

    def compute_fast_hurst(self, time_series: np.ndarray) -> float:
        """
        18-36 Aylık Emtia Süper Döngüsü için R/S Hurst Üssü (H):
        H >= 0.61 -> Kalıcı / Yapısal Arz Açığı Trendi
        H ~ 0.50  -> Rastgele Yürüyüş
        H < 0.40  -> Ortalama Düzeltmeli / Sıkışmış Piyasa
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

    def evaluate_commodity(
        self,
        symbol: str,
        spot_price: float,
        price_series: np.ndarray,
        roll_yield_pct: float,
        physical_deficit_score: float,
        compass_multiplier: float = 1.0
    ) -> CommoditySuperCycleScore:
        """
        Emtia Varlığını 18-36 Aylık Süper Döngü Perspektifiyle Puanlar.
        """
        hurst = self.compute_fast_hurst(price_series)
        is_active = (hurst >= 0.58) and (physical_deficit_score >= 0.40)
        
        # Skor Bileşenleri:
        # 1. Hurst Trend Gücü (%35)
        # 2. Fiziksel Arz Açığı (%35)
        # 3. Roll Yield / Backwardation Primi (%15)
        # 4. Makro Pusula Çarpanı (%15)
        
        roll_score = max(0.0, min(1.0, 0.5 + roll_yield_pct * 5.0))
        comp_score = (
            (0.35 * (hurst / 0.95)) +
            (0.35 * physical_deficit_score) +
            (0.15 * roll_score) +
            (0.15 * (compass_multiplier / 1.25))
        ) * 100.0
        
        return CommoditySuperCycleScore(
            symbol=symbol,
            spot_price=spot_price,
            hurst_exponent=round(hurst, 4),
            physical_deficit_score=round(physical_deficit_score, 4),
            roll_yield_pct=round(roll_yield_pct, 4),
            compass_alignment_pct=round(compass_multiplier * 100.0, 2),
            composite_score=round(comp_score, 4),
            is_super_cycle_active=is_active
        )

    def rank_super_commodities(
        self,
        scores: List[CommoditySuperCycleScore]
    ) -> List[CommoditySuperCycleScore]:
        """Skora göre süper emtiaları sıralar."""
        ranked = sorted(scores, key=lambda x: x.composite_score, reverse=True)
        if ranked:
            logger.info(f"Süper Emtia Sıralaması Tamamlandı. Lider: {ranked[0].symbol} (Skor: {ranked[0].composite_score})")
        return ranked

if __name__ == "__main__":
    decomposer = CommodityDecomposer()
    print("Commodity Decomposer başarıyla hazırlandı.")
