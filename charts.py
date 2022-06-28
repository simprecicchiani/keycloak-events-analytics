import streamlit as st
import pandas as pd
import plotly.express as px


def lines(df: pd.DataFrame, container=st):
    fig = px.line(
        df,
        title="",
        labels={"date": "", "value": ""},
    )
    fig.update_traces(mode="lines", hovertemplate="%{y:f}")
    fig.update_layout(
        margin={"r": 0, "l": 0, "t": 0, "b": 0},
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            title="",
            x=0,
            y=1.2,
        ),
        hovermode="x unified",
        dragmode=False,
    )
    fig.update_yaxes(
        tickformat="%0.2f",
        gridcolor="#ddd",
        side="left",
    )
    container.plotly_chart(
        fig,
        use_container_width=True,
        config=dict(displayModeBar=False),
    )
