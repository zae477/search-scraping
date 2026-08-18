import sys
from datetime import datetime
from scrapers import halfclub

SITES = {"halfclub": halfclub.get_top10}


def run(site):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{site}] {ts}")
    for item in SITES[site]():
        print(f"{item['rank']}. {item['keyword']}")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "halfclub")
