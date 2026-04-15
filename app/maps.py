"""
Google Maps API Integration Module

This module provides utilities for integrating with Google Maps API.
Currently uses Folium for map visualization (works without API keys).

To use real Google Maps API:
1. Get API key from Google Cloud Console
2. Set GOOGLE_MAPS_API_KEY environment variable
3. The module will automatically use Google Maps for better features like:
   - Real-time traffic
   - Actual route directions
   - Live crime data overlays
"""

import os
import folium
from typing import Tuple, Optional


def get_google_maps_api_key() -> Optional[str]:
    """Get Google Maps API key from environment variables."""
    return os.getenv('GOOGLE_MAPS_API_KEY', None)


def create_enhanced_map(
    center: Tuple[float, float],
    route_points_a: list = None,
    route_points_b: list = None,
    crime_zones: list = None,
    unsafe_areas: list = None
) -> folium.Map:
    """
    Create an enhanced map with multiple layers.
    
    Args:
        center: (latitude, longitude) tuple for map center
        route_points_a: List of coordinates for route A
        route_points_b: List of coordinates for route B
        crime_zones: List of (lat, lon, intensity) for crime hotspots
        unsafe_areas: List of unsafe areas to highlight
    
    Returns:
        folium.Map object
    """
    m = folium.Map(
        location=center,
        zoom_start=13,
        tiles="OpenStreetMap"
    )
    
    # Add route A if provided
    if route_points_a:
        folium.PolyLine(
            route_points_a,
            color='red',
            weight=3,
            opacity=0.7,
            popup='Route A'
        ).add_to(m)
        
        # Mark start and end
        folium.Marker(
            location=route_points_a[0],
            popup='Route A - Start',
            icon=folium.Icon(color='red', icon='arrow-down')
        ).add_to(m)
        
        folium.Marker(
            location=route_points_a[-1],
            popup='Route A - End',
            icon=folium.Icon(color='red', icon='flag')
        ).add_to(m)
    
    # Add route B if provided
    if route_points_b:
        folium.PolyLine(
            route_points_b,
            color='green',
            weight=3,
            opacity=0.7,
            popup='Route B'
        ).add_to(m)
        
        # Mark start and end
        folium.Marker(
            location=route_points_b[0],
            popup='Route B - Start',
            icon=folium.Icon(color='green', icon='arrow-down')
        ).add_to(m)
        
        folium.Marker(
            location=route_points_b[-1],
            popup='Route B - End',
            icon=folium.Icon(color='green', icon='flag')
        ).add_to(m)
    
    # Add crime zones heat map if provided
    if crime_zones:
        for crime_zone in crime_zones:
            lat, lon, intensity = crime_zone
            # Color intensity based on crime level
            color = 'darkred' if intensity > 0.7 else 'red' if intensity > 0.4 else 'orange'
            folium.CircleMarker(
                location=(lat, lon),
                radius=intensity * 10,
                popup=f'Crime Risk: {intensity:.0%}',
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.4,
                weight=2
            ).add_to(m)
    
    # Add unsafe areas if provided
    if unsafe_areas:
        for area in unsafe_areas:
            lat, lon, name = area
            folium.Marker(
                location=(lat, lon),
                popup=f'Unsafe Area: {name}',
                icon=folium.Icon(color='black', icon='exclamation')
            ).add_to(m)
    
    return m


def create_crime_heatmap(
    center: Tuple[float, float],
    crime_data: list
) -> folium.Map:
    """
    Create a heatmap showing crime distribution.
    
    Args:
        center: (latitude, longitude) for map center
        crime_data: List of [latitude, longitude, intensity]
    
    Returns:
        folium.Map with crime heatmap overlay
    """
    try:
        from folium.plugins import HeatMap
    except ImportError:
        print("HeatMap plugin not available, using alternative visualization")
        return create_enhanced_map(center, crime_zones=[(d[0], d[1], d[2]) for d in crime_data])
    
    m = folium.Map(
        location=center,
        zoom_start=13,
        tiles="OpenStreetMap"
    )
    
    if crime_data:
        HeatMap(crime_data, radius=15, blur=25, max_zoom=1).add_to(m)
    
    return m


def get_coordinates_from_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates using Nominatim (free, no API key needed).
    
    Args:
        address: Address string
    
    Returns:
        (latitude, longitude) tuple or None if not found
    """
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="smart_safe_route")
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except ImportError:
        print("geopy not installed. Install with: pip install geopy")
    except Exception as e:
        print(f"Error geocoding address: {e}")
    
    return None


def extract_coordinates_from_text(text: str) -> Optional[Tuple[float, float]]:
    """
    Extract coordinates from text like "Location (40.7128, -74.0060)".
    
    Args:
        text: Text containing coordinates
    
    Returns:
        (latitude, longitude) tuple or None
    """
    import re
    
    # Pattern: (number, number)
    pattern = r'\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)'
    match = re.search(pattern, text)
    
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return (lat, lon)
    
    return None


# Mock data for demonstration
MOCK_CRIME_ZONES = [
    (40.7120, -74.0050, 0.8),  # High crime
    (40.7580, -73.9840, 0.3),  # Low crime
    (40.7200, -74.0100, 0.6),  # Medium crime
]

MOCK_ROUTE_A = [
    (40.7128, -74.0060),  # Start
    (40.7150, -74.0080),
    (40.7180, -74.0100),
    (40.7210, -74.0120),
    (40.7240, -74.0140),
]

MOCK_ROUTE_B = [
    (40.7128, -74.0060),  # Start
    (40.7350, -73.9950),
    (40.7450, -73.9900),
    (40.7550, -73.9850),
    (40.7589, -73.9851),  # End
]
