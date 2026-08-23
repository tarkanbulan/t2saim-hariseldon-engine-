#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM EMILIO GULLINI ECONOPHYSICS & MINSKY SINGULARITY ANALYZER (PHI_GULLINI)
Doktrin: Veritas Per Se · G_def Güvensizlik Modeli & 18 Kasım 2026 t* Minsky Borç Tekilliği
"""

import numpy as np
from datetime import datetime
from ..core.schemas import TelemetryInput

class GulliniProtocolAnalyzer:
    """
    Phi_Gullini Hesaplayıcı:
    G_def = 0.40 * TED_norm + 0.35 * CDS_norm + 0.25 * TrustDeficit_TCMB
    Phi_Gullini = 0.55 * G_def + 0.45 * exp(-(t* - t) / 90)
    """
    def __init__(self, t_star_str: str = "2026-11-18", horizon_days: float = 90.0):
        self.t_star = datetime.strptime(t_star_str, "%Y-%m-%d")
        self.horizon_days = horizon_days

    def analyze(self, data: TelemetryInput) -> float:
        # 1. Normalizasyonlar
        ted_norm = np.clip(data.ted_spread_pct / 6.0, 0.0, 1.0)
        cds_norm = np.clip((data.cds_5y - 200.0) / 400.0, 0.0, 1.0)
        trust_deficit = np.clip(data.tcmb_trust_deficit, 0.0, 1.0)

        # 2. Gullini Güvensizlik İndeksi (G_def)
        g_def = (0.40 * ted_norm) + (0.35 * cds_norm) + (0.25 * trust_deficit)

        # 3. Minsky t* Tekilliği Mesafesi
        delta_days = (self.t_star - data.timestamp).total_seconds() / 86400.0
        
        if delta_days > 0:
            minsky_factor = np.exp(-delta_days / self.horizon_days)
        else:
            minsky_factor = 1.0  # Tekillik günü aşıldı/ulaşıldı

        phi = (0.55 * g_def) + (0.45 * minsky_factor)
        return float(np.clip(phi, 0.0, 1.0))
