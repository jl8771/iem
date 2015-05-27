"""
Examples of widget types

dict(type='date', name='date2', default='2012/03/15', label='Bogus2:',
     min="1893/01/01"), # Comes back to python as yyyy-mm-dd

"""
# Association of plots
data = {'plots': [
    {'label': 'Daily', 'options': [
        {'id': "11", 'label': "ASOS/AWOS Daily Maximum Dew Point for a Year"},
        {'id': "32", 'label': "Daily Temperature Departures for One Year",
         'mw': True},
        {'id': "21",
         'label': "Change in NCDC 81 Daily Climatology over X Days"},
        {'id': "66", 'mw': True,
         "label": "Consecutative Days with High Temperature Above Threshold"},
        {'id': "31", 'mw': True,
         'label': "Extreme Jumps or Dips in High Temperature over X days"},
        {'id': "7", 'mw': True,
         'label': "Growing Degree Day Periods for One Year by Planting Date"},
        {'id': "61",
         'label': ("High/Low Temp streaks above/below average "
                   "by NWS CLI Sites")},
        {'id': "19", 'mw': True,
         'label': "Histogram of Daily High/Low Temperatures"},
        {'id': "35", 'label': "Histogram of X Hour Temperature Changes"},
        {'id': "60", 'label': ("Hourly Temperature Frequencies "
                               "Above/Below Threshold")},
        {'id': "34", 'mw': True,
         'label': "Maximum Stretch of Days with High Below Threshold"},
        {'id': "26",
         'label': "Min Daily Low after 1 July / Max Daily High before 1 July"},
        {'id': "5", 'mw': True,
         'label': "Minimum Daily Temperature Range"},
        {'id': "22", 'mw': True,
         'label': ("Percentage of Years within Temperature Range "
                   "from Averages")},
        {'id': "62", 'mw': True,
         'label': "Snow Depth"},
        {'id': "38", 'mw': True,
         'label': "Solar Radiation Estimates from NARR"},
        {'id': "25", 'mw': True,
         'label': "Spread of Daily High and Low Temperatures"},
        {'id': "4", 'mw': True,
         'label': "State Areal Coverage of Precip Intensity over X Days"},
        {'id': "28", 'mw': True,
         'label': "Trailing Number of Days Precipitation Total Rank"},
    ]},
    {'label': 'Monthly', 'options': [
        {'id': "71", 'label': "Average Wind Speed and Direction for Month"},
        {'id': "55", 'label': "Daily Climatology Comparison"},
        {'id': "15", 'mw': True,
         'label': "Daily Temperature Change Frequencies by Month"},
        {'id': '65', 'mw': True,
         'label': 'Day of the Month with the coldest temperature'},
        {'id': "29",
         'label': "Frequency of Hourly Temperature within Range by Month"},
        {'id': "1", 'mw': True,
         'label': "July-August Days Above Temp v. May-June Precip"},
        {'id': "9", 'mw': True, 'label': ("Growing Degree Day Climatology "
                                          "and Daily Values for one Year")},
        {'id': "2", 'mw': True,
         'label': "Month Precipitation v Month Growing Degree Day Departures"},
        {'id': "3", 'mw': True,
         'label': "Monthly Temperature / Precipitation Statistics by Year"},
        {'id': "6", 'mw': True,
         'label': "Monthly Temperature/Precipitation Distributions"},
        {'id': "42",
         'label': "Hourly Temperature Streaks Above/Below Threshold"},
        {'id': "24", 'mw': True,
         'label': "Monthly Precipitation Climate District Ranks"},
        {'id': "8", 'mw': True,
         'label': "Monthly Precipitation Reliability"},
        {'id': "23", 'mw': True,
         'label': "Monthly Station Departures + El Nino 3.4 Index"},
        {'id': "36", 'mw': True,
         'label': "Month warmer than other Month for Year"},
        {'id': "58", 'mw': True,
         'label': ("One Day's Precipitation Greater than X percentage "
                   "of Monthly Total")},
        {'id': "41", 'mw': True,
         'label': ("Quantile / Quantile Plot of Daily Temperatures "
                   "for Two Months")},
        {'id': "20", 'label': "Hours of Precipitation by Month"},
        {'id': "47", 'mw': True,
         'label': "Snowfall vs Precipitation Total for a Month"},
        {'id': "39", 'mw': True,
         'label': "Scenarios for this month besting some previous month"},
        {'id': "57", 'mw': True,
         'label': "Warmest Months for Average Temperature"},
    ]},
    {'label': 'Yearly', 'options': [
        {'id': "12", 'mw': True,
         'label': "Days per year and first/latest date above given threshold"},
        {'id': "13", 'mw': True,
         'label': "End Date of Summer (warmest 91 day period) per Year"},
        {'id': "27", 'mw': True,
         'label': "First Fall Freeze then Killing Frost"},
        {'id': "53", 'label': ("Hourly Frequency of Temperature within "
                               "Certain Ranges")},
        {'id': "10", 'mw': True,
         'label': ("Last Spring and First Fall Date "
                   "above/below given threshold")},
        {'id': '64', 'mw': True,
         'label': 'Last Snowfall of Each Winter Season'},
        {'id': "33", 'mw': True, 'label': "Maximum Low Temperature Drop"},
        {'id': "46", 'label': "Minimum Wind Chill Temperature"},
        {'id': "30", 'mw': True, 'label': "Monthly Temperature Range"},
        {'id': "44", 'label': "NWS Office Accumulated SVR+TOR Warnings"},
        {'id': "69", 'mw': True,
         'label': "Percentage of Year to Date Days Above Average"},
        {'id': "63", 'mw': True,
         'label': "Records Set by Year (Max High / Min Low)"},
        {'id': "14", 'mw': True,
         'label': "Yearly Precipitation Contributions by Daily Totals"},
    ]},
    {'label': 'METAR ASOS Special Plots', 'options': [
        {'id': "40",
         'label': "Cloud Amount and Level Timeseries for One Month"},
        {'id': "59",
         'label': "Daily u and v Wind Component Climatologies"},
        {'id': "54",
         'label': ("Difference between morning low temperatures "
                   "between two sites")},
        {'id': "18", 'label': "Long term temperature time series"},
        {'id': "45", 'label': "Monthly Frequency of Overcast Conditions"},
        {'id': "67",
         'label': "Monthly Frequency of Wind Speeds by Air Temperature"},
        {'id': "37",
         'label': "MOS Forecasted Temperature Ranges + Observations"},
        {'id': "16", 'label': "Wind Rose when specified criterion is meet"},
    ]},
    {'label': 'NWS Warning Plots', 'options': [
        {'id': "73",
         'label': "Number of Watch/Warning/Advisories Issued per Year"},
        {'id': "72",
         'label': "Frequency of Issuance time for Watch/Warning/Advisories"},
        {'id': "52",
         'label': "Gaant Chart of WFO Issued Watch/Warning/Advisories"},
        {'id': "44", 'label': "NWS Office Accumulated SVR+TOR Warnings"},
        {'id': "68",
         'label': "Number of Distinct Phenomena/Significance VTEC per Year"},
        {'id': "70",
         'label': "Period between First and Last VTEC Product Each Year"},
        {'id': "48", 'label': "Time of Day Frequency for Given Warning / UGC"},
        {'id': "56", 'label': "Weekly Frequency of a Watch/Warning/Advisory"},
    ]},
    {'label': 'Sustainable Corn Project Plots', 'options': [
        {'id': "49", 'mw': True,
         'label': "Two Day Precipitation Total Frequencies"},
        {'id': "50", 'mw': True,
         'label': "Frequency of Measurable Daily Precipitation"},
        {'id': "51", 'mw': True,
         'label': "Frequency of No Daily Precipitation over 7 Days"},
    ]},
]}
