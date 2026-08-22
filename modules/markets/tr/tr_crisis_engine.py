#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TURKEY L4 AMYGDALA CRISIS & 1M VECTORIZED MCMC ENGINE (TICKET-TR-04)
Doktrin: Veritas Per Se · Merton Jump Diffusion, GVK Geçici 67 %0 Stopaj ve Reel Kâr
"""

import time
import numpy as np
from typing import Dict, Any
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("TR_CRISIS_ENGINE")

DEFAULT_FRICTION = 0.0006  # %0.04 Aracı kurum komisyonu + %0.02 Slippage = %0.06

class MCMCProjectionResult(BaseModel):
    symbol: str
    horizon_days: int
    nominal_mean_roi: float
    nominal_p05_worst: float
    nominal_p95_best: float
    inflation_rate: float
    fx_depreciation: float
    real_net_profit: float
    psi_tr: float
    crisis_regime: str
    gvk_tax_deduction: float = 0.0
    execution_time_ms: float

# =====================================================================
# L4 AMİGDALA KRİZ VE 1 MİLYON MCMC SİMÜLASYON MOTORU
# =====================================================================

class TRCrisisEngine:
    def __init__(self, friction: float = DEFAULT_FRICTION):
        self.friction = friction

    def compute_psi_tr(
        self,
        a_load: float,
        pfc_control: float,
        usd_try_change_pct: float,
        s_decay: float = 0.95,
        epsilon: float = 1e-4
    ) -> float:
        """
        Türkiye Amigdala Kriz Katsayısı:
        Psi_TR = ((A_load * (1 + KurSoku)) / (PFC_control + eps)) * S_decay
        """
        kur_soku = max(0.0, usd_try_change_pct)
        psi = ((a_load * (1.0 + kur_soku)) / (max(0.05, pfc_control) + epsilon)) * s_decay
        return float(np.clip(psi, 0.0, 1.0))

    def run_1m_vectorized_mcmc(
        self,
        symbol: str,
        current_price: float,
        expected_drift: float,
        historical_volatility: float,
        psi_tr: float,
        horizon_days: int = 20,
        n_simulations: int = 1_000_000,
        monthly_inflation: float = 0.025,
        monthly_fx_change: float = 0.015
    ) -> MCMCProjectionResult:
        """
        1.000.000 Vektörize MCMC Simülasyonu:
        Student-t (nu=4.5) Ağır Kuyruk + Merton Jump Diffusion (<120 ms)
        """
        t0 = time.perf_counter()

        dt = horizon_days / 252.0
        
        # 1. Merton Jump Parametreleri (Amigdala Çöküş İhtimali)
        jump_lambda = 0.5 + (psi_tr * 2.0)   # Kriz anında sıçrama frekansı artar
        jump_mean = -0.05 * psi_tr           # Kriz anında sıçrama yönü aşağıdır
        jump_vol = 0.10

        # 2. Student-t Dağılımı (nu=4.5 Ağır Kuyruk Şokları)
        nu = 4.5
        t_dist = np.random.standard_t(df=nu, size=n_simulations)
        # Varyansı normalize et
        t_dist = t_dist * np.sqrt((nu - 2) / nu)

        # 3. Poisson Sıçramaları
        poisson_jumps = np.random.poisson(lam=jump_lambda * dt, size=n_simulations)
        jump_sizes = np.random.normal(loc=jump_mean, scale=jump_vol, size=n_simulations) * poisson_jumps

        # 4. Difüzyon + Sıçrama Getiri Yolu
        drift = (expected_drift - 0.5 * (historical_volatility ** 2)) * dt
        diffusion = historical_volatility * np.sqrt(dt) * t_dist
        
        simulated_returns = drift + diffusion + jump_sizes
        simulated_prices = current_price * np.exp(simulated_returns)
        nominal_rois = (simulated_prices - current_price) / current_price

        # İstatistiki Çıktılar
        mean_roi = float(np.mean(nominal_rois))
        p05_worst = float(np.percentile(nominal_rois, 5))
        p95_best = float(np.percentile(nominal_rois, 95))

        # 5. GVK Geçici 67 (%0 Stopaj) ve Reel Net Alım Gücü Kârı
        # Reel Net Kâr = ((1 + Nominal Kâr) / (1 + Enflasyon + Kur Artışı)) - 1 - Sürtünme
        combined_discount = monthly_inflation + monthly_fx_change
        real_net_profit = ((1.0 + mean_roi) / (1.0 + combined_discount)) - 1.0 - self.friction

        # Kriz Rejimi Tespiti
        if psi_tr >= 0.75:
            crisis_regime = "PANIC_COLLAPSE_DIP_OPPORTUNITY"
        elif psi_tr >= 0.45:
            crisis_regime = "MODERATE_TENSION_CAUTION"
        else:
            crisis_regime = "NORMAL_CALM_FLOW"

        execution_time_ms = (time.perf_counter() - t0) * 1000.0

        logger.info(
            f"1M MCMC Tamamlandı [{symbol}]: Nominal={mean_roi*100:.2f}%, "
            f"Reel Net={real_net_profit*100:.2f}%, Süre={execution_time_ms:.2f}ms"
        )
        log_audit_event("MCMC_1M_SIMULATION", {
            "symbol": symbol,
            "nominal_roi": mean_roi,
            "real_roi": real_net_profit,
            "psi_tr": psi_tr,
            "latency_ms": execution_time_ms
        })

        return MCMCProjectionResult(
            symbol=symbol,
            horizon_days=horizon_days,
            nominal_mean_roi=round(mean_roi * 100, 2),
            nominal_p05_worst=round(p05_worst * 100, 2),
            nominal_p95_best=round(p95_best * 100, 2),
            inflation_rate=round(monthly_inflation * 100, 2),
            fx_depreciation=round(monthly_fx_change * 100, 2),
            real_net_profit=round(real_net_profit * 100, 2),
            psi_tr=round(psi_tr, 4),
            crisis_regime=crisis_regime,
            gvk_tax_deduction=0.0,  # %0 Stopaj Vergisiz
            execution_time_ms=round(execution_time_ms, 2)
        )
