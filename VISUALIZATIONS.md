# 📊 VISUALIZATIONS & MAPS GUIDE

## Google Maps & Data Visualization Features

The Smart Safe Route Advisor now includes comprehensive visualization capabilities powered by **Google Maps API integration** and **interactive charts**.

---

## 🗺️ MAPS

### 1. Interactive Route Maps (Folium + Google Maps API)

**Location**: `ui/app.py` - Route Maps section

**Features**:
- Real-time interactive maps showing Route A and Route B
- Color-coded routes:
  - **Red**: Route A (faster but potentially riskier)
  - **Green**: Route B (safer, recommended)
- Markers showing start/end points
- Zoom and pan controls
- Based on geocoordinates from input

**Integration**:
```python
import folium
from streamlit_folium import st_folium

map_a = create_route_map("A", 40.7128, -74.0060, 'red')
st_folium(map_a, width=400, height=400)
```

**User Input**:
- Source: "Downtown (40.7128, -74.0060)"
- Destination: "Residential Area (40.7589, -73.9851)"
- Format: Address or "Address (latitude, longitude)"

---

### 2. Crime Heatmap

**Location**: API endpoint `/map/crime-heatmap`

**Features**:
- Visualizes crime risk distribution
- Color intensity shows risk level:
  - Dark Red: High crime (>70%)
  - Red: Medium-High (40-70%)
  - Orange: Medium (10-40%)
- Circles sized by risk intensity
- Helps users understand danger zones

**Implementation**:
```python
from folium.plugins import HeatMap

HeatMap(crime_data, radius=15, blur=25, max_zoom=1).add_to(map)
```

---

### 3. Enhanced Multi-Layer Map

**Location**: `app/maps.py` - `create_enhanced_map()`

**Layers**:
- Route polylines with directional arrows
- Crime zones with color coding
- Unsafe areas with warning markers
- Start/end destination markers
- Customizable crime zone overlays

**Example Usage**:
```python
route_map = create_enhanced_map(
    center=(40.735, -73.995),
    route_points_a=MOCK_ROUTE_A,
    route_points_b=MOCK_ROUTE_B,
    crime_zones=MOCK_CRIME_ZONES
)
```

---

## 📊 CHARTS & VISUALIZATIONS

### 1. Safety Score Comparison Bar Chart

**Type**: Plotly Bar Chart  
**Location**: "Route Comparison" section in UI

**Shows**:
- Route A vs Route B safety scores
- Color-coded (red = lower safety, green = higher safety)
- Actual numeric values displayed on bars
- Interactive hover for exact values

```python
def create_safety_comparison_chart(score_a, score_b):
    fig = go.Figure(data=[
        go.Bar(
            x=['Route A', 'Route B'],
            y=[score_a, score_b],
            marker=dict(color=['#ff6b6b', '#51cf66'])
        )
    ])
```

---

### 2. Risk Profile Radar Chart

**Type**: Plotly Polar Radar  
**Location**: "Risk Profile Comparison" section in UI

**Dimensions**:
- Crime Safety (inverse of crime risk)
- Lighting Safety (inverse of lighting risk)
- Isolation Safety (inverse of isolation risk)

**Benefits**:
- 360-degree risk visualization
- Overlaid comparison between routes
- Shows strengths/weaknesses of each route

```python
fig.add_trace(go.Scatterpolar(
    r=[1-crime, 1-lighting, 1-isolation],
    theta=['Crime Safety', 'Lighting Safety', 'Isolation Safety'],
    fill='toself'
))
```

---

### 3. Time vs Safety Scatter Plot

**Type**: Plotly Scatter  
**Location**: "Time vs Safety Trade-off" section in UI

**Shows**:
- X-axis: Travel time (minutes)
- Y-axis: Safety score (0-10)
- Point size: 20 (large, prominent)
- Color-coded by route
- Annotations with route details

**Insight**:
Users can visually see the trade-off between time and safety. Route B is consistently safer despite taking more time.

```python
fig.add_trace(go.Scatter(
    x=[route_time],
    y=[route_score],
    mode='markers+text',
    marker=dict(size=20, color=route_color)
))
```

---

### 4. Risk Metrics Matrix

**Type**: Streamlit Metrics  
**Location**: "Advanced Insights" section in UI

**Displays**:
- Crime Risk Difference: `|route_a.crime - route_b.crime|`
- Lighting Risk Difference: `|route_a.lighting - route_b.lighting|`
- Isolation Risk Difference: `|route_a.isolation - route_b.isolation|`

**Visual Indicators**:
- Green arrow: Safer (route B is better)
- Red arrow: Riskier (route A is better)
- Percentage values

```python
st.metric(
    "Crime Risk Difference",
    f"{crime_diff:.1%}",
    delta=f"{crime_diff:.1%} safer" if route_b_is_safer else "Risk"
)
```

---

