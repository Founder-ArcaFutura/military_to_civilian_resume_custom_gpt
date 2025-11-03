from playwright.sync_api import sync_playwright, TimeoutError

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch")

        mosids = page.locator("#mosidList option").all_inner_texts()
        mosids = [mosid for mosid in mosids if ":" in mosid]

        import json
        try:
            with open("mnet_data.json", "r") as f:
                all_noc_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_noc_data = {}

        for i, mosid in enumerate(mosids):
            if i >= 10:
                break
            if mosid in all_noc_data:
                print(f"Skipping {mosid} (already scraped).")
                continue

            print(f"Scraping data for {mosid}...")
            page.goto("https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch")
            page.wait_for_selector("#mosidList")
            page.select_option("#mosidList", label=mosid)
            page.click("#mosidSearch")
            try:
                page.wait_for_selector("#noc_table", timeout=5000)
                noc_data = []
                for row in page.locator("#noc_table tbody tr").all():
                    row.locator("summary").click()
                    page.wait_for_timeout(100) # wait for the page to update
                    noc_code = row.locator("th").inner_text()
                    civilian_title = row.locator("summary > b").inner_text()
                    task_statements = [p.inner_text() for p in row.locator("div#detailPanelBodyTable > p").all()]
                    noc_data.append({
                        "noc_code": noc_code,
                        "civilian_title": civilian_title,
                        "task_statements": task_statements
                    })
                all_noc_data[mosid] = noc_data
            except TimeoutError:
                print(f"  > No NOC table found for {mosid}. Skipping.")
                all_noc_data[mosid] = []

        import json
        with open("mnet_data.json", "w") as f:
            json.dump(all_noc_data, f, indent=4)

        browser.close()

if __name__ == "__main__":
    main()
