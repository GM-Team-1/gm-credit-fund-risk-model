import plotly.express as px
import pydeck as pdk
import streamlit as st

def run(st, data_store, ctx):
    st.title("Geographic Analysis")
    st.markdown("State & county level visualizations.")

    state_df = data_store.get("state_heatmap_data", None)
    county_df = data_store.get("county_heatmap_data", None)

    # State heatmap
    if state_df is not None and not state_df.empty:
        st.subheader("State heatmap")
        value_col = next((c for c in state_df.columns if c.lower() in ("value","score","metric","rate","target")), None)
        state_col = next((c for c in state_df.columns if c.lower() in ("state","state_code","state_abbrev")), None)
        if state_col and value_col:
            fig = px.choropleth(
                state_df,
                locations=state_col,
                locationmode="USA-states",
                color=value_col,
                scope="usa",
                labels={value_col: value_col},
                hover_data=state_df.columns.tolist()
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(state_df.head())
    else:
        st.info("No state heatmap data available.")

    # County heatmap
    if county_df is not None and not county_df.empty:
        st.subheader("County heatmap")
        lat_col = next((c for c in county_df.columns if c.lower() in ("lat","latitude")), None)
        lon_col = next((c for c in county_df.columns if c.lower() in ("lon","lng","longitude")), None)
        value_col = next((c for c in county_df.columns if c.lower() in ("value","score","metric","rate","target")), None)
        if lat_col and lon_col:
            view_state = pdk.ViewState(latitude=county_df[lat_col].mean(), longitude=county_df[lon_col].mean(), zoom=4)
            layer = pdk.Layer(
                "HeatmapLayer" if value_col else "ScatterplotLayer",
                data=county_df,
                get_position=f"[{lon_col}, {lat_col}]",
                aggregation="MEAN",
                get_weight=value_col if value_col else 1,
                radiusPixels=50
            )
            deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
            st.pydeck_chart(deck)
        else:
            st.dataframe(county_df.head())
    else:
        st.info("No county heatmap data available.")
