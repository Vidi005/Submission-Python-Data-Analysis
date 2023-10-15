from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")

def create_avg_aqi_df(df, period):
    avg_aqi_df = df.resample(rule=period, on="date_time").agg({
        "pm2_5": "mean",
        "pm10": "mean"
    })
    avg_aqi_df = avg_aqi_df.reset_index()
    avg_aqi_df.rename(columns={
        "pm2_5": "avg_pm2_5",
        "pm10": "avg_pm10"
    }, inplace=True)
    return avg_aqi_df

def create_aqi_stats_df(df):
    aqi_stats_df = df.groupby(by="date_time").agg({
        "pm2_5": ["min", "max", "mean"],
        "pm10": ["min", "max", "mean"]
    })
    aqi_stats_df = aqi_stats_df.reset_index()
    aqi_stats_df.rename(columns={
        "pm2_5": "pm2_5_stats",
        "pm10": "pm10_stats"
    }, inplace=True)
    return aqi_stats_df

def create_monthly_per_year_avg_aqi_df(df):
    monthly_avg_aqi_df = df.resample(rule='M', on='date_time').agg({
        "pm2_5": "mean",
        "pm10": "mean"
    })
    monthly_avg_aqi_df.index = monthly_avg_aqi_df.index.strftime('%b')
    monthly_avg_aqi_df = monthly_avg_aqi_df.reset_index()
    monthly_avg_aqi_df.rename(columns={
        "date_time": "month",
        "pm2_5": "avg_pm2_5",
        "pm10": "avg_pm10"
    }, inplace=True)
    return monthly_avg_aqi_df

def create_avg_aqi_by_station_df(df):
    avg_aqi_by_station_df = df.groupby(by="station").agg({
        "pm2_5": "mean",
        "pm10": "mean"
    }).rename(columns={
        "pm2_5": "avg_pm2_5",
        "pm10": "avg_pm10"
    }).reset_index()
    return avg_aqi_by_station_df

def create_daily_avg_aqi_df(df):
    daily_avg_aqi_df = df.resample(rule='D', on='date_time').agg({
        "pm2_5": "mean",
        "pm10": "mean"
    })
    daily_avg_aqi_df.index = daily_avg_aqi_df.index.strftime('%A')
    daily_avg_aqi_df = daily_avg_aqi_df.reset_index()
    daily_avg_aqi_df.rename(columns={
        "date_time": "day",
        "pm2_5": "avg_pm2_5",
        "pm10": "avg_pm10"
    }, inplace=True)
    day_order = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6
    }
    daily_avg_aqi_df['day_num'] = daily_avg_aqi_df['day'].map(day_order)
    daily_avg_aqi_df = daily_avg_aqi_df.groupby(by=['day']).mean()
    daily_avg_aqi_df = daily_avg_aqi_df.sort_values(
        by=['day_num']).drop(columns=['day_num']).reset_index()
    return daily_avg_aqi_df

def create_hourly_avg_aqi_df(df):
    hourly_avg_aqi_df = df.groupby(by="hour").agg({
        "pm2_5": "mean",
        "pm10": "mean"
    }).reset_index()
    hourly_avg_aqi_df["hour"] = hourly_avg_aqi_df["hour"].astype(str) + ":00"
    return hourly_avg_aqi_df

def create_aqi_by_pm2_5_df(df):
    aqi_by_pm2_5_df = df.groupby(by="aqi_by_pm2_5").idx.nunique().reset_index()
    aqi_by_pm2_5_df.rename(columns={
        "idx": "aqi_by_pm2_5_count"
    }, inplace=True)
    categories = ["Good", "Moderate", "Unhealthy for Sensitive Groups",
                  "Unhealthy", "Very Unhealthy", "Hazardous"]
    aqi_by_pm2_5_df["aqi_by_pm2_5"] = pd.Categorical(
        aqi_by_pm2_5_df["aqi_by_pm2_5"], categories=categories, ordered=True)
    aqi_by_pm2_5_df.sort_values(by="aqi_by_pm2_5").reset_index(drop=True)
    return aqi_by_pm2_5_df

