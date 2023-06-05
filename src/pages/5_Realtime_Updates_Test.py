import streamlit as st
import time
import requests
import pandas as pd
import plotly.express as px
import numpy as np

from streamlit.runtime.scriptrunner import add_script_run_ctx

st.set_page_config(layout="wide")

st.header("Realtime Updating Dashboard")

"""
This is an example page on displaying real time data.
It pulls Bitcoin prices from an api, then displays the data on multiple charts:
- A base chart, which illustrates how prices have fluctuated
- A mean chart, which illustrates the mean of prices over time
- A min max chart, which illustrates the min and max price over time

Multithreading is possible. However, for simplicity's sake, multithreading has not been implemented for this example.
Note: If you are to multithread, run add_script_run_ctx to your thread from streamlit.runtime.scriptrunner.
"""

API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
REQUEST_SLEEP_TIME = 0.5

def request_data():
    response = requests.get(API_URL)
    data = response.json()
    return data["time"]["updatedISO"], float(data["bpi"]["USD"]["rate_float"]) * ((np.random.uniform() / 2 + 0.5) * (np.random.uniform() + 1))

prices = []
dates = []
means = []
min_maxes = []

base_chart = None
means_chart = None
min_max_chart = None

def update_charts():
    global base_chart, means_chart, min_max_chart
    indices = list(range(1, len(prices) + 1))

    base_df = pd.DataFrame(dict(date=dates, price=prices, index=indices))
    base_chart = px.line(base_df, x="index", y="price", title="Bitcoin Price Over Time", markers=True)

    means_df = pd.DataFrame(dict(index=indices, mean=means))
    means_chart = px.line(means_df, x="index", y="mean", title="Mean Bitcoin Price Over Time", markers=True)

    mins, maxes = zip(*min_maxes)
    mins = list(mins)
    maxes = list(maxes)
    all_min_maxes = mins + maxes
    min_max_df = pd.DataFrame(dict(measurement=all_min_maxes, index=indices + indices, type=["Min"] * len(mins) + ["Max"] * len(maxes)))
    min_max_chart = px.line(min_max_df, x="index", y="measurement", color="type", title="Min and Maxes of Bitcoin Price Over Time", markers=True)

def update_dashboard():
    while True:
        date, price = request_data()
        time.sleep(REQUEST_SLEEP_TIME)

        dates.append(date)
        prices.append(price)
        means.append(np.mean(prices))
        min_maxes.append((min(prices), max(prices)))
        update_charts()
        with st.container():
            if base_chart:
                st.plotly_chart(base_chart, use_container_width=True)
            if means_chart:
                st.plotly_chart(means_chart, use_container_width=True)
            if min_max_chart:
                st.plotly_chart(min_max_chart, use_container_width=True)

with st.empty():
    update_dashboard()