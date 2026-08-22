#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TAKASBANK & FORENSIC FRAUD SHIELD (TICKET-TR-03)
Doktrin: Veritas Per Se · BVM ve Kripto Wash-Trading Karşıtı Adli Filtre
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("FRAUD_SHIELD")

# =====================================================================
# ADLİ DENETİM EŞİK DEĞERLERİ
# =====================================================================

MAX_C_TAKAS_THRESHOLD = 0.70       # %70 üzeri Takasbank konsantrasyonu tuzaktır
MAX_R_CANCEL_THRESHOLD = 0.85      # %85 üzeri emir iptali sahte tahtadır (Spoofing)
MAX_VPIN_TOXICITY = 0.45           # 0.45 üzeri VPIN toksik kurumsal kaçıştır
MAX_CRYPTO_WASH_TRADING = 0.40     # %40 üzeri yapay hacim şüphesi

class FraudAuditResult(BaseModel):
    symbol: str
    asset_type: str = Field(..., description="'BIST_EQUITY', 'CRYPTO', 'COMMODITY'")
    is_cleared: bool
    rejection_code: Optional[str] = None
    risk_score: float = Field(..., ge=0.0, le=1.0)
    details: Dict[str, Any]

# =====================================================================
# ADLİ SAHTEKÂRLIK VE MANİPÜLASYON KALKANI
# =====================================================================

class TakasFraudShield:
    def __init__(
        self,
        c_takas_limit: float = MAX_C_TAKAS_THRESHOLD,
        r_cancel_limit: float = MAX_R_CANCEL_THRESHOLD,
        vpin_limit: float = MAX_VPIN_TOXICITY,
        wash_trading_limit: float = MAX_CRYPTO_WASH_TRADING
    ):
        self.c_takas_limit = c_takas_limit
        self.r_cancel_limit = r_cancel_limit
        self.vpin_limit = vpin_limit
        self.wash_trading_limit = wash_trading_limit

    def audit_bist_equity(
        self,
        symbol: str,
        c_takas: float,
        r_cancel: float,
        vpin: float = 0.20
    ) -> FraudAuditResult:
        """
        BIST-100 hissesini Takasbank ve emir defteri manipülasyonlarına karşı denetler.
        """
        rejection_reasons = []
        
        # 1. Bıyıklı Yabancı / Tek Kurum Konsantrasyonu
        if c_takas >= self.c_takas_limit:
            rejection_reasons.append(f"C_TAKAS_EXCEEDED ({c_takas:.2f} >= {self.c_takas_limit})")

        # 2. Sahte Emir İptalleri ve Kademe Boşaltma (Spoofing)
        if r_cancel >= self.r_cancel_limit:
            rejection_reasons.append(f"R_CANCEL_SPOOFING ({r_cancel:.2f} >= {self.r_cancel_limit})")

        # 3. Akış Toksisitesi (VPIN)
        if vpin >= self.vpin_limit:
            rejection_reasons.append(f"VPIN_TOXICITY_HIGH ({vpin:.2f} >= {self.vpin_limit})")

        # Bileşik Risk Skoru
        risk_score = (c_takas * 0.40) + (r_cancel * 0.40) + (vpin * 0.20)
        risk_score = min(1.0, max(0.0, risk_score))

        is_cleared = len(rejection_reasons) == 0
        rejection_code = " | ".join(rejection_reasons) if rejection_reasons else None

        if not is_cleared:
            logger.warning(f"🚨 SAHTEKÂRLIK VETOSU [{symbol}]: {rejection_code}")
            log_audit_event("BIST_FRAUD_VETO", {"symbol": symbol, "rejection_code": rejection_code, "risk_score": risk_score})

        return FraudAuditResult(
            symbol=symbol,
            asset_type="BIST_EQUITY",
            is_cleared=is_cleared,
            rejection_code=rejection_code,
            risk_score=round(risk_score, 4),
            details={
                "c_takas": c_takas,
                "r_cancel": r_cancel,
                "vpin": vpin
            }
        )

    def audit_crypto_asset(
        self,
        symbol: str,
        wash_trading_score: float,
        funding_rate: float
    ) -> FraudAuditResult:
        """
        Kripto varlığı TAS-GNN Wash-Trading ve yapay hacim tuzaklarına karşı denetler.
        """
        is_cleared = wash_trading_score <= self.wash_trading_limit
        rejection_code = f"WASH_TRADING_DETECTED ({wash_trading_score:.2f} > {self.wash_trading_limit})" if not is_cleared else None
        
        risk_score = wash_trading_score
        
        return FraudAuditResult(
            symbol=symbol,
            asset_type="CRYPTO",
            is_cleared=is_cleared,
            rejection_code=rejection_code,
            risk_score=round(risk_score, 4),
            details={
                "wash_trading_score": wash_trading_score,
                "funding_rate": funding_rate
            }
        )