def create_aqi_by_pm10_df(df):
    aqi_by_pm10_df = df.groupby(by="aqi_by_pm10").idx.nunique().reset_index()
    aqi_by_pm10_df.rename(columns={
        "idx": "aqi_by_pm10_count"
    }, inplace=True)
    categories = ["Good", "Moderate", "Unhealthy",
                  "Very Unhealthy", "Hazardous"]
    aqi_by_pm10_df["aqi_by_pm10"] = pd.Categorical(
        aqi_by_pm10_df["aqi_by_pm10"], categories=categories, ordered=True)
    aqi_by_pm10_df.sort_values(by="aqi_by_pm10")
    return aqi_by_pm10_df

def create_agg_df(df, period):
    agg_df = df.resample(rule=period, on="date_time").agg({
        "pm2_5": "mean",
        "pm10": "mean",
        "so2": "mean",
        "no2": "mean",
        "co": "mean",
    })
    if period == "M" and len(annual_periods) < 2:
        agg_df.index = agg_df.index.strftime('%b')
    else:
        agg_df.index = agg_df.index.strftime('%Y-%m-%d')
    agg_df = agg_df.reset_index()
    agg_df.rename(columns={
        "pm2_5": "avg_pm2_5",
        "pm10": "avg_pm10",
        "so2": "avg_so2",
        "no2": "avg_no2",
        "co": "avg_co"
    }, inplace=True)
    return agg_df

def create_agg_stats_df(df):
    agg_stats_df = df.groupby(by="date_time").agg({
        "so2": "mean",
        "no2": "mean",
        "co": "mean"
    })
    agg_stats_df = agg_stats_df.reset_index()
    agg_stats_df.rename(columns={
        "so2": "so2_stats",
        "no2": "no2_stats",
        "co": "co_stats"
    }, inplace=True)
    return agg_stats_df

def set_checkbox_var(position):
    return str(all_df.groupby(
        by="annually_period")["annually_period"].nunique().index[position])

def set_district_var():
    all_district = ["Semua Distrik"]
    district_selection = all_df.groupby(
        by="station")["station"].nunique().sort_values().index.tolist()
    return all_district + district_selection

all_df = pd.read_csv("dashboard/main_data.csv")
all_df["date_time"] = pd.to_datetime(all_df["date_time"])

min_date = all_df["date_time"].min()
max_date = all_df["date_time"].max()
annual_periods = []
annual_period_count = all_df["annually_period"].nunique()
district = "Semua Distrik"
districts_count = all_df["station"].nunique()
all_district_df = all_df
start_date = min_date
end_date = max_date

