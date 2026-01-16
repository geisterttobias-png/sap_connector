class MockSAPClient:
    """
    Simuliert die Antworten des echten SAP Systems.
    Gibt statische Daten zurück, damit wir Frontend & Logik testen können.
    """
    
    def get_equipments(self):
        # Das hier ist die Struktur, die S/4HANA OData liefert ('d' -> 'results')
        return [
            {
                "Equipment": "10000001",
                "EquipmentName": "Hydraulikpumpe H-101",
                "MaintenancePlant": "1000",
                "SystemStatus": "REL", # Released / Freigegeben
                "FunctionalLocation": "Halle-A-Nord",
                "Manufacturer": "Siemens"
            },
            {
                "Equipment": "10000002",
                "EquipmentName": "Förderband F-200",
                "MaintenancePlant": "2000", # Anderes Werk (zum Testen der Rechte!)
                "SystemStatus": "REL",
                "FunctionalLocation": "Halle-B-Sued",
                "Manufacturer": "Bosch"
            },
            {
                "Equipment": "10000003",
                "EquipmentName": "Notstromaggregat (DEFEKT)",
                "MaintenancePlant": "1000",
                "SystemStatus": "LOCKED", # Gesperrt
                "FunctionalLocation": "Keller",
                "Manufacturer": "CAT"
            }
        ]

    def create_order(self, order_data):
        # Simuliert einen erfolgreichen POST Request
        return {
            "MaintenanceOrder": "4000123456", # Simulierte Auftragsnummer
            "OrderDescription": order_data.get("OrderDescription"),
            "SystemStatus": "CRTD" # Created
        }
    def get_equipment_detail(self, equipment_id):  # holt einzelne Equipment Details
        all_data = self.get_equipments()
        for item in all_data:
            if item['Equipment'] == equipment_id:
                return item
        return None
