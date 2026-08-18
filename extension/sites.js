const SITES = [
  {
    name: "하프클럽",
    url: "https://www.halfclub.com/home",
    extract: async function () {
      function findTarget() {
        var blocks = document.querySelectorAll(".horizontal-area");
        for (var i = 0; i < blocks.length; i++) {
          var h2 = blocks[i].querySelector("header h2");
          if (h2 && h2.innerText.indexOf("인기 검색어") !== -1) return blocks[i];
        }
        return null;
      }
      for (var t = 0; t < 30; t++) {
        var target = findTarget();
        if (target) {
          var items = target.querySelectorAll("ol.rank-list .rank-item");
          if (items.length > 0) {
            var out = [];
            for (var j = 0; j < items.length && j < 10; j++) {
              var kw = items[j].querySelector(".keyword");
              if (kw) out.push(kw.innerText.trim());
            }
            return out;
          }
        }
        window.scrollBy(0, 800);
        await new Promise(function (r) { setTimeout(r, 300); });
      }
      return [];
    },
  },
  {
    name: "보리보리",
    url: "https://www.boribori.co.kr/",
    extract: async function () {
      for (var t = 0; t < 30; t++) {
        var sec = document.querySelector("section.search-popular");
        if (sec) {
          var items = sec.querySelectorAll(".popular-item .popular-label");
          if (items.length > 0) {
            var out = [];
            for (var j = 0; j < items.length && j < 10; j++) out.push(items[j].innerText.trim());
            return out;
          }
        }
        window.scrollBy(0, 800);
        await new Promise(function (r) { setTimeout(r, 300); });
      }
      return [];
    },
  },
];
