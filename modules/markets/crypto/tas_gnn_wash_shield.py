#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TAS-GNN CRYPTO WASH-TRADING & ON-CHAIN FRAUD SHIELD (TICKET-CRYPTO-03)
Doktrin: Veritas Per Se · Yapay Hacim, Kendiyle İşlem (Self-Trade) ve Döngüsel Graf Veto
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("TAS_GNN_WASH_SHIELD")

MAX_ALLOWED_WASH_SCORE = 0.40     # %40 üzeri yapay hacim doğrudan VETO
MAX_SELF_TRADE_RATIO = 0.15       # %15 üzeri kendisiyle işlem tahta sahtekarlığıdır
MAX_VOLUME_TO_ACTIVE_USERS = 50.0 # Kullanıcı başına aşırı yapay şişirme eşiği

class CryptoFraudAuditResult(BaseModel):
    symbol: str
    is_cleared: bool
    rejection_code: Optional[str] = None
    wash_trading_score: float = Field(..., ge=0.0, le=1.0)
    self_trade_ratio: float
    graph_cycle_detected: bool
    risk_assessment: str

# =====================================================================
# TAS-GNN GRAF SAHTEKÂRLIK VE YAPAY HACİM KALKANI
# =====================================================================

class TASGNNWashShield:
    def __init__(
        self,
        wash_limit: float = MAX_ALLOWED_WASH_SCORE,
        self_trade_limit: float = MAX_SELF_TRADE_RATIO
    ):
        self.wash_limit = wash_limit
        self.self_trade_limit = self_trade_limit

    def audit_crypto_asset(
        self,
        symbol: str,
        wash_trading_score: float,
        self_trade_ratio: float = 0.05,
        graph_cycle_detected: bool = False,
        volume_to_users_ratio: float = 12.0
    ) -> CryptoFraudAuditResult:
        """
        Kripto varlığı TAS-GNN graf döngüleri ve yapay hacim tuzaklarına karşı denetler.
        """
        rejection_reasons = []

        # 1. TAS-GNN Yapay Hacim Skoru
        if wash_trading_score > self.wash_limit:
            rejection_reasons.append(f"WASH_TRADING_HIGH ({wash_trading_score:.2f} > {self.wash_limit})")

        # 2. Tahtada Kendi Kendine Alım-Satım (Self-Trading)
        if self_trade_ratio > self.self_trade_limit:
            rejection_reasons.append(f"SELF_TRADE_EXCEEDED ({self_trade_ratio:.2f} > {self.self_trade_limit})")

        # 3. On-Chain Döngüsel Transfer (A -> B -> C -> A Graph Cycle)
        if graph_cycle_detected:
            rejection_reasons.append("ONCHAIN_GRAPH_CYCLE_DETECTED (Circular Wash-Trading)")

        # 4. Kullanıcı Başına Anormal Hacim
        if volume_to_users_ratio > MAX_VOLUME_TO_ACTIVE_USERS:
            rejection_reasons.append(f"VOLUME_PER_USER_ANOMALY ({volume_to_users_ratio:.1f}x)")

        is_cleared = len(rejection_reasons) == 0
        rejection_code = " | ".join(rejection_reasons) if rejection_reasons else None

        if not is_cleared:
            risk_assessment = "🚨 MANİPÜLATİF / YAPAY HACİM TUZAĞI (VETO)"
            logger.warning(f"🚨 KRİPTO VETOSU [{symbol}]: {rejection_code}")
            log_audit_event("CRYPTO_WASH_VETO", {"symbol": symbol, "rejection": rejection_code})
        else:
            risk_assessment = "🟢 ORGANİK VE DOĞRULANMIŞ TAHTA"

        return CryptoFraudAuditResult(
            symbol=symbol,
            is_cleared=is_cleared,
            rejection_code=rejection_code,
            wash_trading_score=round(wash_trading_score, 4),
            self_trade_ratio=round(self_trade_ratio, 4),
            graph_cycle_detected=graph_cycle_detected,
            risk_assessment=risk_assessment
        )
