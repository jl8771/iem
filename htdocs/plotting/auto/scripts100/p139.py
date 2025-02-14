"""Top 10 largest, smallest"""
import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore

import pandas as pd
from matplotlib.font_manager import FontProperties
from pyiem.util import get_autoplot_context, get_sqlalchemy_conn
from pyiem.plot import figure
from pyiem.exceptions import NoDataFound
from sqlalchemy import text

MDICT = {
    "all": "No Month/Time Limit",
    "spring": "Spring (MAM)",
    "fall": "Fall (SON)",
    "winter": "Winter (DJF)",
    "summer": "Summer (JJA)",
    "jan": "January",
    "feb": "February",
    "mar": "March",
    "apr": "April",
    "may": "May",
    "jun": "June",
    "jul": "July",
    "aug": "August",
    "sep": "September",
    "oct": "October",
    "nov": "November",
    "dec": "December",
}

PDICT = {"largest": "Largest", "smallest": "Smallest"}


def get_description():
    """Return a dict describing how to call this plotter"""
    desc = {}
    desc["data"] = True
    desc["cache"] = 86400
    desc[
        "description"
    ] = """This table presents the 10 largest or smallest differences
    between the lowest and highest air temperature for a local calendar
    day.  Some stations have auxillary products that provide 'daily' values
    over a date defined always in standard time.  This plot also presents
    sprites of the temperature time series starting at 12 hours before the
    denoted date and ending at 12 hours after the date.  The sprite often
    quickly points out bad data points, sigh, but also easily shows if the
    temperature change was an increase during the day or decrease.

    <p><a href="/plotting/auto/?q=169">Autoplot 169</a> is similar to this
    plot, but computes the change over arbitrary time windows.</p>
    """
    desc["arguments"] = [
        dict(
            type="zstation",
            name="zstation",
            default="AMW",
            label="Select Station:",
            network="IA_ASOS",
        ),
        dict(
            type="select",
            name="v",
            default="largest",
            label="Show largest or smallest differences?",
            options=PDICT,
        ),
        dict(
            type="select",
            name="month",
            default="all",
            label="Month Limiter",
            options=MDICT,
        ),
    ]
    return desc


def plot_date(ax, i, date, station, tz) -> bool:
    """plot date."""
    # request 36 hours
    sts = datetime.datetime(date.year, date.month, date.day, tzinfo=tz)
    sts = sts - datetime.timedelta(hours=12)
    ets = sts + datetime.timedelta(hours=48)
    with get_sqlalchemy_conn("asos") as conn:
        df = pd.read_sql(
            "SELECT valid at time zone 'UTC' as valid, tmpf from alldata "
            "where station = %s and valid >= %s and valid <= %s and "
            "tmpf is not null ORDER by valid ASC",
            conn,
            params=(station, sts, ets),
            index_col=None,
        )
    if df.empty:
        return False
    df["valid"] = df["valid"].dt.tz_localize(ZoneInfo("UTC"))
    # Ensure that we have at least one ob within six hours to start and end
    h6 = datetime.timedelta(hours=6)
    dv = df["valid"]
    if df[(dv >= sts) & (dv < (sts + h6))].empty:
        return False
    h18 = datetime.timedelta(hours=18)
    if df[(dv >= (sts + h18)) & (dv < (sts + h6 + h18))].empty:
        return False
    df["norm"] = (df["tmpf"] - df["tmpf"].min()) / (
        df["tmpf"].max() - df["tmpf"].min()
    )
    df["xnorm"] = [
        x.total_seconds() for x in (df["valid"].dt.to_pydatetime() - sts)
    ]

    lp = ax.plot(df["xnorm"], df["norm"] + i)
    ax.text(
        df["xnorm"].values[-1],
        df["norm"].values[-1] + i,
        date.strftime("%-d %b %Y"),
        va="bottom" if df["norm"].values[-1] < 0.5 else "top",
        color=lp[0].get_color(),
    )
    return True


def plotter(fdict):
    """Go"""
    font0 = FontProperties()
    font0.set_family("monospace")
    font0.set_size(16)
    ctx = get_autoplot_context(fdict, get_description())
    station = ctx["zstation"]
    month = ctx["month"]

    if month == "all":
        months = range(1, 13)
    elif month == "fall":
        months = [9, 10, 11]
    elif month == "winter":
        months = [12, 1, 2]
    elif month == "spring":
        months = [3, 4, 5]
    elif month == "summer":
        months = [6, 7, 8]
    else:
        ts = datetime.datetime.strptime(f"2000-{month}-01", "%Y-%b-%d")
        # make sure it is length two for the trick below in SQL
        months = [ts.month, 999]

    order = "DESC" if ctx["v"] == "largest" else "ASC"
    with get_sqlalchemy_conn("iem") as conn:
        # Over-sample as we may get some DQ's due to lack of data
        df = pd.read_sql(
            text(
                f"""
            SELECT day as date, max_tmpf as max, min_tmpf as min,
            max_tmpf::int - min_tmpf::int as difference
            from summary s JOIN stations t on (s.iemid = t.iemid)
            where t.id = :station and t.network = :network
            and extract(month from day) in :months
            and max_tmpf is not null and min_tmpf is not null
            ORDER by difference {order}, date DESC LIMIT 50
        """
            ),
            conn,
            params={
                "station": station,
                "network": ctx["network"],
                "months": tuple(months),
            },
            parse_dates=("date",),
            index_col=None,
        )
    if df.empty:
        raise NoDataFound("No Data Found,")
    df["rank"] = df["difference"].rank(
        ascending=(ctx["v"] == "smallest"), method="min"
    )
    ab = ctx["_nt"].sts[station]["archive_begin"]
    if ab is None:
        raise NoDataFound("Unknown station metadata.")
    tz = ZoneInfo(ctx["_nt"].sts[station]["tzname"])
    title = (
        f"{ctx['_sname']} ({ab.year}-{datetime.date.today().year})\n"
        f"Top 10 {PDICT[ctx['v']]} Local Calendar Day "
        f"[{month.capitalize()}] Temperature Differences"
    )
    fig = figure(title=title, apctx=ctx)
    fig.text(
        0.1, 0.81, " #  Date         Diff   Low High", fontproperties=font0
    )
    y = 0.74
    ax = fig.add_axes([0.5, 0.1, 0.3, 0.69])
    i = 10
    hits = 0
    rank = 0
    rankval = -1
    for _, row in df.iterrows():
        if hits >= 10:
            break
        if not plot_date(ax, i, row["date"], station, tz):
            continue
        if row["difference"] > rankval:
            rank += 1
            rankval = row["difference"]
        hits += 1
        fig.text(
            0.1,
            y,
            (
                f"{rank:2.0f}  {row['date']:%d %b %Y}   "
                f"{row['difference']:3.0f}   "
                f"{row['min']:3.0f}  {row['max']:3.0f}"
            ),
            fontproperties=font0,
        )
        y -= 0.07
        i -= 1
    ax.set_title("Hourly Temps On Date & +/-12 Hrs")
    ax.set_ylim(1, 11)
    ax.axvline(12 * 3600, color="tan")
    ax.axvline(36 * 3600, color="tan")
    ax.axis("off")
    return fig, df


if __name__ == "__main__":
    plotter(dict(zstation="MCW", network="IA_ASOS"))
