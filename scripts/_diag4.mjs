import { chromium } from "playwright";
import { spawn } from "node:child_process";

const server = spawn("python3", ["-m", "http.server", "8930"], { cwd: process.cwd() });
await new Promise(r => setTimeout(r, 1500));

const browser = await chromium.launch();
const page = await browser.newPage();
const consoleMsgs = [];
page.on("console", msg => consoleMsgs.push(`[${msg.type()}] ${msg.text()}`));
page.on("pageerror", e => consoleMsgs.push(`[pageerror] ${e.message}`));

await page.goto("http://localhost:8930/index.html");
await page.click("[data-tab=news]");
await page.waitForTimeout(2000);

const result = await page.evaluate(async () => {
  const audios = Array.from(document.querySelectorAll(".news-item audio"));
  const out = [];
  for (const a of audios.slice(0, 6)) {
    const info = { src: a.getAttribute("src") };
    const p = new Promise(resolve => {
      const onErr = () => { info.event = "error"; info.errorCode = a.error?.code; info.errorMsg = a.error?.message; cleanup(); resolve(); };
      const onCanPlay = () => { info.event = "canplay"; info.duration = a.duration; info.readyState = a.readyState; cleanup(); resolve(); };
      function cleanup(){ a.removeEventListener("error", onErr); a.removeEventListener("canplay", onCanPlay); }
      a.addEventListener("error", onErr);
      a.addEventListener("canplay", onCanPlay);
      setTimeout(() => { info.event = "timeout"; info.readyState = a.readyState; info.networkState = a.networkState; cleanup(); resolve(); }, 8000);
    });
    a.load();
    try { await a.play(); } catch (e) { info.playError = String(e); }
    await p;
    out.push(info);
  }
  return out;
});

console.log(JSON.stringify(result, null, 2));
console.log("CONSOLE:", JSON.stringify(consoleMsgs.filter(m => !m.includes("favicon")), null, 2));

await browser.close();
server.kill();
