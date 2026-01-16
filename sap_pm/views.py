from django.shortcuts import render
from core.services import SAPService # Wir importieren unsere Service-Klasse

def dashboard(request):
    # 1. Verbindung aufbauen
    sap = SAPService()
    
    # 2. Daten holen (Dein Code!)
    equipments_list = sap.get_equipments()
    
    # 3. An das Template übergeben
    # Das Dictionary {'equipments': ...} ist wichtig! 
    # Der Schlüssel 'equipments' ist der Name, den wir im HTML 
    # in der Schleife {% for item in equipments %} nutzen.
    context = {
        'equipments': equipments_list
    }
    
    return render(request, 'sap_pm/dashboard.html', context)