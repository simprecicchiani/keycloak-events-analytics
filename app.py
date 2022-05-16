import streamlit as st
import pandas as pd
import charts

uploaded_file = st.file_uploader("Upload a file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["login_date"] = pd.to_datetime(df["login_date"], format="%d/%m/%Y %H:%M:%S")

    sessions_per_user = df.groupby("user_id").count()["session_id"]
    registrations = df.loc[::-1].drop_duplicates(subset=["user_id"], keep="first")

    freq = st.selectbox("Data frequency", ["1D", "3D", "1W", "1M"])

    daily_stats = pd.DataFrame()
    daily_stats["logins"] = df.groupby(pd.Grouper(key="login_date", freq=freq))[
        "session_id"
    ].count()
    daily_stats["users"] = df.groupby(pd.Grouper(key="login_date", freq=freq))[
        "user_id"
    ].nunique()
    daily_stats["registrations"] = registrations.groupby(
        pd.Grouper(key="login_date", freq=freq)
    ).count()["user_id"]
    st.header(f"{freq} Stats")
    charts.lines(daily_stats.reset_index())

    cumulative_stats = pd.DataFrame()
    cumulative_stats["users"] = daily_stats["registrations"].cumsum()
    cumulative_stats["logins"] = daily_stats["logins"].cumsum()

    st.header("Cumulative Stats")
    charts.lines(cumulative_stats.reset_index())

    st.header("Number of Users")
    login_boundary = st.number_input(
        "Login boundary", min_value=1, max_value=100, value=1
    )
    st.metric(
        f"Users with more than {login_boundary} login",
        sessions_per_user[sessions_per_user.gt(login_boundary)].size,
    )

    st.header("Registrations")
    st.dataframe(registrations)
    st.download_button(
        "Scarica Posizioni",
        registrations.to_csv(index=False).encode("utf-8"),
        f"wallible_registred_users.csv",
        mime="text/csv",
    )
