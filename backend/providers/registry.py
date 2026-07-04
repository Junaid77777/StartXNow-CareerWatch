import json
import importlib
from typing import Dict, Any
from providers.base import BaseProvider

from services.logging_service import providers_logger


def load_providers():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    providers = {}
    for company in config.get("companies", []):
        name = company["name"]
        module_name = company["module"]
        base_url = company["base_url"]
        
        try:
            module = importlib.import_module(module_name)
            provider_class = getattr(module, name.capitalize() + "Provider")
            providers[name] = provider_class(name=name, base_url=base_url)
            providers_logger.info(f"Loaded provider: {name}")
        except Exception as e:
            providers_logger.error(f"Failed to load provider {name}: {str(e)}")
    
    return providers