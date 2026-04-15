from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple
from fastapi.responses import FileResponse
import os

from app.routes import get_routes
from app.safety import calculate_safety_score
from app.utils import adjust_risk_by_time
from app.ai import generate_explanation
from app.maps import (
    create_enhanced_map, 
    create_crime_heatmap,
    MOCK_ROUTE_A,
    MOCK_ROUTE_B,
    MOCK_CRIME_ZONES
)


app = FastAPI(
    title="Smart Safe Route Advisor",
    description="AI-powered route advisor that prioritizes safety over speed",
    version="1.0.0"
)


class AnalyzeRequest(BaseModel):
    source: str
    destination: str
    time_of_day: str = "Day"


class RouteAnalysis(BaseModel):
    route_a: Dict[str, Any]
    route_b: Dict[str, Any]
    score_a: float
    score_b: float
    recommendation: str
    explanation: str


@app.get("/")
def read_root():
    return {"message": "Smart Safe Route Advisor API"}


@app.post("/analyze", response_model=RouteAnalysis)
def analyze_routes(request: AnalyzeRequest):
    """Analyze routes and recommend the safest option."""
    
    # Load routes
    raw_routes = get_routes()
    
    # Adjust risks based on time of day
    route_a = adjust_risk_by_time(raw_routes[0], request.time_of_day)
    route_b = adjust_risk_by_time(raw_routes[1], request.time_of_day)
    
    # Calculate safety scores
    score_a = calculate_safety_score(route_a)
    score_b = calculate_safety_score(route_b)
    
    # Generate explanation
    explanation = generate_explanation(route_a, route_b, score_a, score_b)
    
    # Determine recommendation
    if score_b > score_a:
        recommendation = "Route B (Safer)"
    else:
        recommendation = "Route A (Safer)"
    
    return RouteAnalysis(
        route_a=route_a,
        route_b=route_b,
        score_a=score_a,
        score_b=score_b,
        recommendation=recommendation,
        explanation=explanation
    )


@app.get("/map/routes")
def get_routes_map():
    """Get interactive map showing both routes."""
    try:
        # Create map centered between routes
        center = (40.735, -73.995)
        route_map = create_enhanced_map(
            center=center,
            route_points_a=MOCK_ROUTE_A,
            route_points_b=MOCK_ROUTE_B,
            crime_zones=MOCK_CRIME_ZONES
        )
        
        # Save to file
        map_file = "/tmp/routes_map.html"
        route_map.save(map_file)
        return FileResponse(map_file, media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating map: {str(e)}")


@app.get("/map/crime-heatmap")
def get_crime_heatmap():
    """Get crime heatmap visualization."""
    try:
        center = (40.735, -73.995)
        crime_map = create_crime_heatmap(
            center=center,
            crime_data=[[zone[0], zone[1], zone[2]] for zone in MOCK_CRIME_ZONES]
        )
        
        # Save to file
        map_file = "/tmp/crime_heatmap.html"
        crime_map.save(map_file)
        return FileResponse(map_file, media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating heatmap: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Smart Safe Route Advisor"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)