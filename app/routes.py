import json
import os


def get_routes():
    """Load routes from JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'routes.json')
    
    with open(file_path, 'r') as f:
        routes = json.load(f)
    
    return routes


def get_route_by_name(route_name):
    """Get a specific route by name."""
    routes = get_routes()
    for route in routes:
        if route['route'] == route_name:
            return route
    return None