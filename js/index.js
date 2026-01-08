import puppeteer from 'puppeteer-core';

const browser = await puppeteer.launch({executablePath: "/etc/profiles/per-user/elias/bin/google-chrome-stable"});
const page = await browser.newPage();
await page.goto('file:///home/elias/repos/calendarator/test.html', {waitUntil: 'networkidle2'});

await page.pdf({path: 'test.pdf'});

await browser.close();