with st.sidebar:
    st.image("dashboard/aqi-logo.png")
    st.caption("Filter Data Berdasarkan:")
    period = st.selectbox(
        label="Pilih Periode",
        options=["Seluruh Periode (2013-2017)",
                 "Rentang Waktu Tertentu", "Tahunan"]
    )
    if period == "Seluruh Periode (2013-2017)":
        annual_periods = ["", ""]
        main_df = all_df[(all_df["date_time"] >= min_date) &
                         (all_df["date_time"] <= max_date)]
        all_district_df = main_df
    elif period == "Rentang Waktu Tertentu":
        annual_periods = ["", ""]
        selected_date_range = st.date_input(
            label="Pilih rentang waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
            start_date, end_date = list(selected_date_range)
            main_df = all_df[(all_df["date_time"] >= str(start_date)) & (
                all_df["date_time"] <= str(end_date))]
        else:
            st.warning("Silahkan pilih rentang waktu yang valid.")
            main_df = all_df[(all_df["date_time"] >= min_date)
                             & (all_df["date_time"] <= max_date)]
        all_district_df = main_df
    else:
        annual_periods = []
        for i in range(annual_period_count):
            period = st.checkbox(set_checkbox_var(
                i).replace("(", "").replace(")", ""), key=i+9)
            if period:
                annual_periods.append(set_checkbox_var(i))
        if annual_periods == []:
            main_df = all_df[all_df["annually_period"].astype(
                str) == ""]
            st.warning("Silahkan pilih minimal satu periode tahunan.")
        else:
            start_date = annual_periods[0].split(" - ")[0].replace("(", "")
            end_date = annual_periods[len(
                annual_periods)-1].split(" - ")[1].replace(")", "")
            main_df = all_df[all_df["annually_period"].astype(
                str).str.contains("|".join(annual_periods))]
        all_district_df = main_df
    district = st.selectbox(
        label="Pilih Distrik",
        options=set_district_var(),
        key=0
    )
    if district != "Semua Distrik":
        main_df = main_df[main_df["station"] == district]
    else:
        main_df = all_district_df

st.title("Air Quality Dashboard")
st.header("Air Quality Index (AQI) in Districs of Tiongkok")

pm2_5_metrics, pm10_metrics = st.columns(2)
with pm2_5_metrics:
    st.markdown("<h3 style='text-align: center;'>PM2.5 (μg/m³)</h3>",
                unsafe_allow_html=True)
with pm10_metrics:
    st.markdown("<h3 style='text-align: center;'>PM10 (μg/m³)</h3>",
                unsafe_allow_html=True)
with pm2_5_metrics:
    avg_pm2_5_col, min_pm2_5_col, max_pm2_5_col = st.columns(3)
    with avg_pm2_5_col:
        avg_aqi_by_pm2_5 = create_aqi_stats_df(
            main_df).pm2_5_stats["mean"].mean()
        st.metric("Average", value=round(avg_aqi_by_pm2_5, 1))
    with min_pm2_5_col:
        min_aqi_by_pm2_5 = create_aqi_stats_df(
            main_df).pm2_5_stats["min"].min()
        st.metric("Min", value=round(min_aqi_by_pm2_5, 1))
    with max_pm2_5_col:
        max_aqi_by_pm2_5 = create_aqi_stats_df(
            main_df).pm2_5_stats["max"].max()
        st.metric("Max", value=round(max_aqi_by_pm2_5, 1))
with pm10_metrics:
    avg_pm10_col, min_pm10_col, max_pm10_col = st.columns(3)
    with avg_pm10_col:
        avg_aqi_by_pm10 = create_aqi_stats_df(
            main_df).pm10_stats["mean"].mean()
        st.metric("Average", value=round(avg_aqi_by_pm10, 1))
    with min_pm10_col:
        min_aqi_by_pm10 = create_aqi_stats_df(main_df).pm10_stats["min"].min()
        st.metric("Min", value=round(min_aqi_by_pm10, 1))
    with max_pm10_col:
        max_aqi_by_pm10 = create_aqi_stats_df(main_df).pm10_stats["max"].max()
        st.metric("Max", value=round(max_aqi_by_pm10, 1))

daily_tab, monthly_tab, quarterly_tab, semester_tab = st.tabs(
    ["Daily", "Monthly", "Quarterly", "Semester"]
)

pm2_5_var = "PM2.5"
pm10_var = "PM10"
selected_period = "D"
date_plt_title = "per-Day"

def plot_avg_aqi_pm2_5(ax, period):
    if period == "M" and len(annual_periods) < 2:
        x_axis = create_monthly_per_year_avg_aqi_df(main_df)['month']
    else:
        x_axis = create_avg_aqi_df(main_df, period)['date_time']
    ax.plot(
        x_axis,
        create_avg_aqi_df(main_df, period)['avg_pm2_5'],
        linewidth=2,
        marker='o',
        label='PM2.5',
        color='brown'
    )

def plot_avg_aqi_pm10(ax, period):
    if period == "M" and len(annual_periods) < 2:
        x_axis = create_monthly_per_year_avg_aqi_df(main_df)['month']
    else:
        x_axis = create_avg_aqi_df(main_df, period)['date_time']
    ax.plot(
        x_axis,
        create_avg_aqi_df(main_df, period)['avg_pm10'],
        linewidth=2,
        marker='o',
        label='PM10',
        color='orange'
    )

def plot_avg_aqi(period):
    if main_df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.grid(zorder=0)
    plt.ylabel("Concentration (μg/m³)")
    if pm2_5_var == "PM2.5":
        plot_avg_aqi_pm2_5(ax, period)
    if pm10_var == "PM10":
        plot_avg_aqi_pm10(ax, period)
    plt.legend()
    concatenation = ""
    if pm2_5_var == "PM2.5" and pm10_var == "PM10":
        concatenation = " and "
    else:
        concatenation = ""
    plt.title(
        f"Average Number of {pm2_5_var}{concatenation}{pm10_var} {date_plt_title}")
    st.pyplot(fig)

with daily_tab:
    daily_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="D")
    if len(daily_date_periods) > 6:
        st.subheader("Daily")
        selected_period = "D"
        date_plt_title = "per-Day"
        pm2_5_col, pm10_col = st.columns(2)
        with pm2_5_col:
            is_pm2_5 = st.checkbox("PM2.5", value=True, key=1)
        with pm10_col:
            is_pm10 = st.checkbox("PM10", value=True, key=2)
        if is_pm2_5 or is_pm10:
            pm2_5_var = "PM2.5" if is_pm2_5 else ""
            pm10_var = "PM10" if is_pm10 else ""
            plot_avg_aqi(selected_period)
        else:
            st.warning("Silakan pilih minimal satu variabel untuk ditampilkan")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu minggu.")
