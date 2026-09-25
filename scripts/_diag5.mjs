import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();
const consoleMsgs = [];
page.on("console", msg => consoleMsgs.push(`[${msg.type()}] ${msg.text()}`));
page.on("pageerror", e => consoleMsgs.push(`[pageerror] ${e.message}`));

await page.goto("https://nguyenbm1979.github.io/LearnEnghlish/", { waitUntil: "networkidle" });
await page.waitForTimeout(1500);

const gateVisible = await page.locator("#authGate").isVisible();
console.log("Auth gate visible:", gateVisible);

let popupError = null;
page.on("popup", async popup => {
  await popup.waitForTimeout(1500);
  console.log("Popup URL:", popup.url());
});

try {
  await page.click("#googleSignInBtn", { timeout: 5000 });
} catch (e) {
  popupError = String(e);
}
await page.waitForTimeout(3000);

console.log("Click error (if any):", popupError);
console.log("CONSOLE:", JSON.stringify(consoleMsgs, null, 2));

await browser.close();
