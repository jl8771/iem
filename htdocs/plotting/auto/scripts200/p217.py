"""SPS Event Plotting Engine, not used from UI."""

# third party
import pytz
from geopandas import read_postgis
from pyiem.network import Table as NetworkTable
from pyiem.plot.geoplot import MapPlot
from pyiem.util import get_autoplot_context, get_dbconn
from pyiem.exceptions import NoDataFound
from pyiem.reference import Z_OVERLAY2
import cartopy.crs as ccrs


TFORMAT = "%b %-d %Y %-I:%M %p %Z"


def get_description():
    """ Return a dict describing how to call this plotter """
    desc = dict()
    desc["cache"] = 3600
    desc["data"] = True
    desc[
        "description"
    ] = """This plot is not meant for interactive use, but a backend for
    SPS plots.
    """
    desc["arguments"] = [
        dict(
            type="text",
            name="pid",
            default="202012300005-KDVN-WWUS83-SPSDVN",
            label="IEM Generated 32-character Product Identifier:",
        ),
        dict(
            type="int",
            default=0,
            name="segnum",
            label="Product Segment Number (starts at 0):",
        ),
    ]
    return desc


def plotter(fdict):
    """ Go """
    pgconn = get_dbconn("postgis")
    ctx = get_autoplot_context(fdict, get_description())
    pid = ctx["pid"][:32]
    segnum = ctx["segnum"]
    nt = NetworkTable("WFO")

    df = read_postgis(
        "SELECT geom, ugcs, wfo, issue, expire, landspout, waterspout, "
        "max_hail_size, max_wind_gust, product, segmentnum "
        f"from sps_{pid[:4]} where product_id = %s",
        pgconn,
        params=(pid,),
        index_col=None,
        geom_col="geom",
    )
    if df.empty:
        raise NoDataFound("SPS Event was not found, sorry.")
    df2 = df[df["segmentnum"] == segnum]
    if df2.empty:
        raise NoDataFound("SPS Event Segment was not found, sorry.")
    row = df2.iloc[0]
    wfo = row["wfo"]
    tz = pytz.timezone(nt.sts[wfo]["tzname"])
    expire = df["expire"].dt.tz_convert(tz)[0]

    if row["geom"].is_empty:
        # Need to go looking for UGCs to compute the bounds
        ugcdf = read_postgis(
            "SELECT simple_geom, ugc from ugcs where wfo = %s and ugc in %s "
            "and end_ts is null",
            pgconn,
            params=(wfo, tuple(row["ugcs"])),
            geom_col="simple_geom",
        )
        bounds = ugcdf["simple_geom"].total_bounds
    else:
        bounds = row["geom"].bounds

    mp = MapPlot(
        title=(
            f"{wfo} Special Weather Statement (SPS) "
            f"till {expire.strftime(TFORMAT)}"
        ),
        sector="custom",
        west=bounds[0] - 0.02,
        south=bounds[1] - 0.3,
        east=bounds[2] + (bounds[2] - bounds[0]) + 0.02,
        north=bounds[3] + 0.3,
        twitter=True,
    )
    # Hackish
    mp.sector = "cwa"
    mp.cwa = wfo

    # Plot text on the page, hehe
    report = (
        row["product"]
        .split("$$")[segnum]
        .replace("\r", "")
        .replace("\003", "")
        .replace("\001", "")
        .replace("$$", "  ")
    )
    pos = report.find("...")
    if pos == -1:
        pos = 0
    report = report[pos : report.find("LAT...LON")]
    mp.fig.text(
        0.5,
        0.85,
        report.strip(),
        bbox=dict(fc="white", ec="k"),
        va="top",
    )

    # Tags
    msg = ""
    for col in "landspout waterspout max_hail_size max_wind_gust".split():
        val = row[col]
        if val is None:
            continue
        msg += f"{col}: {val}\n"
    if msg != "":
        mp.ax.text(
            0.01,
            0.95,
            msg,
            transform=mp.ax.transAxes,
            bbox=dict(color="white"),
        )

    ugcs = {k: 1 for k in row["ugcs"]}
    if not row["geom"].is_empty:
        mp.ax.add_geometries(
            [row["geom"]],
            ccrs.PlateCarree(),
            facecolor="None",
            edgecolor="k",
            linewidth=4,
            zorder=Z_OVERLAY2,
        )
    else:
        mp.fill_ugcs(
            ugcs,
            ec="r",
            fc="None",
            lw=2,
            nocbar=True,
            plotmissing=False,
            zorder=Z_OVERLAY2 - 1,
        )
    radtime = mp.overlay_nexrad(df["issue"][0].to_pydatetime())
    mp.fig.text(
        0.65,
        0.02,
        "RADAR Valid: %s" % (radtime.astimezone(tz).strftime(TFORMAT),),
        ha="center",
    )
    mp.drawcities()
    mp.drawcounties()
    return mp.fig, df.drop("geom", axis=1)


if __name__ == "__main__":
    plotter({"pid": "202103152025-KRIW-WWUS85-SPSRIW", "segnum": 0})