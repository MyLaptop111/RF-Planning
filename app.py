import math
import streamlit as st
import folium
from folium.plugins import MeasureControl, Draw
from streamlit_folium import st_folium

from rf_engine.propagation import fspl_db, okumura_hata_db, cost231_hata_db
from rf_engine.link_budget import mapl_db, noise_floor_dbm, rsrp_dbm
from rf_engine.dimensioning import hex_cell_area_km2, sites_from_area, sites_from_capacity, required_sites
from rf_engine.geometry import haversine_km, polygon_area_m2

st.set_page_config(page_title="RF Planner V2", layout="wide")
st.title("📡 RF Planning & Dimension Tool — V2")

st.sidebar.header("RF Parameters")
technology = st.sidebar.selectbox("Technology", ["4G LTE", "5G NR", "2G GSM", "3G UMTS"])
model = st.sidebar.selectbox("Propagation Model", ["Free Space", "Okumura-Hata", "COST-231 Hata"])

freq = st.sidebar.number_input("Frequency (MHz)", min_value=100.0, max_value=6000.0, value=1800.0, step=10.0)
tx_power = st.sidebar.number_input("Tx Power (dBm)", value=43.0, step=1.0)
tx_gain = st.sidebar.number_input("Tx Antenna Gain (dBi)", value=17.0, step=1.0)
rx_gain = st.sidebar.number_input("Rx Antenna Gain (dBi)", value=0.0, step=1.0)
hb = st.sidebar.number_input("BS Antenna Height (m)", value=30.0, min_value=1.0, step=1.0)
hm = st.sidebar.number_input("UE Height (m)", value=1.5, min_value=0.5, step=0.5)
bandwidth_mhz = st.sidebar.number_input("Bandwidth (MHz)", value=20.0, min_value=0.1, step=5.0)

st.sidebar.header("Link Budget Losses")
cable_loss = st.sidebar.number_input("Cable/Feeder Loss (dB)", value=2.0, step=0.5)
body_loss = st.sidebar.number_input("Body Loss (dB)", value=0.0, step=0.5)
penetration_loss = st.sidebar.number_input("Building Penetration (dB)", value=0.0, step=1.0)
shadow_margin = st.sidebar.number_input("Shadowing Margin (dB)", value=8.0, step=1.0)
interference_margin = st.sidebar.number_input("Interference Margin (dB)", value=3.0, step=1.0)
rx_sensitivity = st.sidebar.number_input("Rx Sensitivity (dBm)", value=-100.0, step=1.0)
cm = st.sidebar.number_input("COST-231 City Correction Cm (dB)", value=3.0, step=1.0)

mapl = mapl_db(tx_power, tx_gain, rx_gain, cable_loss, body_loss, penetration_loss,
               shadow_margin, interference_margin, rx_sensitivity)
noise = noise_floor_dbm(bandwidth_mhz*1e6)

c1,c2,c3,c4 = st.columns(4)
c1.metric("MAPL", f"{mapl:.1f} dB")
c2.metric("Noise Floor", f"{noise:.1f} dBm")
c3.metric("Technology", technology)
c4.metric("Frequency", f"{freq:.0f} MHz")

st.subheader("📏 Dimension & Map")
if "sites" not in st.session_state: st.session_state.sites=[]

m=folium.Map(location=[30.0444,31.2357], zoom_start=12, tiles="OpenStreetMap")
MeasureControl(primary_length_unit="kilometers", primary_area_unit="sqkilometers").add_to(m)
Draw(export=True, draw_options={
    "polyline": True, "polygon": True, "rectangle": True, "circle": False,
    "marker": True, "circlemarker": False
}).add_to(m)

for i,(lat,lon) in enumerate(st.session_state.sites,1):
    folium.Marker([lat,lon], tooltip=f"Candidate Site {i}",
                  icon=folium.Icon(icon="signal", prefix="fa")).add_to(m)

map_data=st_folium(m, height=560, width=None)

col1,col2=st.columns(2)
with col1:
    if map_data and map_data.get("last_clicked"):
        p=map_data["last_clicked"]
        if st.button("➕ Add Candidate Site"):
            st.session_state.sites.append((p["lat"],p["lng"]))
            st.rerun()

with col2:
    if st.button("🗑 Clear Candidate Sites"):
        st.session_state.sites=[]
        st.rerun()

if st.session_state.sites:
    st.write("Candidate Sites:", len(st.session_state.sites))
    st.dataframe(
        [{"Site":i, "Latitude":round(p[0],6), "Longitude":round(p[1],6)}
         for i,p in enumerate(st.session_state.sites,1)],
        use_container_width=True
    )

st.divider()
st.subheader("📐 Site Dimensioning")

area_km2=st.number_input("Planning Area (km²)", min_value=0.01, value=25.0, step=1.0)
radius_km=st.number_input("Estimated Cell Radius (km)", min_value=0.01, value=1.5, step=0.1)
traffic_erl=st.number_input("Total Offered Traffic (Erlang)", min_value=0.0, value=100.0, step=10.0)
site_capacity_erl=st.number_input("Traffic Capacity / Site (Erlang)", min_value=0.1, value=20.0, step=1.0)

n_cov=sites_from_area(area_km2,radius_km)
n_cap=sites_from_capacity(traffic_erl,site_capacity_erl)
n_req=required_sites(n_cov,n_cap)

d1,d2,d3,d4=st.columns(4)
d1.metric("Hex Cell Area", f"{hex_cell_area_km2(radius_km):.2f} km²")
d2.metric("Coverage Sites", n_cov)
d3.metric("Capacity Sites", n_cap)
d4.metric("Required Sites", n_req)

st.info("This V2 is an engineering calculation foundation. Real-world planning should add antenna patterns, terrain/buildings, clutter, sectorization, load models, interference, and a validated 3GPP/ITU propagation model before field deployment.")

st.divider()
st.subheader("📶 Path Loss / RSRP Calculator")
distance_km=st.number_input("Distance (km)", min_value=0.001, value=1.0, step=0.1)

try:
    if model=="Free Space":
        pl=fspl_db(freq,distance_km)
    elif model=="Okumura-Hata":
        pl=okumura_hata_db(freq,hb,hm,distance_km)
    else:
        pl=cost231_hata_db(freq,hb,hm,distance_km,cm)
    rx=rsrp_dbm(tx_power,tx_gain,rx_gain,pl,cable_loss+body_loss+penetration_loss)
    st.write(f"**Path Loss:** {pl:.2f} dB")
    st.write(f"**Received Power / RSRP proxy:** {rx:.2f} dBm")
except ValueError as e:
    st.warning(str(e))

st.caption("Next V3: coverage grid + heatmap + sector azimuth/downtilt + interference/SINR + automated site placement/optimization.")
