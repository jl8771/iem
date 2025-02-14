"""
Provide nws text in JSON format
"""
# stdlib
import datetime
import json

# extras
import pytz
from paste.request import parse_formvars
from pyiem.util import get_dbconn, html_escape


def application(environ, start_response):
    """Answer request."""
    headers = [("Content-type", "application/json")]
    if environ.get("REQUEST_METHOD") != "GET":
        start_response("405 Method Not Allowed", headers)
        return ['{"error": "Only HTTP GET Supported"}'.encode("utf8")]

    fields = parse_formvars(environ)
    pgconn = get_dbconn("afos")
    acursor = pgconn.cursor()
    pid = fields.get("product_id", "201302241937-KSLC-NOUS45-PNSSLC")[:35]
    cb = fields.get("callback")
    tokens = pid.split("-")
    utc = datetime.datetime.strptime(tokens[0], "%Y%m%d%H%M")
    utc = utc.replace(tzinfo=pytz.UTC)
    root = {"products": []}

    acursor.execute(
        "SELECT data from products where pil = %s and entered = %s",
        (tokens[3], utc),
    )
    for row in acursor:
        root["products"].append({"data": row[0]})
    pgconn.close()

    if cb is None:
        data = json.dumps(root)
    else:
        data = f"{html_escape(cb)}({json.dumps(root)})"

    start_response("200 OK", headers)
    return [data.encode("ascii")]
