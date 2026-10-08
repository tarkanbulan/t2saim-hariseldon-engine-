from pathlib import Path

theory_dir = Path(r"E:\Tarkan_Analiz\New_Page_Ews\08_Theory")
sub_dir = theory_dir / "sub_platforms"
master_file = theory_dir / "T2SAIM_MASTER_EWS_BIRLESIK_ADLI_PLATFORMU.html"

with open(master_file, "r", encoding="utf-8") as f:
    standalone_html = f.read()

sub_files = {
    "p1": "p1_birlesik_ews.html",
    "p2": "p2_kuresel_harp.html",
    "p3": "p3_master_gozlemevi.html",
    "p4": "p4_sistemik_analiz.html",
    "p5": "p5_karanlik_madde.html",
    "p6": "p6_ekonomi_otopsisi.html",
    "p7": "p7_adli_rapor_80yil.html",
    "p8": "p8_egemen_risk_core20.html",
    "p9": "p9_core20_kokpit.html"
}

for pid, sname in sub_files.items():
    sp = sub_dir / sname
    if sp.exists():
        with open(sp, "r", encoding="utf-8") as f:
            raw_html = f.read()
        escaped_srcdoc = raw_html.replace("&", "&amp;").replace('"', "&quot;")
        target_tag = f'<iframe id="frame-{pid}" src="sub_platforms/{sname}"'
        repl_tag = f'<iframe id="frame-{pid}" src="sub_platforms/{sname}" srcdoc="{escaped_srcdoc}"'
        standalone_html = standalone_html.replace(target_tag, repl_tag)

standalone_file = theory_dir / "T2SAIM_MASTER_EWS_STANDALONE_PORTABLE.html"
with open(standalone_file, "w", encoding="utf-8") as f:
    f.write(standalone_html)

print(f"Standalone portable platform created successfully: {standalone_file} ({len(standalone_html):,} bytes)")
