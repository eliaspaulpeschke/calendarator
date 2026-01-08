import puppeteer from 'puppeteer-core';

const browser = await puppeteer.launch({executablePath: "/etc/profiles/per-user/elias/bin/google-chrome-stable"});
const page = await browser.newPage();
await page.goto(`file://${process.argv[2]}`, {waitUntil: 'networkidle2'});

await page.pdf({
      path: 'test.pdf'
    , preferCSSPageSize: true});

await browser.close();
