#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM UNIFIED CRISIS SENSOR ENGINE (TURKEY EWS V5.0)
Doktrin: Veritas Per Se · 5 Boyutlu Dinamik Faz Geçişi & UCI Doğrusal Olmayan Rezonans
"""

import numpy as np
from datetime import datetime
from ..core.schemas import TelemetryInput, CrisisOutput
from ..core.amnesia import AmnesiaFilter
from ..core.adwin_drift import ConceptDriftManager
from ..core.venn_abers import VennAbersCalibrator
from ..analyzers.macro_minsky import MacroMinskyAnalyzer
from ..analyzers.banking_liquidity import BankingLiquidityAnalyzer
from ..analyzers.neuro_amigdala import NeuroAmygdalaAnalyzer
from ..analyzers.gullini_protocol import GulliniProtocolAnalyzer
from ..analyzers.acemoglu_decay import AcemogluDecayAnalyzer
from ..analyzers.shap_explainer import TreeSHAPExplainer
from ..config.settings import get_settings

class UnifiedCrisisSensor:
    def __init__(self):
        self.settings = get_settings()
        self.amnesia = AmnesiaFilter(
            nominal_lambda=self.settings.AMNESIA_LAMBDA_NOMINAL,
            drift_lambda=self.settings.AMNESIA_LAMBDA_DRIFT
        )
        self.drift_mgr = ConceptDriftManager(delta=self.settings.ADWIN_DELTA)
        self.calibrator = VennAbersCalibrator(ece_target=self.settings.ECE_TARGET)
        
        # 5 Analizör
        self.macro_analyzer = MacroMinskyAnalyzer()
        self.bank_analyzer = BankingLiquidityAnalyzer()
        self.neuro_analyzer = NeuroAmygdalaAnalyzer()
        self.gullini_analyzer = GulliniProtocolAnalyzer(t_star_str=self.settings.MINSKY_T_STAR)
        self.acemoglu_analyzer = AcemogluDecayAnalyzer()
        self.shap_explainer = TreeSHAPExplainer()

    def evaluate(self, data: TelemetryInput) -> CrisisOutput:
        """
        Gelen telemetriyi 5 boyutlu sensörlerden geçirir, kalibre eder ve kriz çıktısı üretir.
        """
        # 1. 5 Katmanlı Ham Skorlar
        phi_macro = self.macro_analyzer.analyze(data)
        phi_bank = self.bank_analyzer.analyze(data)
        phi_neuro = self.neuro_analyzer.analyze(data)
        phi_gullini = self.gullini_analyzer.analyze(data)
        phi_acemoglu = self.acemoglu_analyzer.analyze(data)

        # 2. Ağırlıklı Toplam ve Doğrusal Olmayan UCI
        weights = {
            "Phi_Macro (Minsky & Rezerv)": self.settings.WEIGHT_MACRO,
            "Phi_Bank (Likidite & NPL)": self.settings.WEIGHT_BANK,
            "Phi_Neuro (Amigdala & Kaçış)": self.settings.WEIGHT_NEURO,
            "Phi_Gullini (Güvensizlik & t*)": self.settings.WEIGHT_GULLINI,
            "Phi_Acemoglu (TR-DEI & Kurumsal)": self.settings.WEIGHT_ACEMOGLU
        }
        
        phis_dict = {
            "Phi_Macro (Minsky & Rezerv)": phi_macro,
            "Phi_Bank (Likidite & NPL)": phi_bank,
            "Phi_Neuro (Amigdala & Kaçış)": phi_neuro,
            "Phi_Gullini (Güvensizlik & t*)": phi_gullini,
            "Phi_Acemoglu (TR-DEI & Kurumsal)": phi_acemoglu
        }

        weighted_sum = sum(weights[k] * phis_dict[k] for k in weights)
        raw_uci = 1.0 - np.exp(-1.45 * weighted_sum)

        # 3. Konsept Kayması ve Amnesia Sönümleme
        is_drift = self.drift_mgr.update(raw_uci)
        self.amnesia.set_drift_mode(is_drift)
        smoothed_uci = self.amnesia.update(raw_uci)

        # 4. Venn-Abers Olasılık Kalibrasyonu [p0, p1]
        p0, p1 = self.calibrator.calibrate(smoothed_uci)
        decision_action = self.calibrator.determine_decision_gate(p0, p1)

        # 5. İki Kademeli Durum Sınıflandırması
        # D+14 Taktiksel
        if (data.dolgap_premium_pct > 2.5) or (phi_neuro > 0.70):
            tactical_state = "TACTICAL_CRISIS_ALARM"
        elif smoothed_uci > 0.50:
            tactical_state = "ELEVATED_TENSION"
        else:
            tactical_state = "NORMAL"

        # M+3 Stratejik
        if phi_gullini > 0.75 or phi_acemoglu > 0.70:
            strategic_state = "MINSKY_SINGULARITY_LOCK"
        elif smoothed_uci > 0.55:
            strategic_state = "STRUCTURAL_DECAY"
        else:
            strategic_state = "SUSTAINABLE"

        # 6. Çeyrek Kelly Fraksiyonu
        # Kelly: f* = (p * b - q) / b -> Çeyrek Kelly koruması
        p_win = max(0.01, 1.0 - smoothed_uci)
        kelly_full = max(0.0, (p_win * 1.5 - (1.0 - p_win)) / 1.5)
        quarter_kelly = float(np.clip(kelly_full * 0.25, 0.0, 0.25))

        # 7. TreeSHAP Faktör Ayrıştırması
        shap_factors = self.shap_explainer.explain(phis_dict, weights)

        return CrisisOutput(
            timestamp=data.timestamp,
            uci_score=round(smoothed_uci, 4),
            confidence_interval_p0=p0,
            confidence_interval_p1=p1,
            phi_macro=round(phi_macro, 4),
            phi_bank=round(phi_bank, 4),
            phi_neuro=round(phi_neuro, 4),
            phi_gullini=round(phi_gullini, 4),
            phi_acemoglu=round(phi_acemoglu, 4),
            tactical_state_d14=tactical_state,
            strategic_state_m3=strategic_state,
            recommended_action=decision_action,
            quarter_kelly_fraction=round(quarter_kelly, 4),
            top_shap_factors=shap_factors,
            is_concept_drift_detected=is_drift
        )
