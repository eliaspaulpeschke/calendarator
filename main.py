import asyncio
import dominate
import calendar
import icalendar
import recurring_ical_events
import datetime
from datetime import timedelta
import os,sys
import pathlib
from typing import Iterable

from config import *
from dominate.tags import *



cal = calendar.Calendar()

def get_icals() -> list[icalendar.Calendar]:
    try: 
        import importlib.util
        spec = importlib.util.spec_from_file_location(name = "env", location= "./.env.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["env"] = module
        spec.loader.exec_module(module)
        calendar_urls = module.calendar_urls
    except ImportError:
        print("Could not find .env.py")
        return []
    calendars = []
    for (idx, url) in enumerate(calendar_urls):
        cname = f"cal{idx}.ics"
        os.system(f"wget -O {cname} {url}")
        cpath = pathlib.Path(cname)
        cal = icalendar.Calendar.from_ical(cpath.read_bytes())
        calendars.append(cal)
    return calendars

icals = get_icals()

def get_month(month: int) -> str:
    months = ["Januar", "Februar" , "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return months[month-1]

days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

def html_template(pages: Iterable[dom_tag]):
    with open("style.css") as f:
        the_style = "".join(f.readlines())
    doc = dominate.document(title='Calendarator')
    with doc.head:
        link(rel='stylesheet', href='style.css')
#        with style():
 #           dominate.util.raw(the_style)
    for content in pages:
        doc.add(content)
    return doc

def get_weeknr(year: int, month: int, day:int) -> int:
    return datetime.date(year, month, day).isocalendar().week

def get_events_for_date(date: datetime.date) -> list[icalendar.Component]:
    events = []
    for cal in icals:
        events.extend(recurring_ical_events.of(cal).between(date, date + timedelta(days=1)))
    return events

def month_overview(year: int, month: int) -> div:
    pg = div(_class = "page")
    with pg.add(div(_class = "month-container")).add(table()):
        tr(th(),th(get_month(month), _class = "month-name"))
        with tr():
            th()
            for d in days:
                th(d, _class = "month-dayname")
        for week in cal.monthdays2calendar(year, month):
            firstday = [x for x in week if x[0] != 0][0][0]
            with tr():
                td(div(str(get_weeknr(year, month, firstday)), _class="weeknr-content"), _class="month-weeknr")
                for (month_day, week_day) in week:
                    events = []
                    if month_day != 0:
                        day_date = datetime.date(year,month,month_day)
                        events = get_events_for_date(day_date) 
                    if len(events) > 0:
                        cnt = [span(str(month_day))] + [span(str(x.decoded("summary"), 'utf-8'), _class="month-event") for x in events]

                    else:
                        cnt = [""] if month_day == 0 else [str(month_day)]
                    cls = "monthday-empty" if month_day == 0 else "monthday-content"
                    td(div((x for x in cnt), _class=cls))

    return pg

async def main() -> None:
    html_str = html_template(month_overview(2026, i) for i in range(1,13)).render()

    with open("out.html", "w") as f:
        f.writelines(html_str.splitlines(keepends=True))

    await print_pdf("out.html")

async def print_pdf(file: str) -> None:
    print(f"node js/index.js {os.path.abspath(file)}")
    os.system(f"node js/index.js {os.path.abspath(file)}")




    

if __name__ == "__main__":
    asyncio.run(main())
