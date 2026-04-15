# 🗺️ GOOGLE MAPS & VISUALIZATIONS - QUICK START

## Launch with Maps & Charts

```bash
cd c:\Users\Shubha\Desktop\smart-safe-route-advisor

# Install (includes visualization packages)
pip install -r requirements.txt

# Run the enhanced app with all visualizations
streamlit run ui/app.py
```

**App opens at**: `http://localhost:8501`

---

## 🎬 What You'll See

### 1. Interactive Maps (2 side-by-side)
```
┌─────────────────────┬─────────────────────┐
│   Route A (Map)     │   Route B (Map)     │
│                     │                     │
│  Red line route     │  Green line route   │
│  Start/End markers  │  Start/End markers  │
│  Zoom/Pan controls  │  Zoom/Pan controls  │
└─────────────────────┴─────────────────────┘
```

### 2. Safety Comparison Chart
```
Safety Score Comparison

Route A    ████████░░  3.7/10
Route B    ███████████ 7.7/10
```

### 3. Risk Profile Radar Chart
```
Shows 3 dimensions:
- Crime Safety
- Lighting Safety  
- Isolation Safety

Route A vs Route B overlaid
```

### 4. Time vs Safety Scatter
```
X-axis: Travel time (15-20 minutes)
Y-axis: Safety score (3.7-7.7)
Points show the trade-off
```

### 5. Advanced Insights Metrics
```
Crime Risk Difference      50% safer
Lighting Risk Difference   30% better
Isolation Risk Difference  30% safer
```

---

## 🎮 INTERACTIVE FEATURES

### Maps
- **Scroll**: Zoom in/out
- **Click+Drag**: Pan around
- **Click Legend**: Toggle route visibility
- **Hover Marker**: See details

### Charts (Plotly)
- **Hover**: See exact values
- **Drag**: Pan within chart
- **Box Select**: Zoom to area
- **Legend Click**: Hide/show routes
- **Camera Icon**: Download as PNG

---

## 📌 SAMPLE INPUT VALUES

### Uses realistic NYC coordinates:

**Source Options**:
```
Downtown (40.7128, -74.0060)
Financial District (40.7074, -74.0113)
Midtown (40.7580, -73.9855)
```

**Destination Options**:
```
Residential Area (40.7589, -73.9851)
Upper West Side (40.7831, -73.9712)
Central Park (40.7829, -73.9654)
```

**Format accepted**:
- Just address name: "Downtown"
- With coordinates: "Downtown (40.7128, -74.0060)"
- Any format that contains (lat, lon)

---

## 🌍 HOW GOOGLE MAPS INTEGRATION WORKS

### Current: Folium (Free, No Auth)
✅ Works immediately
✅ OpenStreetMap tiles
✅ No API key needed
✅ Perfect for demo

### Code in `ui/app.py`:
```python
import folium
from streamlit_folium import st_folium

map_a = folium.Map(
    location=[40.7128, -74.0060],
    zoom_start=13,
    tiles="OpenStreetMap"
)

# Add route line
folium.PolyLine(route_coordinates).add_to(map_a)

# Display in Streamlit
st_folium(map_a, width=400, height=400)
```

---

## 🚀 API ENDPOINTS (For Backend)

### Start API:
```bash
python -m uvicorn app.main:app --reload
```

### Endpoints:

1. **POST /analyze** - Get route analysis
```json
{
  "source": "Downtown",
  "destination": "Residential Area",
  "time_of_day": "Day"
}
```

2. **GET /map/routes** - Interactive map (HTML)
```
http://localhost:8000/map/routes
```

3. **GET /map/crime-heatmap** - Crime heatmap (HTML)
```
http://localhost:8000/map/crime-heatmap
```

4. **GET /health** - Health check
```json
{
  "status": "healthy",
  "service": "Smart Safe Route Advisor"
}
```

---

## 📊 VISUALIZATION LIBRARIES USED

```python
# Maps
import folium
from streamlit_folium import st_folium

# Charts
import plotly.graph_objects as go
import plotly.express as px

# UI
import streamlit as st
```

---

## 🎯 MOCK DATA (FOR DEMO)

The app includes mock coordinates for demonstration:

**Route A** (Risky but Fast):
- 15 minutes
- High crime risk (70%)
- Poor lighting (60%)
- Isolated roads (50%)
- Score: 3.7/10

**Route B** (Safe but Longer):
- 20 minutes
- Low crime risk (20%)
- Good lighting (30%)
- Popular roads (20%)
- Score: 7.7/10

→ **Trade-off**: +5 minutes for 108% more safety

---

## 🔧 CUSTOMIZATION TIPS

### Change Colors:
```python
# In ui/app.py
marker_color = 'red'    # Available: red, blue, green, purple, etc.
chart_color = '#ff6b6b'  # Any hex color
```

### Add More Routes:
```python
# In data/routes.json
{
  "route": "C",
  "time": 18,
  "crime_risk": 0.4,
  "lighting_risk": 0.4,
  "isolation_risk": 0.3
}
```

### Connect Real APIs:
```python
# Replace mock data in app/maps.py
crime_data = fetch_from_crime_api(bbox)
route_data = fetch_from_directions_api(source, dest)
coordinates = geocode(address)
```

---

## ✨ IMPRESSIVE DEMO MOMENTS

1. **Load the app** - Watch maps appear instantly
2. **Change time to Night** - See risks increase by 10%
3. **Hover maps** - Reveal start/end points
4. **Interact with chart** - Zoom into specific data
5. **Check radar** - Show 360° risk comparison
6. **Point at metrics** - Show 50%, 30%, 30% differences
7. **Mention APIs** - Explain readiness for real Google Maps

---

## 🎬 DEMO SCRIPT

```
"Let me show you the enhanced version with maps and charts.

[Click to load the app]

Here you can see Route A in red and Route B in green on 
interactive maps. Both routes start downtown and go to the 
residential area.

[Point at safety chart]

The bar chart shows the safety scores. Route B is much safer.

[Highlight radar chart]

This radar chart shows all three risk factors:
- Crime (Route B is 50% safer)
- Lighting (Route B is 30% better)
- Isolation (Route B is 30% safer)

[Point at scatter plot]

Here's the trade-off: Route B takes 5 more minutes but is 
significantly safer. This is the value proposition.

[Switch to Night mode]

At night, all risks increase by 10%, but Route B remains 
the clear winner.

The API behind this is ready for real Google Maps integration—
with live traffic, actual crime statistics, and direction routes."
```

---

## 📱 RESPONSIVE DESIGN

All visualizations adapt to:
- ✅ Desktop (full features)
- ✅ Tablet (optimized layout)
- ✅ Mobile (stacked cards)
- ✅ Dark mode (theme-aware colors)
- ✅ Light mode (contrast-optimized)

---

## 🐛 TROUBLESHOOTING

**Maps don't load?**
- Check internet connection (needs OpenStreetMap CDN)
- Ensure folium is installed: `pip install folium`

**Charts not interactive?**
- Click a blank area of chart first
- Try different browser (Chrome works best)

**Coordinates not parsed?**
- Use format: "Place (lat, lon)"
- Example: "Downtown (40.7128, -74.0060)"

**Port 8501 in use?**
- Run: `streamlit run ui/app.py --server.port 8502`

---

## 📚 LEARN MORE

See full documentation in:
- `VISUALIZATIONS.md` - Complete visualization guide
- `README.md` - Project overview
- `DEMO.md` - Demo script
- `DEPLOYMENT.md` - Deployment guide

---

**Your app is fully enhanced and ready for impressive demo!** 🎉

Questions? Check the relevant documentation file above.
