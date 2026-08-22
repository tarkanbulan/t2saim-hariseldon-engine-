#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM & HARI SELDON KARA KUTU (BLACK BOX) LOGGING ENGINE
Doktrin: Veritas Per Se · Sıfır Kayıpsız İşlem ve Hata Takibi
"""

import os
import sys
import logging
import json
import hashlib
from datetime import datetime
from logging.handlers import RotatingFileHandler

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
KARARGAH_LOG_DIR = r"E:\T2SAIM_NEXUS_MIRROR\0000_A_Karargah\02_KARA_KUTU_LOGS"

os.makedirs(LOCAL_LOG_DIR, exist_ok=True)
os.makedirs(KARARGAH_LOG_DIR, exist_ok=True)

class T2SAIMJsonFormatter(logging.Formatter):
    """Her log kaydını JSON Lines formatında yapılandırır."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage()
        }
        if hasattr(record, "payload_hash"):
            log_record["payload_hash"] = record.payload_hash
        if hasattr(record, "execution_ms"):
            log_record["execution_ms"] = record.execution_ms
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

def get_logger(module_name: str = "T2SAIM_CORE") -> logging.Logger:
    """T2SAIM Kara Kutu logger nesnesi üretir."""
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # 1. Konsol Çıktısı (Okunabilir Format)
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(logging.INFO)
        c_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%H:%M:%S")
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        # 2. Yerel Dönen Log Dosyası (.log)
        today_str = datetime.now().strftime("%Y%m%d")
        f_log_path = os.path.join(LOCAL_LOG_DIR, f"t2saim_execution_{today_str}.log")
        f_handler = RotatingFileHandler(f_log_path, maxBytes=10*1024*1024, backupCount=10, encoding="utf-8")
        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s()]: %(message)s")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

        # 3. Kara Kutu JSON Lines Kütüğü (Adli Kanıt Kütüğü)
        audit_path = os.path.join(LOCAL_LOG_DIR, f"t2saim_kara_kutu_audit_{today_str}.jsonl")
        a_handler = RotatingFileHandler(audit_path, maxBytes=20*1024*1024, backupCount=20, encoding="utf-8")
        a_handler.setLevel(logging.INFO)
        a_handler.setFormatter(T2SAIMJsonFormatter())
        logger.addHandler(a_handler)

    return logger

def log_audit_event(event_type: str, details: dict, raw_payload: str = None):
    """Önemli alım-satım, veri girişi veya kriz sinyallerini çift yönlü mühürler."""
    payload_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest() if raw_payload else "NO_PAYLOAD"
    now_iso = datetime.now().isoformat()

    record = {
        "timestamp": now_iso,
        "event_type": event_type,
        "payload_hash": payload_hash,
        "details": details
    }

    # Yerel ve Karargâh kütüklerine eşzamanlı yaz
    for target_dir in [LOCAL_LOG_DIR, KARARGAH_LOG_DIR]:
        audit_file = os.path.join(target_dir, "T2SAIM_KARA_KUTU_MASTER_AUDIT.jsonl")
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