with monthly_tab:
    monthly_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="M")
    if len(monthly_date_periods) > 3:
        st.subheader("Monthly")
        selected_period = "M"
        date_plt_title = "per-Month"
        pm2_5_col, pm10_col = st.columns(2)
        with pm2_5_col:
            is_pm2_5 = st.checkbox("PM2.5", value=True, key=3)
        with pm10_col:
            is_pm10 = st.checkbox("PM10", value=True, key=4)
        if is_pm2_5 or is_pm10:
            pm2_5_var = "PM2.5" if is_pm2_5 else ""
            pm10_var = "PM10" if is_pm10 else ""
            plot_avg_aqi(selected_period)
        else:
            st.warning("Silakan pilih minimal satu variabel untuk ditampilkan.")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu caturwulan.")
with quarterly_tab:
    quarterly_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="Q")
    if len(quarterly_date_periods) > 3:
        st.subheader("Quarterly")
        selected_period = "Q"
        date_plt_title = "per-Quarter"
        pm2_5_col, pm10_col = st.columns(2)
        with pm2_5_col:
            is_pm2_5 = st.checkbox("PM2.5", value=True, key=5)
        with pm10_col:
            is_pm10 = st.checkbox("PM10", value=True, key=6)
        if is_pm2_5 or is_pm10:
            pm2_5_var = "PM2.5" if is_pm2_5 else ""
            pm10_var = "PM10" if is_pm10 else ""
            plot_avg_aqi(selected_period)
        else:
            st.warning("Silakan pilih minimal satu variabel untuk ditampilkan.")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu tahun.")
with semester_tab:
    if pd.to_datetime(end_date) - pd.to_datetime(start_date) >= max_date - min_date - timedelta(days=1):
        st.subheader("Semester")
        selected_period = "6M"
        date_plt_title = "per-Semester"
        pm2_5_col, pm10_col = st.columns(2)
        with pm2_5_col:
            is_pm2_5 = st.checkbox("PM2.5", value=True, key=7)
        with pm10_col:
            is_pm10 = st.checkbox("PM10", value=True, key=8)
        if is_pm2_5 or is_pm10:
            pm2_5_var = "PM2.5" if is_pm2_5 else ""
            pm10_var = "PM10" if is_pm10 else ""
            plot_avg_aqi(selected_period)
        else:
            st.warning("Silakan pilih minimal satu variabel untuk ditampilkan.")
    else:
        st.warning("Silakan pilih rentang waktu pada semua periode.")

