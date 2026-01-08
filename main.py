import asyncio
import pyppeteer
import dominate
import calendar

from config import *
from dominate.tags import *

def html_template(content):
    with open("style.css") as f:
        the_style = "".join(f.readlines())
    doc = dominate.document(title='Calendarator')
    with doc.head:
        with style():
            dominate.util.raw(the_style)
    doc.add(content)
    return doc

async def main() -> None:
    pg = div(_class = "page")
    hcal = calendar.HTMLCalendar()
   
    #Need to do a table anyway, flexbox seems to be broken
    with pg:
        with div(_class = "year-container"):
           for i in range(1,13):
               with div(_class ="month-container"):
                   dominate.util.raw(hcal.formatmonth(2026,i,False))

    html_str = html_template(pg).render()

    with open("test.html", "w") as f:
        f.writelines(html_str.splitlines(keepends=True))

    await print_pdf("test.html")



async def print_pdf(file: str) -> None:
    browser = await pyppeteer.launch(executablePath="/etc/profiles/per-user/elias/bin/google-chrome-stable")
    page = await browser.newPage()
    await page.goto(f"file://{file}")
    await page.pdf(path="test.pdf", preferCSSPageSize=True)



    

if __name__ == "__main__":
    asyncio.run(main())
