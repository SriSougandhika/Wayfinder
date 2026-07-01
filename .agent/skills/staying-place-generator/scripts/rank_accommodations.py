import json
import sys

def rank_hotels(hotels):
    """
    Sorts hotels by rating (descending) and price level.
    Ensures a varied selection for the user.
    """
    # Sort by rating first, then by price level to provide variety
    sorted_hotels = sorted(
        hotels, 
        key=lambda x: (x.get('rating', 0), -x.get('price_level', 0)), 
        reverse=True
    )
    return sorted_hotels[:5]

if __name__ == "__main__":
    # In the Factory Model, scripts read from stdin or a temp file
    try:
        raw_input = sys.stdin.read()
        data = json.loads(raw_input)
        
        # Expecting a list of hotel objects from MCP
        top_5 = rank_hotels(data)
        print(json.dumps(top_5, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"Ranking failed: {str(e)}"}))