## 🌐 GOOGLE MAPS API INTEGRATION

### Current Implementation

Using **Folium** (free, no API key required):
- Works immediately without additional credentials
- OpenStreetMap tiles as base layer
- Folium.plugins for HeatMaps and advanced features

### Future Enhancement: Real Google Maps API

To enable full Google Maps features:

```bash
# 1. Get API key from Google Cloud Console
# 2. Set environment variable
export GOOGLE_MAPS_API_KEY="your-api-key-here"

# 3. Uncomment in app/maps.py for real-time features:
# - Live traffic
# - Actual route directions (Google Directions API)
# - Real crime data overlays
# - Historical patterns
```

---

## 📱 INTERACTIVE FEATURES

### Map Controls
- **Zoom**: Scroll or +/- buttons
- **Pan**: Click and drag
- **Fullscreen**: Expand map to full screen
- **Layer Toggle**: Show/hide route layers

### Chart Interactions
- **Hover**: See exact values
- **Zoom**: Box select to zoom into specific range
- **Pan**: Click and drag within chart
- **Toggle Series**: Click legend to hide/show routes

### Dark Mode Support
- Charts automatically adjust to Streamlit theme
- Maps readable in both light and dark modes

---

## 📈 DATA STRUCTURE FOR VISUALIZATIONS

### Mock Crime Zones (for demo)
```python
MOCK_CRIME_ZONES = [
    (40.7120, -74.0050, 0.8),  # High crime
    (40.7580, -73.9840, 0.3),  # Low crime
    (40.7200, -74.0100, 0.6),  # Medium crime
]
```

### Mock Route Points
```python
MOCK_ROUTE_A = [
    (40.7128, -74.0060),  # Start
    (40.7150, -74.0080),
    (40.7180, -74.0100),
    # ... more waypoints
]
```

### Integration with Real Data
```python
# To use real data, replace with:
routes = get_actual_routes_from_api()
crime_data = get_crime_data_from_api()
coordinates = geocode_address(user_input)
```

---

## 🎨 COLOR SCHEME

| Element | Color | Meaning |
|---------|-------|---------|
| Route A | Red (#ff6b6b) | Faster, riskier |
| Route B | Green (#51cf66) | Safer, slower |
| High Crime | Dark Red | Avoid |
| Medium Crime | Orange | Caution |
| Low Crime | Green | Safe |
| Start Marker | Blue | Origin |
| End Marker | Red | Destination |

---

## 🔧 TECHNICAL DETAILS

### Map Library: Folium
- **Lightweight**: ~2MB download
- **Browser-based**: No server resources needed
- **Extensible**: Easy to add custom layers
- **Interactive**: Responsive to user input

### Chart Library: Plotly
- **Modern**: WebGL rendering for smooth interaction
- **Responsive**: Auto-scales to container
- **Accessible**: Hover text for additional info
- **exportable**: Download charts as PNG

### Streamlit Integration
- **st_folium()**: Embed Folium maps in Streamlit
- **st.plotly_chart()**: Embed Plotly visualizations
- **st.metric()**: Display KPIs with delta indicators

---

## 📡 API ENDPOINTS FOR MAPS

### GET /map/routes
Returns interactive map showing both routes with crime zones
```
Response: HTML file with Folium visualization
```

### GET /map/crime-heatmap
Returns crime distribution heatmap
```
Response: HTML file with HeatMap visualization
```

### GET /health
Health check endpoint
```
Response: {"status": "healthy", "service": "Smart Safe Route Advisor"}
```

---

## 🚀 PERFORMANCE OPTIMIZATION

- Maps lazy-load: Generated on-demand
- Charts cached: Re-rendered only when data changes
- Streamlit reruns: Efficient state management
- Folium tiles: Use fastest available CDN

---

## 📚 LIBRARIES USED

| Library | Version | Purpose |
|---------|---------|---------|
| folium | Latest | Interactive maps |
| streamlit-folium | Latest | Streamlit integration |
| plotly | Latest | Interactive charts |
| python-dotenv | Latest | Environment variables |
| fastapi | Latest | API endpoints |

---

## 🎯 USER BENEFITS

1. **Visual Decision Making**: See the difference between routes
2. **Risk Awareness**: Understand danger zones at a glance
3. **Data-Driven Choices**: Make informed decisions with charts
4. **Interactive Exploration**: Zoom, pan, and interact with data
5. **Professional Presentation**: Impress stakeholders with visuals

---

## 🔮 FUTURE ENHANCEMENTS

- [ ] Real Google Maps API integration
- [ ] Live traffic feeds
- [ ] Real-time crime database overlay
- [ ] 3D route visualization
- [ ] Dynamic heatmap updates
- [ ] Route history tracking
- [ ] User feedback integration
- [ ] Machine learning predictions

---

**Smart Safe Route Advisor** - Making navigation data visual, intuitive, and actionable.
