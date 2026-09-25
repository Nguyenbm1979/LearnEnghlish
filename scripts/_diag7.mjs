import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("https://nguyenbm1979.github.io/LearnEnghlish/", { waitUntil: "networkidle" });
await page.click("[data-tab=news]");
await page.waitForTimeout(1500);

const result = await page.evaluate(async () => {
  const audios = Array.from(document.querySelectorAll(".news-item audio"));
  const out = [];
  for (const a of audios) {
    const src = a.getAttribute("src") || "";
    if (!src.startsWith("data/audio/")) continue; // only test mirrored local files
    const info = { src };
    const p = new Promise(resolve => {
      const onErr = () => { info.event = "error"; cleanup(); resolve(); };
      const onCanPlay = () => { info.event = "canplay"; info.duration = a.duration; cleanup(); resolve(); };
      function cleanup(){ a.removeEventListener("error", onErr); a.removeEventListener("canplay", onCanPlay); }
      a.addEventListener("error", onErr);
      a.addEventListener("canplay", onCanPlay);
      setTimeout(() => { info.event = "timeout"; cleanup(); resolve(); }, 10000);
    });
    a.load();
    try { await a.play(); } catch (e) { info.playError = String(e); }
    await p;
    out.push(info);
  }
  const iframeCount = document.querySelectorAll(".news-item iframe").length;
  return { audios: out, iframeCount };
});

console.log(JSON.stringify(result, null, 2));
await browser.close();
