def generate_explanation(route_a, route_b, score_a, score_b):
    """
    Generate AI explanation comparing two routes.
    
    Args:
        route_a: dict with route A data
        route_b: dict with route B data
        score_a: safety score for route A
        score_b: safety score for route B
    
    Returns:
        str with explanation
    """
    # Determine safer route
    if score_b > score_a:
        safer_route = "Route B"
        faster_route = "Route A" if route_a['time'] < route_b['time'] else "Route B"
        
        # Build explanation based on risk analysis
        explanations = []
        
        # Crime risk analysis
        if route_b['crime_risk'] < route_a['crime_risk']:
            explanations.append("avoids high-crime zones")
        
        # Lighting risk analysis
        if route_b['lighting_risk'] < route_a['lighting_risk']:
            explanations.append("travels through better-lit areas")
        
        # Isolation risk analysis
        if route_b['isolation_risk'] < route_a['isolation_risk']:
            explanations.append("avoids isolated roads")
        
        explanation_text = ", ".join(explanations) if explanations else "has better overall safety metrics"
        
        return f"Route B is recommended. This route {explanation_text}. While it takes {route_b['time'] - route_a['time']} more minutes, your safety is prioritized."
    else:
        safer_route = "Route A"
        
        explanations = []
        
        if route_a['crime_risk'] < route_b['crime_risk']:
            explanations.append("avoids high-crime zones")
        
        if route_a['lighting_risk'] < route_b['lighting_risk']:
            explanations.append("travels through better-lit areas")
        
        if route_a['isolation_risk'] < route_b['isolation_risk']:
            explanations.append("avoids isolated roads")
        
        explanation_text = ", ".join(explanations) if explanations else "has better overall safety metrics"
        
        return f"Route A is recommended. This route {explanation_text}."