#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const [key, ...rest] = arg.replace(/^--/, '').split('=');
    return [key, rest.join('=') || true];
  })
);

const url = args.url || process.env.FRONTEND_URL || 'http://localhost:3000';
const outDir = args.out || 'frontend-artifacts/screenshots';
const rtl = args.rtl === true || args.rtl === 'true' || process.env.FRONTEND_RTL === 'true';

fs.mkdirSync(outDir, { recursive: true });

async function main() {
  let chromium;
  try {
    ({ chromium } = await import('playwright'));
  } catch {
    console.error('Playwright is not installed. Install with: npm i -D playwright && npx playwright install chromium');
    process.exit(2);
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  const shots = [
    { name: 'desktop.png', width: 1440, height: 1100 },
    { name: 'tablet.png', width: 1024, height: 1100 },
    { name: 'mobile.png', width: 390, height: 1200 }
  ];

  for (const shot of shots) {
    await page.setViewportSize({ width: shot.width, height: shot.height });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(outDir, shot.name), fullPage: true });
  }

  if (rtl) {
    for (const shot of [
      { name: 'rtl-desktop.png', width: 1440, height: 1100 },
      { name: 'rtl-mobile.png', width: 390, height: 1200 }
    ]) {
      await page.setViewportSize({ width: shot.width, height: shot.height });
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.evaluate(() => {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.setAttribute('lang', 'he');
      });
      await page.screenshot({ path: path.join(outDir, shot.name), fullPage: true });
    }
  }

  await browser.close();
  console.log(`Screenshots written to ${outDir}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
