import os
import re

def resolve_context(template_str, override_state=None):
    """Replaces [[VARIABLE_NAME]] with values from state or environment."""
    state = override_state or {}
    def replacement(match):
        var_name = match.group(1).strip()
        return str(state.get(var_name, os.environ.get(var_name, match.group(0))))
    
    return re.sub(r'\[\[([^\]]+)\]\]', replacement, template_str)