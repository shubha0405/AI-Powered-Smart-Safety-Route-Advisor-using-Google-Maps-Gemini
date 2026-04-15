import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routes import get_routes
from app.safety import calculate_safety_score
from app.utils import adjust_risk_by_time
from app.ai import generate_explanation

import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go


# ==================== ULTRA MODERN COLORFUL CSS ====================
def apply_stunning_styling():
    """Apply vibrant, colorful, modern styling."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Gradient Background */
    .main {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header with Neon Glow */
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 50px 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4), 
                    0 0 40px rgba(240, 147, 251, 0.3),
                    inset 0 1px 0 rgba(255,255,255,0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .header-section h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .header-section p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-top: 15px;
        font-weight: 500;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea;
        padding: 25px;
        border-radius: 16px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
        border-color: #764ba2;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 15px 0;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.85rem;
        margin: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #ffd600 0%, #ffaa00 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(255, 214, 0, 0.3);
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Recommendation Box */
    .recommendation-safe {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #00a8e8 100%);
        color: white;
        padding: 35px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 20px 60px rgba(0, 212, 255, 0.3),
                    0 0 0 1px rgba(255,255,255,0.2) inset;
        border: 2px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-safe h3 {
        color: white;
        margin: 0 0 15px 0;
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.35) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.45) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15),
                    0 10px 30px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #999;
        border-top: 2px solid rgba(102, 126, 234, 0.2);
        margin-top: 50px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def create_route_map(name, lat, lon, color):
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB positron")
    folium.Marker(location=[lat, lon], popup=f"Route {name}", icon=folium.Icon(color=color, icon="location", prefix='fa')).add_to(m)
    folium.Circle(location=[lat, lon], radius=500, color=color, fill=True, fillColor=color, fillOpacity=0.15, weight=3).add_to(m)
    return m


def create_safety_chart(s_a, s_b):
    fig = go.Figure(data=[go.Bar(x=['Route A', 'Route B'], y=[s_a, s_b], marker=dict(color=['rgb(255, 107, 107)', 'rgb(0, 212, 255)'], line=dict(color=['rgb(255, 68, 68)', 'rgb(0, 150, 255)'], width=3)), text=[f"{s_a}/10", f"{s_b}/10"], textposition='outside')])
    fig.update_layout(title=dict(text="<b>🛡️ Safety Score Comparison</b>", font=dict(size=24, color='#667eea')), yaxis_title="<b>Score</b>", height=500, plot_bgcolor='rgba(200, 200, 255, 0.05)', yaxis=dict(range=[0, 10]))
    return fig


def create_radar_chart(r_a, r_b):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[1-r_a['crime_risk'], 1-r_a['lighting_risk'], 1-r_a['isolation_risk']], theta=['Crime Safe', 'Lighting', 'Isolation'], fill='toself', name='Route A', line=dict(color='rgb(255, 107, 107)', width=3), fillcolor='rgba(255, 107, 107, 0.35)'))
    fig.add_trace(go.Scatterpolar(r=[1-r_b['crime_risk'], 1-r_b['lighting_risk'], 1-r_b['isolation_risk']], theta=['Crime Safe', 'Lighting', 'Isolation'], fill='toself', name='Route B', line=dict(color='rgb(0, 212, 255)', width=3), fillcolor='rgba(0, 212, 255, 0.35)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=600, title=dict(text="<b>📊 Risk Profile</b>", font=dict(size=24, color='#667eea')))
    return fig


def main():
    st.set_page_config(page_title="SafeRoute", page_icon="🗺️", layout="wide", initial_sidebar_state="expanded")
    
    apply_stunning_styling()
    
    # SIDEBAR with Login Button
    with st.sidebar:
        st.markdown("### 👤 Account")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Login", use_container_width=True):
                st.info("Welcome! Demo Mode Active ✨", icon="ℹ️")
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.success("Logged out!", icon="✅")
        
        st.divider()
        st.markdown("### ⚙️ Settings")
        time_of_day = st.radio("Time", ["Day 🌞", "Night 🌙"], label_visibility="collapsed").split()[0]
        
        st.markdown("### 📍 Journey")
        source = st.text_input("📌 Start", "Downtown (40.7128, -74.0060)")
        destination = st.text_input("🎯 End", "Residential (40.7589, -73.9851)")
    
    # HEADER
    st.markdown("""
    <div class="header-section">
        <h1>🗺️ Smart Safe Route Navigator</h1>
        <p>AI-powered route safety. Arrive safer, every time. ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DATA
    raw_routes = get_routes()
    route_a = adjust_risk_by_time(raw_routes[0], time_of_day)
    route_b = adjust_risk_by_time(raw_routes[1], time_of_day)
    
    score_a = calculate_safety_score(route_a)
    score_b = calculate_safety_score(route_b)
    safer_route = "A" if score_a > score_b else "B"
    improvement = ((max(score_a, score_b) - min(score_a, score_b)) / min(score_a, score_b) * 100)
    time_diff = abs(route_a['time'] - route_b['time'])
    explanation = generate_explanation(route_a, route_b, score_a, score_b)
    
    # STATS
    st.markdown("### 📊 Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">🏆 Recommended</div><div class="metric-value">Route {safer_route}</div><span class="badge badge-success">+{improvement:.0f}%</span></div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">⏱️ Route A</div><div class="metric-value">{route_a['time']}m</div><span class="badge badge-warning">vs {route_b['time']}m</span></div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">🛡️ Safety</div><div class="metric-value">{score_a}/10</div><span class="badge badge-success">vs {score_b}/10</span></div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">⏰ Difference</div><div class="metric-value">{time_diff}m</div><span class="badge badge-danger">Extra</span></div>""", unsafe_allow_html=True)
    
    st.divider()
    
    # TABS
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ MAPS", "📊 CHARTS", "🤖 AI", "📋 COMPARE", "❓ HELP"])
    
    with tab1:
        st.markdown("### 🗺️ Route Maps")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%); padding: 18px; border-radius: 14px; color: white; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(255,107,107,0.3);'><b>📍 Route A</b> • <b>{route_a['time']}min</b> • 🛡️ <b>{score_a}/10</b></div>", unsafe_allow_html=True)
            st_folium(create_route_map("A", 40.7128, -74.0060, 'red'), height=500)
        
        with col2:
            st.markdown(f"<div style='background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%); padding: 18px; border-radius: 14px; color: white; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(0,212,255,0.3);'><b>📍 Route B</b> • <b>{route_b['time']}min</b> • 🛡️ <b>{score_b}/10</b></div>", unsafe_allow_html=True)
            st_folium(create_route_map("B", 40.7589, -73.9851, 'blue'), height=500)
    
    with tab2:
        st.markdown("### 📊 Analytics")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_safety_chart(score_a, score_b), use_container_width=True)
        with col2:
            times_data = [{'name': 'A', 'time': route_a['time'], 'score': score_a}, {'name': 'B', 'time': route_b['time'], 'score': score_b}]
            fig = go.Figure()
            for d in times_data:
                fig.add_trace(go.Scatter(x=[d['time']], y=[d['score']], mode='markers', name=f"Route {d['name']}", marker=dict(size=40)))
            fig.update_layout(title="⚖️ Time vs Safety", xaxis_title="Time", yaxis_title="Safety", height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.plotly_chart(create_radar_chart(route_a, route_b), use_container_width=True)
    
    with tab3:
        st.markdown("### 🤖 AI Recommendation")
        if safer_route == "A":
            st.markdown(f"<div class='recommendation-safe'><h3>✅ Route A is Best</h3><p>{improvement:.1f}% Safer • {route_a['time']}min • Score: {score_a}/10</p></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='recommendation-safe'><h3>✅ Route B is Safer</h3><p>{improvement:.1f}% Safer • {route_b['time']}min • Score: {score_b}/10</p></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='background: #f0f4ff; border: 2px solid #667eea; padding: 25px; border-radius: 16px;'><h4 style='color: #667eea; margin-top: 0;'>Route A</h4><p><b>Safety:</b> {score_a}/10</p><p><b>Time:</b> {route_a['time']}m</p></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='background: #f0f4ff; border: 2px solid #667eea; padding: 25px; border-radius: 16px;'><h4 style='color: #667eea; margin-top: 0;'>Route B</h4><p><b>Safety:</b> {score_b}/10</p><p><b>Time:</b> {route_b['time']}m</p></div>", unsafe_allow_html=True)
        
        st.info(explanation)
    
    with tab4:
        st.markdown("### 📋 Detailed Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #667eea;'>Route A</h3>")
            st.metric("Safety", f"{score_a}/10")
            st.metric("Time", f"{route_a['time']}m")
            st.write(f"🚨 Crime: {route_a['crime_risk']:.1%}")
            st.progress(route_a['crime_risk'])
            st.write(f"💡 Lighting: {route_a['lighting_risk']:.1%}")
            st.progress(route_a['lighting_risk'])
            st.write(f"🏕️ Isolation: {route_a['isolation_risk']:.1%}")
            st.progress(route_a['isolation_risk'])
        
        with col2:
            st.markdown("<h3 style='color: #667eea;'>Route B</h3>")
            st.metric("Safety", f"{score_b}/10")
            st.metric("Time", f"{route_b['time']}m")
            st.write(f"🚨 Crime: {route_b['crime_risk']:.1%}")
            st.progress(route_b['crime_risk'])
            st.write(f"💡 Lighting: {route_b['lighting_risk']:.1%}")
            st.progress(route_b['lighting_risk'])
            st.write(f"🏕️ Isolation: {route_b['isolation_risk']:.1%}")
            st.progress(route_b['isolation_risk'])
    
    with tab5:
        st.markdown("### ❓ Help")
        with st.expander("What do scores mean?"):
            st.markdown("- **9-10:** Very Safe ✅\n- **7-8:** Safe ✓\n- **5-6:** Moderate ⚠️\n- **<5:** Risky ❌")
        
        with st.expander("How calculated?"):
            st.markdown("Crime (50%) + Lighting (30%) + Isolation (20%)")
        
        with st.expander("How to use?"):
            st.markdown("1. Set locations\n2. Choose time\n3. View results\n4. Compare\n5. Decide")
    
    st.divider()
    st.markdown("""
    <div class="footer">
        <h3 style="color: #667eea; margin: 0;">🗺️ SafeRoute Navigator</h3>
        <p>From <b>Fastest</b> → <b>Safest</b></p>
        <p style="font-size: 0.9rem;">© 2026 SafeRoute</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

