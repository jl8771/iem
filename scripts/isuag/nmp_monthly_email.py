"""Generates an email with the National Mesonet Program contact status

Requires: iem property `nmp_monthly_email_list`

Period of performance is previous month 17th thru this month 16th

Run on the 17th from `RUN_2AM.sh`

"""
from __future__ import print_function
import datetime
import smtplib
from email.mime.text import MIMEText

import psycopg2
from pandas.io.sql import read_sql
from pyiem.util import get_properties


def generate_report(start_date, end_date):
    """Generate the text report"""
    pgconn = psycopg2.connect(database='isuag', host='iemdb', user='nobody')
    days = (end_date - start_date).days + 1
    totalobs = days * 24 * 17
    df = read_sql("""
        SELECT station, count(*) from sm_hourly WHERE valid >= %s
        and valid < %s GROUP by station ORDER by station
    """, pgconn, params=(start_date, end_date + datetime.timedelta(days=1)),
                  index_col='station')
    performance = min([100, df['count'].sum() / float(totalobs) * 100.])
    return """
Iowa Environmental Mesonet Data Delivery Report
===============================================

  Dataset: ISU Soil Moisture Network
  Performance Period: %s thru %s
  Reported Performance: %.1f%%

Additional Details
==================
  Total Required Observations: %.0f (24 hourly obs x 17 stations x %.0f days)
  Observations Delivered: %.0f

Report Generated: %s
.END
""" % (start_date.strftime("%d %b %Y"), end_date.strftime("%d %b %Y"),
       performance, totalobs, days, df['count'].sum(),
       datetime.datetime.now().strftime("%d %B %Y %H:%M %p"))


def main():
    """Go Main Go"""
    emails = get_properties()['nmp_monthly_email_list'].split(",")

    end_date = datetime.date.today().replace(day=16)
    start_date = (end_date - datetime.timedelta(days=40)).replace(day=17)
    report = generate_report(start_date, end_date)

    msg = MIMEText(report)
    msg['Subject'] = "[IEM] 404-41-12 Synoptic Contract Deliverables Report"
    msg['From'] = 'IEM Automation <mesonet@mesonet.agron.iastate.edu>'
    msg['To'] = ', '.join(emails)
    msg.add_header('reply-to', 'akrherz@iastate.edu')

    # Send the email via our own SMTP server.
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    main()