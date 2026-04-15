def calculate_safety_score(route):
    """
    Calculate safety score for a route using the formula:
    Safety Score = (1 - crime_risk) * 0.5 + (1 - lighting_risk) * 0.3 + (1 - isolation_risk) * 0.2
    
    Returns score out of 10.
    """
    crime_risk = route.get('crime_risk', 0)
    lighting_risk = route.get('lighting_risk', 0)
    isolation_risk = route.get('isolation_risk', 0)
    
    # Apply formula
    safety_score = (
        (1 - crime_risk) * 0.5 +
        (1 - lighting_risk) * 0.3 +
        (1 - isolation_risk) * 0.2
    )
    
    # Convert to 0-10 scale
    return round(safety_score * 10, 2)