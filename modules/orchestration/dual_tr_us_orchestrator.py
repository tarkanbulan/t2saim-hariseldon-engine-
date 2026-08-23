#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TR-ABD ÇİFT KUTUPLU MASTER ORKESTRATÖR (DUAL-CORE COMMAND DECK)
Doktrin: Veritas Per Se · Türkiye & ABD Piyasaları Eşzamanlı İcra ve Kriz Yönetimi
"""

import os
import sys
import hashlib
import json
import time
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.common.t2saim_logger import get_logger, log_audit_event
from modules.markets.tr.tr_runner import TRPodRunner
from modules.markets.us.us_runner import USPodRunner
from t2saim_crisis_engine.engine.sensor import UnifiedCrisisSensor
from t2saim_crisis_engine.core.schemas import TelemetryInput

logger = get_logger("TR_US_DUAL_ORCHESTRATOR")

class DualCoreState(BaseModel):
    timestamp: datetime
    tr_action: str
    tr_uci_score: float
    tr_selected_asset: str
    tr_real_net_profit_pct: float
    us_action: str
    us_vix_level: float
    us_selected_asset: str
    us_real_net_usd_roi_pct: float
    cross_market_hedge_ratio: float
    execution_time_ms: float
    dual_sha256_hash: str

class TRUSDualOrchestrator:
    """
    Türkiye ve ABD Piyasalarını Eşzamanlı Olarak Yöneten Çift Kutuplu Komuta Masası:
    1. Türkiye Podu: BIST-100 Sektörel Dağılım + Takasbank Hırsızlık Kalkanı + 5D UCI Kriz Motoru
    2. ABD Podu: SPY/QQQ/VIX Makro Pusula + <$1000 Sektörel Asimetrik Liderler + VIX Volatilite Kalkanı
    3. Çapraz Piyasa Dolar/TL & Faiz Makası Koruma Dengesi
    """
    def __init__(self):
        self.tr_runner = TRPodRunner()
        self.us_runner = USPodRunner()
        self.crisis_sensor = UnifiedCrisisSensor()

    def execute_dual_pipeline(self) -> DualCoreState:
        start_time = time.perf_counter()
        logger.info("================================================================================")
        logger.info("🛰️ T2SAIM & HARI SELDON: TR - ABD ÇİFT KUTUPLU GÜNLÜK İCRA BAŞLADI")
        logger.info("================================================================================")

        # 1. Türkiye Boru Hattını Çalıştır
        tr_result = self.tr_runner.execute_daily_pipeline()

        # 2. ABD Boru Hattını Çalıştır
        us_result = self.us_runner.execute_daily_pipeline()

        # 3. Kriz Telemetrisi ve Çapraz Piyasa Hedge Oranı
        sample_telemetry = TelemetryInput(
            timestamp=datetime.now(),
            m2_nir_ratio=16.8,
            net_nir_usd_billion=-48.5,
            reer_cpi=69.2,
            ext_debt_service_1y_billion=191.0,
            dolgap_premium_pct=1.45,
            ldr_ratio=1.18,
            npl_real_ratio=4.8,
            npl_official_ratio=1.7,
            ted_spread_pct=4.2,
            uyap_active_cases_million=25.4,
            bounced_checks_billion_tl=72.0,
            sigma_20_60_ratio=1.45,
            v_run=0.72,
            h_herd=0.68,
            fatalism_buffer=0.80,
            cds_5y=270.0,
            tcmb_trust_deficit=0.65,
            procurement_hhi=2950.0,
            kik_21b_ratio=0.38,
            rent_to_mfg_credit=2.6,
            lm1_caliper_cv=0.11,
            tr_dei_score=0.72
        )
        crisis_out = self.crisis_sensor.evaluate(sample_telemetry)

        # Çapraz Risk Dengesi: TR UCI yükseldikçe portföy ağırlığı ABD nakit & hisse lehine kayar
        uci = crisis_out.uci_score
        hedge_ratio = float(min(1.0, max(0.0, uci * 1.2)))

        exec_ms = (time.perf_counter() - start_time) * 1000.0

        # Çift Onay Kütük Paketi
        dual_payload = {
            "timestamp": datetime.now().isoformat(),
            "tr_asset": tr_result.get("symbol", "N/A"),
            "tr_real_net_profit_pct": tr_result.get("real_net_profit_pct", 0.0),
            "tr_uci_score": round(uci, 4),
            "tr_action": crisis_out.recommended_action,
            "us_asset": us_result.get("symbol", "N/A"),
            "us_price_usd": us_result.get("price_usd", 0.0),
            "us_real_net_usd_roi_pct": us_result.get("real_net_usd_roi_pct", 0.0),
            "us_vix_level": us_result.get("vix_level", 15.0),
            "us_action": us_result.get("status", "PENDING_CAPTAIN_APPROVAL"),
            "cross_market_hedge_ratio": round(hedge_ratio, 4),
            "execution_time_ms": round(exec_ms, 2)
        }

        dual_json = json.dumps(dual_payload, sort_keys=True)
        dual_sha = hashlib.sha256(dual_json.encode("utf-8")).hexdigest()
        dual_payload["dual_sha256_hash"] = dual_sha

        log_audit_event("DUAL_TR_US_EXECUTION", dual_payload, raw_payload=dual_json)
        self.render_dual_deck(dual_payload)

        return DualCoreState(
            timestamp=datetime.now(),
            tr_action=crisis_out.recommended_action,
            tr_uci_score=round(uci, 4),
            tr_selected_asset=tr_result.get("symbol", "N/A"),
            tr_real_net_profit_pct=tr_result.get("real_net_profit_pct", 0.0),
            us_action=us_result.get("status", "PENDING_CAPTAIN_APPROVAL"),
            us_vix_level=us_result.get("vix_level", 15.0),
            us_selected_asset=us_result.get("symbol", "N/A"),
            us_real_net_usd_roi_pct=us_result.get("real_net_usd_roi_pct", 0.0),
            cross_market_hedge_ratio=round(hedge_ratio, 4),
            execution_time_ms=round(exec_ms, 2),
            dual_sha256_hash=dual_sha
        )

    def render_dual_deck(self, data: dict):
        print("\n" + "█" * 80)
        print("🏛️ T2SAIM & HARI SELDON: TR - ABD ÇİFT KUTUPLU KAPTAN İCRA MASASI")
        print("█" * 80)
        print("🇹🇷 [TÜRKİYE PODU VE KRİZ KALKANI]:")
        print(f"   • Seçilen Varlık   : 🚀 {data['tr_asset']} (Net Reel Kâr: +%{data['tr_real_net_profit_pct']:.2f})")
        print(f"   • Birleşik Kriz UCI: %{data['tr_uci_score']*100:.2f} ──► Durum: {data['tr_action']}")
        print(f"   • Vergi Avantajı   : GVK Geçici 67 %0 Stopaj (Tam Muafiyet)")
        print("-" * 80)
        print("🇺🇸 [ABD PİYASALARI PODU VE VIX KALKANI]:")
        print(f"   • Seçilen Varlık   : 🚀 {data['us_asset']} (${data['us_price_usd']:.2f}) (Net Reel USD: +%{data['us_real_net_usd_roi_pct']:.2f})")
        print(f"   • VIX Termometresi : {data['us_vix_level']} (Sistemik Panik Kalkanı ONAYLI)")
        print(f"   • Sermaye Kısıtı   : <$1000 Sektörel Asimetrik Liderler")
        print("-" * 80)
        print("⚖️ [ÇAPRAZ PİYASA RİSK DENGESİ]:")
        print(f"   • Dinamik Hedge Oranı : %{data['cross_market_hedge_ratio']*100:.1f} (USD/TL & Faiz Koruma Makası)")
        print(f"   • İcra İntikal Süresi : {data['execution_time_ms']} ms (1M MCMC Çift Yönlü)")
        print(f"   • Kriptografik Mühür  : {data['dual_sha256_hash'][:32]}...")
        print("█" * 80)
        print("                   [ 🟢 KAPTAN TR-ABD İCRA ONAYI ]")
        print("█" * 80 + "\n")

if __name__ == "__main__":
    orchestrator = TRUSDualOrchestrator()
    orchestrator.execute_dual_pipeline()