st.subheader("Best & Worst AQI in Tiongkok Districs")
st.markdown("* #### Best & Worst AQI by Average of PM2.5 Parameter")
colors = ["yellow", "lightgrey", "lightgrey",
          "lightgrey", "lightgrey", "green"]
if main_df.empty or district != "Semua Distrik":
    st.warning("Tidak ada data untuk ditampilkan. Silakan pilih semua distrik.")
else:
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
    sns.barplot(
        x="avg_pm2_5",
        y="station",
        data=create_avg_aqi_by_station_df(main_df).sort_values("avg_pm2_5", ascending=False).head(), palette=colors, ax=ax[0]
    )
    ax[0].set_title("Worst AQI by PM2.5", fontsize=20)
    ax[0].set_xlabel("Concentration (μg/m³)", fontsize=16)
    ax[0].set_ylabel(None)
    ax[0].tick_params(labelsize=15)
    sns.barplot(
        x="avg_pm2_5",
        y="station",
        data=create_avg_aqi_by_station_df(main_df).sort_values(by="avg_pm2_5").head(), palette=reversed(colors), ax=ax[1]
    )
    ax[1].set_title("Best AQI by PM2.5", fontsize=20)
    ax[1].set_xlabel("Concentration (μg/m³)", fontsize=16)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_ylabel(None)
    ax[1].tick_params(labelsize=15)
    plt.suptitle("Worst and Best AQI by PM2.5", fontsize=24)
    st.pyplot(fig)

st.markdown("* #### Best & Worst AQI by Average of PM10 Parameter")
if main_df.empty or district != "Semua Distrik":
    st.warning("Tidak ada data untuk ditampilkan. Silakan pilih semua distrik.")
else:
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
    sns.barplot(
        x="avg_pm10",
        y="station",
        data=create_avg_aqi_by_station_df(main_df).sort_values("avg_pm10", ascending=False).head(), palette=colors, ax=ax[0]
    )
    ax[0].set_title("Worst AQI by PM10", fontsize=20)
    ax[0].set_xlabel("Concentration (μg/m³)", fontsize=16)
    ax[0].set_ylabel(None)
    ax[0].tick_params(labelsize=15)
    sns.barplot(
        x="avg_pm10",
        y="station",
        data=create_avg_aqi_by_station_df(main_df).sort_values(by="avg_pm10").head(), palette=reversed(colors), ax=ax[1]
    )
    ax[1].set_title("Best AQI by PM10", fontsize=20)
    ax[1].set_xlabel("Concentration (μg/m³)", fontsize=16)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_ylabel(None)
    ax[1].tick_params(labelsize=15)
    plt.suptitle("Worst and Best AQI by PM10", fontsize=24)
    st.pyplot(fig)

st.subheader("Best & Worst Time AQI by PM2.5 & PM10")
st.markdown("* #### Best & Worst AQI Time per-Day")

def plot_daily_avg_aqi():
    if main_df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.grid(zorder=0)
    plt.ylabel("Concentration (μg/m³)")
    if pm2_5_var == "PM2.5":
        ax.plot(
            create_daily_avg_aqi_df(main_df)['day'],
            create_daily_avg_aqi_df(main_df)['avg_pm2_5'],
            linewidth=2,
            marker='o',
            label='PM2.5',
            color='brown')
    if pm10_var == "PM10":
        ax.plot(
            create_daily_avg_aqi_df(main_df)['day'],
            create_daily_avg_aqi_df(main_df)['avg_pm10'],
            linewidth=2,
            marker='o',
            label='PM10',
            color='orange')
    plt.legend()
    concatenation = ""
    if pm2_5_var == "PM2.5" and pm10_var == "PM10":
        concatenation = " and "
    else:
        concatenation = ""
    plt.title(
        f"Average Number of {pm2_5_var}{concatenation}{pm10_var} per-Day")
    st.pyplot(fig)

daily_date_periods = pd.period_range(
    str(start_date), str(end_date), freq="D")
