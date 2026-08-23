#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TREESHAP FACTORED CRISIS EXPLAINER
Doktrin: Veritas Per Se · Kriz Tetikleyicilerinin Şeffaf Yüzdesel Açıklanabilirliği
"""

from typing import List, Dict
from ..core.schemas import SHAPFactor

class TreeSHAPExplainer:
    """
    Kriz Tetikleyicisi Faktör Ayrıştırıcısı:
    SHAP_i = (w_i * Phi_i) / sum(w_k * Phi_k) * 100
    """
    def explain(
        self,
        phis: Dict[str, float],
        weights: Dict[str, float]
    ) -> List[SHAPFactor]:
        contributions = {}
        total_weighted = 0.0
        
        for name, phi in phis.items():
            w = weights.get(name, 0.20)
            contrib = w * phi
            contributions[name] = contrib
            total_weighted += contrib

        factors = []
        for name, contrib in contributions.items():
            pct = (contrib / total_weighted * 100.0) if total_weighted > 0 else 20.0
            factors.append(SHAPFactor(
                factor_name=name,
                weight_pct=round(pct, 2),
                contribution_score=round(contrib, 4)
            ))
            
        factors.sort(key=lambda x: x.weight_pct, reverse=True)
        return factors
