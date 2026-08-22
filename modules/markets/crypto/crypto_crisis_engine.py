#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRYPTO 1M MCMC ENGINE & FUNDING BASIS ARBITRAGE (TICKET-CRYPTO-04)
Doktrin: Veritas Per Se · Student-t (nu=3.5) Kripto Ağır Kuyruk Şokları ve Reel USD Getiri
"""

import time
import numpy as np
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("CRYPTO_CRISIS_ENGINE")

CRYPTO_TOTAL_FRICTION = 0.0015  # %0.10 Borsa Taker Komisyonu + %0.05 Slippage/Gas

class CryptoMCMCResult(BaseModel):
    symbol: str
    horizon_days: int
    nominal_mean_roi_pct: float
    worst_p05_pct: float
    best_p95_pct: float
    funding_basis_annual_pct: float
    usd_inflation_pct: float
    real_net_usd_roi_pct: float
    liquidation_risk_state: str
    execution_time_ms: float

# =====================================================================
# KRİPTO 1 MİLYON MCMC VE LİKİDASYON KRİZ MOTORU
# =====================================================================

class CryptoCrisisEngine:
    def __init__(self, friction: float = CRYPTO_TOTAL_FRICTION):
        self.friction = friction

    def run_1m_crypto_mcmc(
        self,
        symbol: str,
        current_price_usd: float,
        expected_drift: float,
        historical_volatility: float,
        funding_rate_8h: float = 0.0001,
        macro_regime: str = "BULL_EXPANSION",
        horizon_days: int = 14,
        n_simulations: int = 1_000_000,
        usd_annual_inflation: float = 0.032
    ) -> CryptoMCMCResult:
        """
        1.000.000 Vektörize Kripto MCMC Simülasyonu:
        Student-t (nu=3.5 Ultra Ağır Kuyruk) + Poisson Likidasyon Sıçramaları (<150 ms)
        """
        t0 = time.perf_counter()
        dt = horizon_days / 365.0

        # 1. Kripto Likidasyon Sıçrama Parametreleri (Rejime Göre)
        if macro_regime == "BEAR_LIQUIDATION":
            jump_lambda = 3.5
            jump_mean = -0.12  # Sert likidasyon basamağı
            jump_vol = 0.18
        elif macro_regime == "BULL_EXPANSION":
            jump_lambda = 1.2
            jump_mean = 0.04
            jump_vol = 0.12
        else:
            jump_lambda = 1.8
            jump_mean = -0.02
            jump_vol = 0.10

        # 2. Student-t Kripto Kuyruk Dağılımı (nu=3.5)
        nu = 3.5
        t_dist = np.random.standard_t(df=nu, size=n_simulations)
        t_dist = t_dist * np.sqrt((nu - 2.0) / nu)

        # 3. Poisson Likidasyon Şokları
        poisson_jumps = np.random.poisson(lam=jump_lambda * dt, size=n_simulations)
        jump_sizes = np.random.normal(loc=jump_mean, scale=jump_vol, size=n_simulations) * poisson_jumps

        # 4. Yörünge Simülasyonu
        drift = (expected_drift - 0.5 * (historical_volatility ** 2)) * dt
        diffusion = historical_volatility * np.sqrt(dt) * t_dist
        
        simulated_returns = drift + diffusion + jump_sizes
        simulated_prices = current_price_usd * np.exp(simulated_returns)
        nominal_rois = (simulated_prices - current_price_usd) / current_price_usd

        mean_roi = float(np.mean(nominal_rois))
        p05_worst = float(np.percentile(nominal_rois, 5))
        p95_best = float(np.percentile(nominal_rois, 95))

        # 5. Funding Rate Arbitrajı ve Net Reel USD Getiri
        funding_basis_annual = funding_rate_8h * 3 * 365 * 100.0
        period_funding = (funding_basis_annual / 100.0) * dt
        
        period_usd_inflation = (usd_annual_inflation) * dt
        # Reel USD Kâr = ((1 + Nominal + Funding) / (1 + USD Enflasyon)) - 1 - Sürtünme
        real_net_usd_roi = ((1.0 + mean_roi + period_funding) / (1.0 + period_usd_inflation)) - 1.0 - self.friction

        execution_time_ms = (time.perf_counter() - t0) * 1000.0

        liquidation_risk_state = "HIGH_LEVERAGE_CASCADE" if p05_worst < -0.25 else "STABLE_FLOW"

        logger.info(
            f"1M Kripto MCMC [{symbol}]: Nominal={mean_roi*100:.2f}%, "
            f"Reel USD={real_net_usd_roi*100:.2f}%, Süre={execution_time_ms:.2f}ms"
        )
        log_audit_event("CRYPTO_1M_MCMC_SIMULATION", {
            "symbol": symbol,
            "nominal_roi": mean_roi,
            "real_usd_roi": real_net_usd_roi,
            "latency_ms": execution_time_ms
        })

        return CryptoMCMCResult(
            symbol=symbol,
            horizon_days=horizon_days,
            nominal_mean_roi_pct=round(mean_roi * 100, 2),
            worst_p05_pct=round(p05_worst * 100, 2),
            best_p95_pct=round(p95_best * 100, 2),
            funding_basis_annual_pct=round(funding_basis_annual, 2),
            usd_inflation_pct=round(period_usd_inflation * 100, 2),
            real_net_usd_roi_pct=round(real_net_usd_roi * 100, 2),
            liquidation_risk_state=liquidation_risk_state,
            execution_time_ms=round(execution_time_ms, 2)
        )
