from datetime import datetime
from pytz import timezone

from core.settings import TIME_ZONE


def local_datetime() -> datetime:

    dt_tdy: datetime = datetime.today()
    lc_dt: datetime = timezone(TIME_ZONE).localize(dt_tdy)

    return lc_dt


def convert_datetime(dt: datetime) -> datetime:

    lc_dt: datetime = timezone(TIME_ZONE).localize(dt)

    return lc_dt
