#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM BIST-100 SECTOR DECOMPOSITION & TOP 10 ALPHA ENGINE (TICKET-TR-02)
Doktrin: Veritas Per Se · Fraktal Eğilim ve Asimetrik Döviz Alfa Seçimi
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("BIST_DECOMPOSER")

# =====================================================================
# 3 STRATEJİK SEKTÖR KÜMESİ VE AĞIRLIKLARI
# =====================================================================

SECTOR_CLUSTERS = {
    "EXPORTERS_FX": {
        "weight": 1.25,
        "symbols": ["ASELS", "THYAO", "TUPRS", "FROTO", "EREGL", "SISE", "ARCLK", "TAVHL", "CCOLA", "PGSUS"]
    },
    "HIGH_BETA_TECH": {
        "weight": 1.15,
        "symbols": ["KCHOL", "SAHOL", "LOGO", "KFEIN", "MIATK", "REEDR", "ASTOR", "KONTR", "EUPWR", "ALARK"]
    },
    "DEFENSIVE_CASHFLOW": {
        "weight": 1.10,
        "symbols": ["BIMAS", "MGROS", "SOKM", "ENKAI", "TCELL", "TTKOM", "ULKER", "AEFES", "AKSA"]
    }
}

class AlphaStockScore(BaseModel):
    symbol: str
    sector: str
    score: float
    hurst_exponent: float
    c_takas: float
    r_cancel: float
    expected_alpha: float
    rank: int

# =====================================================================
# HIZLI FRAKTAL HURST ÜSSÜ HESAPLAYICI (<0.2 ms)
# =====================================================================

def compute_hurst_fast(series: np.ndarray, max_lag: int = 20) -> float:
    """
    Vektörize hızlı Hurst üssü hesaplayıcısı (R/S Analizi).
    h > 0.50 -> Kalıcı trend (Persistent)
    h < 0.50 -> Ortalama dönen (Mean-reverting)
    h = 0.50 -> Rastgele yürüyüş (Random Walk)
    """
    if len(series) < max_lag * 2:
        return 0.50

    try:
        series = np.asarray(series, dtype=float)
        # Farklar üzerinden R/S aralıkları
        lags = range(4, min(max_lag, len(series) // 2))
        rs_values = []
        valid_lags = []
        
        for lag in lags:
            # Alt serilere böl
            n_chunks = len(series) // lag
            chunk_rs = []
            for i in range(n_chunks):
                chunk = series[i * lag : (i + 1) * lag]
                mean_adj = chunk - np.mean(chunk)
                cum_dev = np.cumsum(mean_adj)
                r = np.max(cum_dev) - np.min(cum_dev)
                s = np.std(chunk)
                if s > 1e-8:
                    chunk_rs.append(r / s)
            if chunk_rs:
                rs_values.append(np.mean(chunk_rs))
                valid_lags.append(lag)

        if len(valid_lags) < 3:
            return 0.50

        x = np.log(valid_lags)
        y = np.log(rs_values)
        poly = np.polyfit(x, y, 1)
        h = float(poly[0])
        return max(0.05, min(0.95, h))
    except Exception as e:
        logger.warning(f"Hurst hesaplama hatası: {e}")
        return 0.50

# =====================================================================
# BIST-100 AYRIŞTIRMA VE ALFA SEÇİM ÇEKİRDEĞİ
# =====================================================================

class BISTDecomposer:
    def __init__(self):
        self.sector_map = {}
        for cluster, data in SECTOR_CLUSTERS.items():
            for sym in data["symbols"]:
                self.sector_map[sym] = (cluster, data["weight"])

    def get_sector_info(self, symbol: str) -> tuple:
        """Sembolün sektörünü ve çarpan ağırlığını döner."""
        return self.sector_map.get(symbol, ("OTHER_INDUSTRIAL", 1.00))

    def evaluate_stock_alpha(
        self,
        symbol: str,
        price_series: np.ndarray,
        net_profit_margin: float = 0.18,
        fx_revenue_ratio: float = 0.65,
        debt_to_ebitda: float = 1.20,
        c_takas: float = 0.45,
        r_cancel: float = 0.25,
        epsilon: float = 1e-4
    ) -> AlphaStockScore:
        """
        T2SAIM BIST Alfa Skor Formülü:
        Score = ((NetKarMarji * FX_Ratio) / (Debt/EBITDA + eps)) * (1 - R_cancel) * (1 - C_takas) * W_sektor * (h / 0.50)
        """
        cluster, weight = self.get_sector_info(symbol)
        h = compute_hurst_fast(price_series)

        # Temel Finansal Çarpan Kalitesi
        fundamental_factor = (net_profit_margin * fx_revenue_ratio) / (max(0.1, debt_to_ebitda) + epsilon)
        
        # Sahtekarlık ve Manipülasyon İndirimi
        fraud_discount = max(0.01, (1.0 - r_cancel)) * max(0.01, (1.0 - c_takas))
        
        # Fraktal İvme Çarpanı
        fractal_factor = max(0.2, (h / 0.50))

        # Nihai Skor
        score = fundamental_factor * fraud_discount * weight * fractal_factor
        expected_alpha = score * 15.0  # Yıllık bazda normalize edilmiş alfa beklentisi (%)

        return AlphaStockScore(
            symbol=symbol,
            sector=cluster,
            score=round(score, 4),
            hurst_exponent=round(h, 4),
            c_takas=round(c_takas, 4),
            r_cancel=round(r_cancel, 4),
            expected_alpha=round(expected_alpha, 2),
            rank=0
        )

    def select_top_10_alpha(self, stock_evaluations: List[AlphaStockScore]) -> List[AlphaStockScore]:
        """Tüm BIST hisselerini skora göre sıralayıp Top 10 Alfa Listesini üretir."""
        sorted_stocks = sorted(stock_evaluations, key=lambda x: x.score, reverse=True)
        top_10 = sorted_stocks[:10]
        
        for idx, stock in enumerate(top_10, start=1):
            stock.rank = idx
            
        logger.info(f"Top 10 BIST Alfa Seçimi Tamamlandı. Lider: {top_10[0].symbol} (Skor: {top_10[0].score})")
        log_audit_event("TOP_10_BIST_ALPHA_SELECTED", {
            "top_1": top_10[0].symbol if top_10 else "NONE",
            "top_10_symbols": [s.symbol for s in top_10]
        })
        return top_10
