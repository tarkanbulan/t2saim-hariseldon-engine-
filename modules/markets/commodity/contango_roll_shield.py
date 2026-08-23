#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CONTANGO ROLL-BLEED ADLİ KALKANI (TICKET-COMMODITY-03)
Doktrin: Veritas Per Se · Vadeli Eğrisi Adli Denetimi & Sermaye Kanaması Vetosu
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

logger = get_logger("CONTANGO_ROLL_SHIELD")

# Kritik Eşikler
MAX_ALLOWED_CONTANGO_ROLL_BLEED = -0.020  # %2.0 aylık contango erimesi eşiği
DEEP_CONTANGO_ANNUAL_THRESHOLD = -0.150  # %15.0 yıllık contango sermaye kaybı

class ContangoAuditResult(BaseModel):
    symbol: str
    front_month_futures: float
    next_month_futures: float
    monthly_roll_yield_pct: float
    annualized_roll_yield_pct: float
    curve_state: str = Field(..., description="BACKWARDATION, MILD_CONTANGO, DEEP_CONTANGO_BLEED")
    is_cleared: bool
    rejection_code: Optional[str] = None

class ContangoRollShield:
    """
    Emtia Vadeli Eğrisinde Contango Sermaye Kanamasını (Roll-Bleed) Tespit Eden ve Veto Eden Kalkan.
    Formül: Roll_Yield = (F_0 - F_1) / F_0
    F_1 > F_0 -> Contango (Roll_Yield < 0) -> Sermaye Kanaması
    F_0 > F_1 -> Backwardation (Roll_Yield > 0) -> Pozitif Taşıma Primi
    """
    def __init__(
        self,
        max_monthly_bleed: float = MAX_ALLOWED_CONTANGO_ROLL_BLEED,
        max_annual_bleed: float = DEEP_CONTANGO_ANNUAL_THRESHOLD
    ):
        self.max_monthly_bleed = max_monthly_bleed
        self.max_annual_bleed = max_annual_bleed

    def audit_commodity_curve(
        self,
        symbol: str,
        front_month_price: float,
        next_month_price: float,
        is_physical_spot_trust: bool = False
    ) -> ContangoAuditResult:
        """
        Emtia vadeli sözleşmesini denetler.
        Eğer varlık fiziksel tröst ise (Örn: Darphane ALTIN.S1 veya Sprott Uranium SRUUF),
        vadeli roll maliyeti sıfırdır, doğrudan onaylanır.
        """
        # 1. Fiziki Tröst / Sertifika Muafiyeti (Fiziki kasada duran varlıklar roll kaybetmez)
        if is_physical_spot_trust or symbol == "ALTIN.S1":
            return ContangoAuditResult(
                symbol=symbol,
                front_month_futures=front_month_price,
                next_month_futures=next_month_price,
                monthly_roll_yield_pct=0.0,
                annualized_roll_yield_pct=0.0,
                curve_state="PHYSICAL_SPOT_BACKED",
                is_cleared=True,
                rejection_code=None
            )

        if front_month_price <= 0:
            return ContangoAuditResult(
                symbol=symbol,
                front_month_futures=front_month_price,
                next_month_futures=next_month_price,
                monthly_roll_yield_pct=0.0,
                annualized_roll_yield_pct=0.0,
                curve_state="INVALID_PRICE",
                is_cleared=False,
                rejection_code="INVALID_PRICE"
            )

        # 2. Roll Yield Hesabı
        monthly_roll = (front_month_price - next_month_price) / front_month_price
        annualized_roll = monthly_roll * 12.0

        # 3. Durum Sınıflandırması
        if monthly_roll > 0.0:
            state = "BACKWARDATION"
            cleared = True
            rejection = None
        elif monthly_roll >= self.max_monthly_bleed:
            state = "MILD_CONTANGO"
            cleared = True
            rejection = None
        else:
            state = "DEEP_CONTANGO_BLEED"
            cleared = False
            rejection = f"CONTANGO_ROLL_BLEED_EXCEEDED ({monthly_roll*100:.2f}% < {self.max_monthly_bleed*100:.2f}%)"

        if not cleared:
            logger.warning(f"🚨 EMTİA VETOSU [{symbol}]: {rejection}")
            log_audit_event("CONTANGO_BLEED_VETO", {
                "symbol": symbol,
                "monthly_roll_pct": monthly_roll * 100.0,
                "annualized_roll_pct": annualized_roll * 100.0,
                "rejection_code": rejection
            })

        return ContangoAuditResult(
            symbol=symbol,
            front_month_futures=front_month_price,
            next_month_futures=next_month_price,
            monthly_roll_yield_pct=round(monthly_roll * 100.0, 4),
            annualized_roll_yield_pct=round(annualized_roll * 100.0, 4),
            curve_state=state,
            is_cleared=cleared,
            rejection_code=rejection
        )

if __name__ == "__main__":
    shield = ContangoRollShield()
    print("Contango Roll Shield başarıyla hazırlandı.")
