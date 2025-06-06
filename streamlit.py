import streamlit as st
import laspy
import numpy as np
import pandas as pd
import pydeck as pdk

st.title("🛰️ Point Cloud Viewer (.laz/.las)")

uploaded_file = st.file_uploader("Upload a .laz or .las file", type=["laz", "las"])

if uploaded_file:
    with open("temp.laz", "wb") as f:
        f.write(uploaded_file.read())

    las = laspy.read("temp.laz")
    xyz = np.vstack((las.x, las.y, las.z)).T
    df = pd.DataFrame(xyz, columns=["x", "y", "z"]).sample(n=min(10000, len(xyz)))

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=np.mean(df['y']),
            longitude=np.mean(df['x']),
            zoom=18,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "PointCloudLayer",
                data=df,
                get_position='[x, y, z]',
                get_normal=[0, 0, 15],
                point_size=1
            )
        ]
    ))
