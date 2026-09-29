import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const jobs = JSON.parse(fs.readFileSync(path.join(here, 'jobs.json')));
const b = await chromium.launch();
for (const [name, w, h, transparent] of jobs) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(here, 'html', name.replace(/\//g, '__') + '.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(120);
  const out = path.join(here, 'out', name + '.png');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await p.screenshot({ path: out, omitBackground: !!transparent });
  await p.close();
}
await b.close();
console.log('rendered', jobs.length);
