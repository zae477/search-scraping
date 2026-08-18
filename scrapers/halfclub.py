from .base import render_and_extract

URL = "https://www.halfclub.com/home"


def _extract(page):
    for block in page.query_selector_all(".horizontal-area"):
        h2 = block.query_selector("header h2")
        if h2 and "인기 검색어" in h2.inner_text():
            items = block.query_selector_all("ol.rank-list .rank-item")[:10]
            return [
                {"rank": i, "keyword": it.query_selector(".keyword").inner_text()}
                for i, it in enumerate(items, 1)
            ]
    return []


def get_top10():
    return render_and_extract(URL, "ol.rank-list", _extract)
