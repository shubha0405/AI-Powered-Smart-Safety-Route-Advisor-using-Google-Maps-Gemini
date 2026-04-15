def adjust_risk_by_time(route, time_of_day):
    """
    Adjust route risks based on time of day.
    
    Args:
        route: dict with risk values
        time_of_day: str ('Day' or 'Night')
    
    Returns:
        dict with adjusted risks
    """
    adjusted_route = route.copy()
    
    if time_of_day.lower() == 'night':
        # Increase all risks by 0.1, capped at 1.0
        adjusted_route['crime_risk'] = min(route['crime_risk'] + 0.1, 1.0)
        adjusted_route['lighting_risk'] = min(route['lighting_risk'] + 0.1, 1.0)
        adjusted_route['isolation_risk'] = min(route['isolation_risk'] + 0.1, 1.0)
    else:
        # Day - no change
        pass
    
    return adjusted_route