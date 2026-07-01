import yaml
# pyrefly: ignore [missing-import]
from google.genai import Client

class PolicyService:
    def is_action_safe(self, tool_name, args, role="itinerary_specialist"):
        # 1. Structural Check
        with open("policies.yaml", 'r') as f:
            config = yaml.safe_load(f)
        allowed = config['roles'].get(role, {}).get('allowed_tools', [])
        if tool_name not in allowed:
            return False
            
        # 2. Semantic Check (PII/Intent Alignment)
        client = Client(vertexai=True)
        prompt = f"Evaluate if this action violates PII policies or safety: {tool_name} with {args}"
        response = client.models.generate_content(model="gemini-3.1-pro", contents=prompt)
        return not response.text.strip().upper().startswith("VIOLATION")