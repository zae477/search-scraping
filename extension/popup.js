function waitForLoad(tabId) {
  return new Promise(function (resolve) {
    function listener(id, info) {
      if (id === tabId && info.status === "complete") {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    }
    chrome.tabs.onUpdated.addListener(listener);
  });
}

document.getElementById("run").addEventListener("click", async function () {
  var statusEl = document.getElementById("status");
  var outEl = document.getElementById("out");
  outEl.value = "";
  var lines = [];

  for (var i = 0; i < SITES.length; i++) {
    var site = SITES[i];
    statusEl.textContent = site.name + " 수집 중... (" + (i + 1) + "/" + SITES.length + ")";
    try {
      var tab = await chrome.tabs.create({ url: site.url, active: false });
      await waitForLoad(tab.id);
      var res = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: site.extract });
      var keywords = (res[0] && res[0].result) || [];
      await chrome.tabs.remove(tab.id);
      lines.push("[" + site.name + "]");
      if (keywords.length === 0) lines.push("(수집 실패)");
      else lines.push.apply(lines, keywords);
      lines.push("");
    } catch (e) {
      lines.push("[" + site.name + "] 오류: " + e.message);
      lines.push("");
    }
  }

  var text = lines.join("\n").trim();
  outEl.value = text;
  await navigator.clipboard.writeText(text);
  statusEl.textContent = "완료! 클립보드에 복사됨.";
});
