#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM & HARI SELDON CRYPTOGRAPHIC PROVENANCE & ANTI-TAMPERING VERIFIER
Canonical Vault: E:\T2SAIM_NEXUS_MIRROR\000_SPARK\T2SAIM _OS\Prediction
Author: Tarkan Bulan (Kaptan Tarco) & James William (DZV)
License: T2SAIM Epistemic Forensic Protocol (Veritas Per Se)
"""

import os
import json
import hashlib
import sys
from datetime import datetime

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
LEDGER_FILE = os.path.join(VAULT_DIR, "CRYPTOGRAPHIC_PROVENANCE_LEDGER.json")

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_verification():
    print("=" * 80)
    print("🏛️ T2SAIM & HARI SELDON: CANONICAL PROVENANCE & ANTI-TAMPERING VERIFIER")
    print(f"Konum: {VAULT_DIR}")
    print(f"Zaman: {datetime.now().isoformat()}")
    print("=" * 80)

    if not os.path.exists(LEDGER_FILE):
        print(f"[HATA] Provenance kütüğü bulunamadı: {LEDGER_FILE}")
        sys.exit(1)

    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    records = ledger.get("records", [])
    total_files = len(records)
    passed = 0
    failed = 0
    missing = 0

    print(f"Kütük Protokolü : {ledger.get('protocol')}")
    print(f"Oluşturulma     : {ledger.get('creation_timestamp')}")
    print(f"Kayıtlı Dosya   : {total_files} adet\n")

    print("-" * 80)
    print(f"{'DURUM':<10} | {'BOYUT':<10} | {'DOSYA ADI':<40} | {'HASH KONTROLÜ'}")
    print("-" * 80)

    for rec in records:
        rel_path = rec.get("relative_path")
        expected_hash = rec.get("sha256_hash")
        fname = rec.get("file_name")
        full_path = os.path.join(VAULT_DIR, rel_path)

        if not os.path.exists(full_path):
            print(f"❌ KAYIP    | {'-':<10} | {fname[:40]:<40} | Dosyaya erişilemiyor!")
            missing += 1
            continue

        actual_hash = compute_sha256(full_path)
        file_size = os.path.getsize(full_path)

        if actual_hash == expected_hash:
            print(f"✅ ONAY     | {file_size:<10} | {fname[:40]:<40} | {actual_hash[:16]}... (Eşleşti)")
            passed += 1
        else:
            print(f"⚠️ TAHRİFAT | {file_size:<10} | {fname[:40]:<40} | Hash uyuşmuyor!")
            failed += 1

    print("-" * 80)
    print(f"SONUÇ: Toplam: {total_files} | Başarılı: {passed} | Tahrifat: {failed} | Kayıp: {missing}")
    
    if failed == 0 and missing == 0:
        print("\n🏆 ADLİ DOĞRULAMA: %100 BAŞARILI. SIFIR TAHRİFAT, SIFIR GEÇMİŞ UYDURMA KANITLANDI.")
    else:
        print("\n🚨 DİKKAT: Bazı dosyalarda değişiklik veya eksiklik tespit edildi!")
    print("=" * 80)

if __name__ == "__main__":
    run_verification()