if len(daily_date_periods) > 6:
    pm2_5_col, pm10_col = st.columns(2)
    with pm2_5_col:
        is_pm2_5 = st.checkbox("PM2.5", value=True, key=14)
    with pm10_col:
        is_pm10 = st.checkbox("PM10", value=True, key=15)
    if is_pm2_5 or is_pm10:
        pm2_5_var = "PM2.5" if is_pm2_5 else ""
        pm10_var = "PM10" if is_pm10 else ""
        plot_daily_avg_aqi()
    else:
        st.warning("Silakan pilih minimal satu variabel untuk ditampilkan.")
else:
    st.warning("Silakan pilih rentang waktu minimal seminggu.")

st.markdown("* #### Best & Worst AQI Time per-Hour")

def plot_hourly_avg_aqi():
    if main_df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.grid(zorder=0)
    plt.ylabel("Concentration (μg/m³)")
    plt.xticks(rotation=45)
    if pm2_5_var == "PM2.5":
        ax.plot(
            create_hourly_avg_aqi_df(main_df)['hour'],
            create_hourly_avg_aqi_df(main_df)['pm2_5'],
            linewidth=2,
            marker='o',
            label='PM2.5',
            color='brown')
    if pm10_var == "PM10":
        ax.plot(
            create_hourly_avg_aqi_df(main_df)['hour'],
            create_hourly_avg_aqi_df(main_df)['pm10'],
            linewidth=2,
            marker='o',
            label='PM10',
            color='orange')
    plt.legend()
    concatenation = ""
    if pm2_5_var == "PM2.5" and pm10_var == "PM10":
        concatenation = " and "
    else:
        concatenation = ""
    plt.title(
        f"Average Number of {pm2_5_var}{concatenation}{pm10_var} per-Hour")
    st.pyplot(fig)

daily_date_periods = pd.period_range(
    str(start_date), str(end_date), freq="D")
if len(daily_date_periods) > 0:
    pm2_5_col, pm10_col = st.columns(2)
    with pm2_5_col:
        is_pm2_5 = st.checkbox("PM2.5", value=True, key=16)
    with pm10_col:
        is_pm10 = st.checkbox("PM10", value=True, key=17)
    if is_pm2_5 or is_pm10:
        pm2_5_var = "PM2.5" if is_pm2_5 else ""
        pm10_var = "PM10" if is_pm10 else ""
        plot_hourly_avg_aqi()
    else:
        st.warning("Silakan pilih minimal satu variabel untuk ditampilkan.")
else:
    st.warning("Silakan pilih rentang waktu minimal satu hari.")

st.subheader("AQI Demographics")
st.markdown("* #### Number of AQI Categories by PM2.5")

def set_custom_palette(counts, colors):
    max_count = counts.max()
    palettes = [colors[1] if count == max_count else colors[0]
                for count in counts]
    return palettes

if main_df.empty:
    st.warning("Tidak ada data untuk ditampilkan.")
else:
    color_list = ["lightgrey", "brown"]
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(
        y="aqi_by_pm2_5_count",
        x="aqi_by_pm2_5",
        data=create_aqi_by_pm2_5_df(main_df),
        palette=set_custom_palette(create_aqi_by_pm2_5_df(main_df).sort_values(by="aqi_by_pm2_5")[
                                   "aqi_by_pm2_5_count"], color_list)
    )
    plt.title("Number of AQI Categories by PM2.5", fontsize=20)
    plt.xlabel("Categories", fontsize=15)
    plt.ylabel(None)  # type: ignore
    st.pyplot(fig)

st.markdown("* #### Number of AQI Categories by PM10")
if main_df.empty:
    st.warning("Tidak ada data untuk ditampilkan.")
else:
    color_list = ["lightgrey", "orange"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        y="aqi_by_pm10_count",
        x="aqi_by_pm10",
        data=create_aqi_by_pm10_df(main_df),
        palette=set_custom_palette(create_aqi_by_pm10_df(main_df).sort_values(by="aqi_by_pm10")[
                                   "aqi_by_pm10_count"], color_list)
    )
    plt.title("Number of AQI Categories by PM10", fontsize=20)
    plt.xlabel("Categories", fontsize=14)
    plt.ylabel(None)  # type: ignore
    st.pyplot(fig)

