#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM VIX VOLATILITY & TAIL-RISK ADLİ KALKANI (TICKET-US-03)
Doktrin: Veritas Per Se · VIX Spike Tespiti & Sistemik Likidasyon Vetosu
"""

import os
import sys
from pydantic import BaseModel, Field
from typing import Optional

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("VIX_VOLATILITY_SHIELD")

VIX_CRITICAL_LEVEL = 28.5        # Mutlak kriz / panik eşiği
VIX_DAILY_SPIKE_MAX_PCT = 20.0   # Günlük maksimum tolere edilen VIX sıçraması (%)

class VIXAuditResult(BaseModel):
    vix_level: float = Field(..., ge=0.0)
    vix_1d_change_pct: float
    market_state: str = Field(..., description="CALM_FLOW, ELEVATED_VOLATILITY, SYSTEMIC_PANIC_SPIKE")
    is_cleared: bool
    rejection_code: Optional[str] = None

class VIXVolatilityShield:
    """
    ABD Piyasaları için VIX Volatilite ve Kuyruk Riski Kalkanı:
    1. VIX >= 28.5 ise VETO
    2. Delta_VIX >= %20.0 ise VETO
    """
    def __init__(
        self,
        max_vix_level: float = VIX_CRITICAL_LEVEL,
        max_vix_spike: float = VIX_DAILY_SPIKE_MAX_PCT
    ):
        self.max_vix_level = max_vix_level
        self.max_vix_spike = max_vix_spike

    def audit_us_market(
        self,
        current_vix: float,
        previous_vix: float
    ) -> VIXAuditResult:
        if previous_vix <= 0:
            previous_vix = current_vix
            
        vix_change_pct = ((current_vix - previous_vix) / previous_vix) * 100.0

        if current_vix >= self.max_vix_level:
            state = "SYSTEMIC_PANIC_SPIKE"
            cleared = False
            rejection = f"VIX_ABSOLUTE_CRITICAL ({current_vix:.2f} >= {self.max_vix_level})"
        elif vix_change_pct >= self.max_vix_spike:
            state = "SYSTEMIC_PANIC_SPIKE"
            cleared = False
            rejection = f"VIX_DAILY_SPIKE_EXCEEDED (+{vix_change_pct:.2f}% >= +{self.max_vix_spike}%)"
        elif current_vix >= 22.0:
            state = "ELEVATED_VOLATILITY"
            cleared = True
            rejection = None
        else:
            state = "CALM_FLOW"
            cleared = True
            rejection = None

        if not cleared:
            logger.warning(f"🚨 ABD PİYASASI VETOSU: {rejection}")
            log_audit_event("VIX_SHIELD_VETO", {
                "current_vix": current_vix,
                "vix_change_pct": vix_change_pct,
                "rejection_code": rejection
            })

        return VIXAuditResult(
            vix_level=round(current_vix, 2),
            vix_1d_change_pct=round(vix_change_pct, 2),
            market_state=state,
            is_cleared=cleared,
            rejection_code=rejection
        )

if __name__ == "__main__":
    shield = VIXVolatilityShield()
    print("VIX Volatility Shield hazır.")
