import math
import json
import sys

def calculate_distance(lat1, lon1, lat2, lon2):
    """Deterministic Haversine formula to prevent LLM distance guessing."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def generate_hub_and_spoke_itinerary(pois, hotel_coords, days, base_radius=15, max_radius=40):
    """
    Clusters POIs relative to a fixed hotel 'hub'.
    Allocates closest spots to earlier days and expands radius if POI density is low.
    """
    # 1. Calculate distance of every POI from the hotel hub
    for poi in pois:
        poi['dist_from_hotel'] = calculate_distance(
            hotel_coords['lat'], hotel_coords['lng'],
            poi['coordinates']['lat'], poi['coordinates']['lng']
        )

    # 2. Filter by max allowed radius and sort by proximity
    valid_pois = [p for p in pois if p['dist_from_hotel'] <= max_radius]
    sorted_pois = sorted(valid_pois, key=lambda x: x['dist_from_hotel'])

    # 3. Distribute into daily clusters (3-4 POIs per day to respect meal/rest rules)
    itinerary = {}
    pois_per_day = 4 
    
    for d in range(1, days + 1):
        day_label = f"Day {d}"
        # Grab the next batch of closest POIs
        batch = sorted_pois[(d-1)*pois_per_day : d*pois_per_day]
        
        # Determine current day radius for the template
        current_radius = max([p['dist_from_hotel'] for p in batch]) if batch else 0
        
        itinerary[day_label] = {
            "cluster_radius": round(max(base_radius, current_radius), 2),
            "locations": batch
        }
        
    return itinerary

if __name__ == "__main__":
    # The agent passes POIs, Hotel Coords, and Duration via JSON
    try:
        data = json.loads(sys.stdin.read())
        result = generate_hub_and_spoke_itinerary(
            data['pois'], 
            data['staying_at']['coordinates'], 
            data['duration_days']
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))