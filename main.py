import asyncio
import dominate
import calendar
import os
from typing import Iterable

from config import *
from dominate.tags import *

type tag = a | th | tr | td | div | p | ul | ol | li

cal = calendar.Calendar()

def html_template(pages: Iterable[tag]):
    with open("style.css") as f:
        the_style = "".join(f.readlines())
    doc = dominate.document(title='Calendarator')
    with doc.head:
        with style():
            dominate.util.raw(the_style)
    for content in pages:
        doc.add(content)
    return doc

def month_overview(year: int, month: int) -> div:
    pg = div(_class = "page")
    with pg:
        with div(_class = "month-container"):
            with table():
                with tr():
                    for d in ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]:
                        th(d)
                for week in cal.monthdays2calendar(year, month):
                    with tr():
                        for (month_day, week_day) in week:
                            td(div("" if month_day == 0 else str(month_day), _class=("monthday-empty" if month_day == 0 else "monthday-content" )))

    return pg

async def main() -> None:
    html_str = html_template(month_overview(2026, i) for i in range(1,13)).render()

    with open("test.html", "w") as f:
        f.writelines(html_str.splitlines(keepends=True))

    await print_pdf("test.html")



async def print_pdf(file: str) -> None:
    print(f"node js/index.js {os.path.abspath(file)}")
    os.system(f"node js/index.js {os.path.abspath(file)}")




    

if __name__ == "__main__":
    asyncio.run(main())
