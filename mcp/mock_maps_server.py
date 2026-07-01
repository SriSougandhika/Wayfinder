# mcp/mock_maps_server.py
import sys
import json

MOCK_DATA = {
    "Paris": {
        "pois": [
            {"name": "Eiffel Tower", "coordinates": {"lat": 48.8584, "lng": 2.2945}, "rating": 4.7},
            {"name": "Louvre Museum", "coordinates": {"lat": 48.8606, "lng": 2.3376}, "rating": 4.8},
            {"name": "Notre-Dame", "coordinates": {"lat": 48.8530, "lng": 2.3499}, "rating": 4.7},
            {"name": "Sacré-Cœur", "coordinates": {"lat": 48.8867, "lng": 2.3431}, "rating": 4.6},
            {"name": "Arc de Triomphe", "coordinates": {"lat": 48.8738, "lng": 2.2950}, "rating": 4.7},
            {"name": "Musée d'Orsay", "coordinates": {"lat": 48.8599, "lng": 2.3266}, "rating": 4.8},
            {"name": "Luxembourg Gardens", "coordinates": {"lat": 48.8462, "lng": 2.3371}, "rating": 4.7},
            {"name": "Sainte-Chapelle", "coordinates": {"lat": 48.8554, "lng": 2.3450}, "rating": 4.8}
        ],
        "hotels": [
            {"name": "Hotel de Crillon", "coordinates": {"lat": 48.8672, "lng": 2.3214}, "price_level": 4, "rating": 4.8, "description": "Ultra-luxury 5-star palace hotel overlooking Place de la Concorde."},
            {"name": "Hotel Regina Louvre", "coordinates": {"lat": 48.8628, "lng": 2.3323}, "price_level": 3, "rating": 4.6, "description": "Elegant 4-star boutique hotel near the Louvre Museum."},
            {"name": "Hotel Paris Avenue 3", "coordinates": {"lat": 48.8566, "lng": 2.3522}, "price_level": 3, "rating": 4.5, "description": "Modern hotel in the heart of Paris near the Marais."},
            {"name": "Hotel Caron de Beaumarchais", "coordinates": {"lat": 48.8575, "lng": 2.3565}, "price_level": 2, "rating": 4.4, "description": "Charming 18th-century themed boutique hotel in the Marais."},
            {"name": "Generator Paris", "coordinates": {"lat": 48.8789, "lng": 2.3698}, "price_level": 1, "rating": 4.2, "description": "Stylish, budget-friendly design hostel in the 10th Arrondissement."}
        ]
    },
    "Lyon": {
        "pois": [
            {"name": "Basilique Notre-Dame de Fourvière", "coordinates": {"lat": 45.7622, "lng": 4.8226}, "rating": 4.8},
            {"name": "Parc de la Tête d'Or", "coordinates": {"lat": 45.7772, "lng": 4.8556}, "rating": 4.6},
            {"name": "Vieux Lyon", "coordinates": {"lat": 45.7625, "lng": 4.8275}, "rating": 4.7},
            {"name": "Place des Terreaux", "coordinates": {"lat": 45.7674, "lng": 4.8335}, "rating": 4.5},
            {"name": "Musée des Confluences", "coordinates": {"lat": 45.7336, "lng": 4.8180}, "rating": 4.6},
            {"name": "Cathedral Saint-Jean-Baptiste", "coordinates": {"lat": 45.7608, "lng": 4.8273}, "rating": 4.7},
            {"name": "Théâtre Gallo Romain", "coordinates": {"lat": 45.7597, "lng": 4.8197}, "rating": 4.8},
            {"name": "Les Halles Paul Bocuse", "coordinates": {"lat": 45.7623, "lng": 4.8510}, "rating": 4.7}
        ],
        "hotels": [
            {"name": "Villa Florentine", "coordinates": {"lat": 45.7628, "lng": 4.8220}, "price_level": 4, "rating": 4.7, "description": "5-star luxury hotel in Vieux Lyon with a heated panoramic pool and fine dining."},
            {"name": "Hotel Le Royal Lyon", "coordinates": {"lat": 45.7570, "lng": 4.8320}, "price_level": 3, "rating": 4.6, "description": "Elegant boutique hotel overlooking Bellecour Square, blending classic style with modern comfort."},
            {"name": "Courtyard Lyon", "coordinates": {"lat": 45.7600, "lng": 4.8500}, "price_level": 2, "rating": 4.4, "description": "Modern mid-range hotel offering comfortable rooms, close to Les Halles Paul Bocuse."},
            {"name": "Hotel Silky by HappyCulture", "coordinates": {"lat": 45.7635, "lng": 4.8340}, "price_level": 1, "rating": 4.3, "description": "Chic, budget-friendly hotel set in a historical building in the Presqu'île district."},
            {"name": "Radisson Blu Hotel Lyon", "coordinates": {"lat": 45.7615, "lng": 4.8570}, "price_level": 3, "rating": 4.2, "description": "Upscale accommodation in the Part-Dieu tower featuring spectacular city views."}
        ]
    }
}

def get_data(city):
    return MOCK_DATA.get(city, {"error": "City not found"})

if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        print(json.dumps(get_data(input_data.get("city", "Paris"))))
    except Exception as e:
        print(json.dumps({"error": str(e)}))