st.subheader("Comparing PM2.5, PM10, SO₂, NO₂, and CO Correlation")

avg_so2_col, avg_no2_col, avg_co_col = st.columns(3)
with avg_so2_col:
    avg_so2 = create_agg_stats_df(main_df).so2_stats.mean()
    st.metric("Average SO₂ (μg/m³)", value=round(avg_so2, 2))
with avg_no2_col:
    avg_no2 = create_agg_stats_df(main_df).no2_stats.mean()
    st.metric("Average NO₂ (μg/m³)", value=round(avg_no2, 2))
with avg_co_col:
    avg_co = create_agg_stats_df(main_df).co_stats.mean()
    st.metric("Average CO (μg/m³)", value=round(avg_co, 2))

weekly_tab, monthly_tab, quarterly_tab, semester_tab = st.tabs(
    ["Weekly", "Monthly", "Quarterly", "Semester"],
)
period_plt_title = "per-Week"

def plot_agg(period):
    if main_df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    fig, ax0 = plt.subplots(figsize=(15, 10))
    plt.grid(zorder=0)
    plt.plot(
        create_agg_df(main_df, period).date_time,
        create_agg_df(main_df, period).avg_pm2_5,
        label='PM2.5',
        color='blue',
        linewidth=3,
        marker='o'
    )
    plt.plot(
        create_agg_df(main_df, period).date_time,
        create_agg_df(main_df, period).avg_pm10,
        label='PM10',
        color='orange',
        linewidth=3,
        marker='o'
    )
    plt.plot(
        create_agg_df(main_df, period).date_time,
        create_agg_df(main_df, period).avg_so2,
        label='SO₂',
        color='green',
        linestyle=':',
        linewidth=2,
        marker='o'
    )
    plt.plot(
        create_agg_df(main_df, period).date_time,
        create_agg_df(main_df, period).avg_no2,
        label='NO₂',
        color='red',
        linestyle='--',
        linewidth=2,
        marker='o'
    )
    plt.ylabel("Concentration PM2.5, PM10, SO₂, NO₂ (μg/m³)", fontsize=12)
    plt.xticks(rotation=45)
    ax1 = ax0.twinx()
    ax1.plot(
        create_agg_df(main_df, period).date_time,
        create_agg_df(main_df, period).avg_co,
        label='CO',
        color='purple',
        linestyle='-.',
        marker='o'
    )
    ax1.yaxis.tick_right()
    ax1.set_ylabel("Concentration CO (μg/m³)",
                   size=12, rotation=270, labelpad=20)
    ax1.set_xlabel(None)
    lines1, labels1 = ax0.get_legend_handles_labels()
    lines2, labels2 = ax1.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    plt.legend(lines, labels)
    plt.title(
        f'Correlation Belong PM2.5, PM10, SO₂, NO₂, and CO {period_plt_title}', fontsize=18)
    st.pyplot(fig)

with weekly_tab:
    daily_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="M")
    if len(daily_date_periods) > 0:
        st.subheader("Weekly")
        period_plt_title = "per-Week"
        plot_agg("W")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu bulan.")
with monthly_tab:
    monthly_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="M")
    if len(monthly_date_periods) > 3:
        st.subheader("Monthly")
        period_plt_title = "per-Month"
        plot_agg("M")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu caturwulan.")
with quarterly_tab:
    quarterly_date_periods = pd.period_range(
        str(start_date), str(end_date), freq="Q")
    if len(quarterly_date_periods) > 3:
        st.subheader("Quarterly")
        period_plt_title = "per-Quartal"
        plot_agg("Q")
    else:
        st.warning("Silakan pilih rentang waktu minimal satu tahun.")
with semester_tab:
    if pd.to_datetime(end_date) - pd.to_datetime(start_date) >= max_date - min_date - timedelta(days=1):
        st.subheader("Semester")
        period_plt_title = "per-Semester"
        plot_agg("6M")
    else:
        st.warning("Silakan pilih rentang waktu pada semua periode.")
