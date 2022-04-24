import streamlit as st
import pandas as pd
import plotly.express as px


def lines(df: pd.DataFrame, container=st):
    # df.set_index("date", inplace=True)
    # df.index = pd.DatetimeIndex(df.index)
    # st.line_chart(df)
    fig = px.line(
        df,
        x="login_date",
        y=df.columns,
        title="",
        labels={"date": "", "value": ""},
        # hover_data={"date": "|%B %d, %Y"},
    )
    fig.update_traces(mode="lines", hovertemplate="%{y:f}")  # , showlegend=False
    fig.update_layout(
        margin={"r": 0, "l": 0, "t": 0, "b": 0},
        # paper_bgcolor="#fff",
        plot_bgcolor="rgba(0,0,0,0)",
        # height=600,
        # xaxis_title="Data",
        # yaxis_title=f"Valore ({currency_symbol})",
        legend=dict(
            orientation="h",
            # yanchor="bottom",
            # y=1,
            # xanchor="right",
            # x=1,
            title="",
        ),
        hovermode="x unified",
        dragmode=False,
    )
    fig.update_xaxes(
        showgrid=False,
        # showline=True,
        # linewidth=1,
        # linecolor="black",
        # dtick="M3",
        # tickformat="%b\n%Y",
        ticklabelmode="period",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            ),
            bgcolor="white",
            # font=dict(color="black"),
        ),
    )
    fig.update_yaxes(
        tickformat="%0.2f",
        gridcolor="#ddd",
        side="right",
        autorange=True,
        # ticklabelposition="inside",
    )
    container.plotly_chart(
        fig,
        use_container_width=True,
        config=dict(displayModeBar=False),
    )
