import streamlit as st
import pandas as pd
import charts


uploaded_file = st.file_uploader("Upload file eventi keycloak", type=["csv"])
if uploaded_file is not None:
    events = pd.read_csv(
        "keycloack-events.csv", usecols=["email", "login_date", "user_id", "session_id"]
    ).iloc[::-1]
    events["login_date"] = pd.to_datetime(
        events["login_date"], format="%d/%m/%Y %H:%M:%S"
    )

    freqency = st.selectbox(
        "Frequenza dati",
        [
            {
                "label": "Giornaliera",
                "value": "1D",
            },
            {
                "label": "3 Giorni",
                "value": "3D",
            },
            {
                "label": "Settimanale",
                "value": "1W",
            },
            {
                "label": "Mensile",
                "value": "1M",
            },
        ],
        format_func=lambda x: x["label"],
    )["value"]

    period = st.date_input(
        "Periodo",
        value=[events["login_date"].min(), events["login_date"].max()],
        min_value=events["login_date"].min(),
        max_value=events["login_date"].max(),
    )
    events = events.loc[
        (events["login_date"] >= pd.Timestamp(period[0]))
        & (events["login_date"] <= pd.Timestamp(period[1]))
    ]

    sessions_per_user = (
        events.groupby("user_id")
        .count()
        .drop(columns=["email", "login_date"])
        .rename(columns={"session_id": "number_of_sessions"})
    )
    registrations = (
        events.drop_duplicates(subset=["user_id"], keep="first")
        .rename(columns={"login_date": "registration_date"})
        .drop(columns=["session_id"])
        .reset_index(drop=True)
    )
    users = (
        events.groupby("user_id")
        .agg({"session_id": "count", "login_date": "min"})
        .rename(
            columns={
                "session_id": "number_of_logins",
                "login_date": "registration_date",
            }
        )
    )

    statistics = pd.DataFrame(
        {
            "number_of_logins": events.groupby(
                pd.Grouper(key="login_date", freq=freqency)
            )["session_id"].count(),
            "number_of_users": events.groupby(
                pd.Grouper(key="login_date", freq=freqency)
            )["user_id"].nunique(),
            "number_of_registrations": registrations.groupby(
                pd.Grouper(key="registration_date", freq=freqency)
            ).count()["user_id"],
        }
    )

    cumulative_statistics = pd.DataFrame(
        {
            "cumulative_logins": statistics["number_of_logins"].cumsum(),
            "cumulative_registrations": statistics["number_of_registrations"].cumsum(),
        }
    )

    st.header("Eventi")
    charts.lines(statistics)
    charts.lines(cumulative_statistics)

    st.header("Utenti")
    charts.lines(
        sessions_per_user.reset_index()
        .groupby("number_of_sessions")
        .count()
        .rename(columns={"user_id": "number_of_users"})
        .sort_index(ascending=False)
        .cumsum()
    )
    st.dataframe(registrations)
    st.download_button(
        "Download Tabella Utenti",
        registrations.to_csv(index=False).encode("utf-8"),
        f"wallible_registred_users.csv",
        mime="text/csv",
    )
