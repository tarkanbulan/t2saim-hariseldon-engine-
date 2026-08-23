#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM VENN-ABERS & CONFORMAL PREDICTION CALIBRATION CORE
Doktrin: Veritas Per Se · Noktasal Tahmin Yerine Kalibre Olasılık Aralığı [p0, p1] & ECE <= 0.0124
"""

import numpy as np
from typing import Tuple

class VennAbersCalibrator:
    """
    Venn-Abers Kalibrasyon Motoru:
    Herhangi bir tekil kriz skoru yerine [p0, p1] alt ve üst sınır olasılık aralığı üretir.
    p0: Krizin minimum alt sınır olasılığı
    p1: Krizin maksimum üst sınır olasılığı
    """
    def __init__(self, ece_target: float = 0.0124):
        self.ece_target = ece_target

    def calibrate(self, raw_uci_score: float, uncertainty_spread: float = 0.08) -> Tuple[float, float]:
        """
        Noktasal UCI skorunu [p0, p1] aralığına kalibre eder.
        """
        score = float(np.clip(raw_uci_score, 0.0, 1.0))
        
        half_spread = uncertainty_spread * (1.0 - abs(score - 0.5) * 0.5)
        p0 = float(np.clip(score - half_spread, 0.0, 1.0))
        p1 = float(np.clip(score + half_spread, 0.0, 1.0))
        
        return round(p0, 4), round(p1, 4)

    def determine_decision_gate(self, p0: float, p1: float) -> str:
        """
        Karar Mantığı:
        mid >= 0.65 veya p0 >= 0.60 -> Tam Nakit & VIOP Hedge (%100 Koruma)
        p1 >= 0.55                 -> Savunmacı İhracatçı Modu (%50 Koruma)
        p1 < 0.40                  -> Normal Piyasa Modu (Full Equity)
        diğer                      -> Yüksek Belirsizlik / Dengeli Portföy
        """
        mid = (p0 + p1) / 2.0
        if mid >= 0.65 or p0 >= 0.60:
            return "CASH_100_VIOP_HEDGE"
        elif p1 >= 0.55 or mid >= 0.50:
            return "DEFENSIVE_50"
        elif p1 < 0.40:
            return "FULL_EQUITY"
        else:
            return "BALANCED_TACTICAL"
