import os
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from .mocks import MockSAPClient

class SAPService:
    def __init__(self):
        # Wir laden die Konfiguration
        self.use_mock = os.getenv('USE_MOCK_SAP') == 'True'
        self.base_url = os.getenv('SAP_BASE_URL')
        self.auth = HTTPBasicAuth(
            os.getenv('SAP_USER'), 
            os.getenv('SAP_PASSWORD')
        )
        
        # Wenn Mock aktiv ist, laden wir die Klasse aus mocks.py
        if self.use_mock:
            self.client = MockSAPClient()
        else:
            self.client = None # Wird bei echten Requests initialisiert

    def get_equipments(self):
        """
        Holt die Liste aller Equipments.
        Unterscheidet automatisch zwischen Mock und Echt.
        """
        if self.use_mock:
            return self.client.get_equipments()
        
        # --- ECHTE SAP LOGIK ---
        endpoint = f"{self.base_url}API_EQUIPMENT/Equipment"
        
        # OData Parameter für Performance (nur nötige Felder)
        params = {
            "$format": "json",
            "$top": 50,
            "$select": "Equipment,EquipmentName,MaintenancePlant,SystemStatus,FunctionalLocation"
        }

        try:
            response = requests.get(endpoint, auth=self.auth, params=params, timeout=10)
            response.raise_for_status() # Wirft Fehler bei 401, 404, 500
            
            # OData liefert Daten oft verschachtelt in ['d']['results']
            data = response.json()
            return data.get('d', {}).get('results', [])
            
        except requests.exceptions.RequestException as e:
            print(f"SAP Connection Error: {e}")
            return [] # Oder Fehler weiterwerfen, je nach Strategie

    def create_order(self, equipment_id, text, plant):
        """
        Legt einen Auftrag in SAP an.
        """
        if self.use_mock:
            return self.client.create_order({
                "Equipment": equipment_id, 
                "OrderDescription": text
            })

        # --- ECHTE SAP LOGIK ---
        # 1. CSRF Token holen (Pflicht bei SAP POSTs!)
        # Später eher komplex
        pass
