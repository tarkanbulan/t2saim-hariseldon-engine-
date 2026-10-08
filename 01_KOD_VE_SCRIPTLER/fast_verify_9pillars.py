import json
from playwright.sync_api import sync_playwright

FILES = [
    r"E:\Tarkan_Analiz\New_Page_Ews\08_Theory\T2SAIM_MASTER_EWS_BIRLESIK_ADLI_PLATFORMU.html",
    r"E:\Tarkan_Analiz\New_Page_Ews\08_Theory\T2SAIM_MASTER_EWS_STANDALONE_PORTABLE.html"
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for fpath in FILES:
        fname = fpath.split("\\")[-1]
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)[:200]))
        page.goto("file:///" + fpath.replace("\\", "/"))
        page.wait_for_timeout(2000)
        
        file_res = {"errors": errors, "pillars": {}}
        for i in range(1, 10):
            pid = f"p{i}"
            btn = page.query_selector(f"[data-pillar='{pid}']")
            if btn:
                btn.click()
                page.wait_for_timeout(500)
                fr = next((f for f in page.frames if f.name == f"frame-{pid}"), None)
                if fr:
                    canvases = fr.evaluate("() => document.querySelectorAll('canvas').length")
                    titles = fr.evaluate("() => document.title || (document.querySelector('h1') ? document.querySelector('h1').innerText : 'No Title')")
                    file_res["pillars"][pid] = {
                        "frame_found": True,
                        "canvases": canvases,
                        "title": titles[:60]
                    }
                else:
                    file_res["pillars"][pid] = {"frame_found": False}
        
        # Test Hub pillar
        btn_hub = page.query_selector("[data-pillar='hub']")
        if btn_hub:
            btn_hub.click()
            page.wait_for_timeout(500)
            rows = page.evaluate("() => document.querySelectorAll('#hub-episodes-body tr').length")
            file_res["pillars"]["hub"] = {"rows": rows}
            
        results[fname] = file_res
        page.close()
    browser.close()

print(json.dumps(results, indent=2, ensure_ascii=False))
