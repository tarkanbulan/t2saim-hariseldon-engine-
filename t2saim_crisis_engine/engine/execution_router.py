#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM EXECUTION ROUTER & CAPITAL PROTECTION GATEWAY
Doktrin: Veritas Per Se · Çeyrek Kelly, Panik Kapısı & VIOP Kur Hedge Yönlendiricisi
"""

from typing import Dict
from ..core.schemas import CrisisOutput

class ExecutionRouter:
    """
    Sermaye Koruma ve Karar Yönlendirici:
    Kriz seviyesine göre portföy varlık dağılımını belirler.
    """
    def route_portfolio(self, crisis_out: CrisisOutput) -> Dict[str, any]:
        action = crisis_out.recommended_action
        uci = crisis_out.uci_score
        
        if action == "CASH_100_VIOP_HEDGE" or uci >= 0.65:
            allocation = {
                "CASH_TL_OR_USD": 0.80,
                "VIOP_USD_TRY_HEDGE": 0.20,
                "EQUITY_ALPHA": 0.00,
                "DEFENSIVE_EXPORTERS": 0.00
            }
            alert_level = "RED_PANIC_GATE_ACTIVE"
            hedge_status = "100% CAPITAL SHIELD & VIOP HEDGE"
        elif action == "DEFENSIVE_50" or uci >= 0.50:
            allocation = {
                "CASH_TL_OR_USD": 0.50,
                "VIOP_USD_TRY_HEDGE": 0.10,
                "DEFENSIVE_EXPORTERS": 0.40,
                "EQUITY_ALPHA": 0.00
            }
            alert_level = "YELLOW_DEFENSIVE_MODE"
            hedge_status = "50% CASH + SAVUNMACI İHRACATÇILAR"
        else:
            allocation = {
                "EQUITY_ALPHA": 0.70,
                "DEFENSIVE_EXPORTERS": 0.20,
                "CASH_TL_OR_USD": 0.10,
                "VIOP_USD_TRY_HEDGE": 0.00
            }
            alert_level = "GREEN_EXPANSION"
            hedge_status = "NORMAL ALPHA SPREAD"

        return {
            "timestamp": crisis_out.timestamp.isoformat(),
            "uci_score": crisis_out.uci_score,
            "action": action,
            "alert_level": alert_level,
            "hedge_status": hedge_status,
            "quarter_kelly": crisis_out.quarter_kelly_fraction,
            "target_allocation": allocation
        }
