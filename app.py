import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Parking Tracker",
    page_icon="🚗",
    layout="wide"
)

st.title ("Parking Live Dashboard 🚗")

@st.cache_data(ttl=300)
def load_data():

    df = pd.read_csv("parking_data.csv")

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    latest_snapshot = df.tail(16)

    return df, latest_snapshot

try:

    df, latest_snapshot = load_data()

    st.subheader("Current Status of Parkings")

    cols = st.columns(4)

    for index, row in latest_snapshot.iterrows():
        with cols[index % 4]:

            pie_df = pd.DataFrame({
                "Status":["Free", "Occupied"],
                "Spots": [row['free_spots'], row['occupied_spots']]
            })

            
        fig = px.pie(
            pie_df, 
            values="Spots", 
            names="Status",
            title=f"🚗 {row['parking_name']}",
            hole=0.5,
            color="Status",
            color_discrete_map={"Free": "#2ecc71", "Occupied": "#e74c3c"}
        )
        
       
        fig.update_traces(textinfo='percent', showlegend=False)
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.metric("Free", f"{row['free_spots']} / {row['total_spots']}")

except:
    print("No data")