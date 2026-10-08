# RF Planner V2

Run:
python -m pip install -r requirements.txt
python -m streamlit run app.py

V2 includes:
- Interactive map + measurement tools
- Candidate site placement
- MAPL / link budget
- Noise floor
- Free-space path loss
- Okumura-Hata
- COST-231 Hata
- RSRP/received-power proxy
- Coverage-based site estimate
- Capacity-based site estimate
- Required sites = max(coverage, capacity, traffic)

Roadmap:
V3: grid coverage heatmap, antenna sectors, azimuth/downtilt, SINR/interference.
V4: 3GPP/ITU models, terrain/buildings/clutter.
V5: automatic candidate generation + optimization.
V6: GIS layers, reports and validation.
