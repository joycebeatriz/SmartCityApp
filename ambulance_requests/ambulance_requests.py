import requests
import random
import time

class AmbulanceRequests:
    def __init__(self):
        self.requests = []
    
    def add_request(self, request):
        self.requests.append(request)
    
    def get_requests(self):
        return self.requests

class Hospital:
    def __init__(self, name, location, availability):
        self.name = name
        self.location = location
        self.availability = availability

class AmbulanceRequest:
    def __init__(self, location, time):
        self.location = location
        self.time = time

# Exemplo de uso
ambulance_requests = AmbulanceRequests()

# Dados fictícios de solicitação de ambulância
requests_data = [
    {"location": "Localização A", "time": "09:00"},
    {"location": "Localização B", "time": "10:30"},
    {"location": "Localização C", "time": "12:15"}
]

# Criar instâncias de hospitais
hospital1 = Hospital("Hospital A", "Localização A", True)
hospital2 = Hospital("Hospital B", "Localização B", False)

# Adicionar solicitações de ambulância
ambulance_requests.add_request(hospital1)
ambulance_requests.add_request(hospital2)

# Obter todas as solicitações
all_requests = ambulance_requests.get_requests()
for request in all_requests:
    print("Hospital:", request.name)
    print("Localização:", request.location)
    print("Disponibilidade:", request.availability)
    print()

# Conectar-se ao Orion Context Broker
orion_url = "http://localhost:1026/"

# Criar entidades no Orion para representar as solicitações de ambulância
for request in all_requests:
    entity_data = {
        "id": request.name.replace(" ", "_"),
        "type": "AmbulanceRequest",
        "location": {"type": "Point", "coordinates": [0, 0]},  # Preencher com as coordenadas de localização da solicitação
        "availability": request.availability
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(orion_url + "v2/entities", json=entity_data, headers=headers)
    if response.status_code == 201:
        print("Entidade criada com sucesso:", request.name)
    else:
        print("Falha ao criar entidade:", request.name)

# Publicar os dados fictícios de solicitação de ambulância no Orion Context Broker
for request_data in requests_data:
    request = AmbulanceRequest(request_data["location"], request_data["time"])

    entity_data = {
        "id": str(random.randint(1, 100)),  # ID único para cada solicitação
        "type": "AmbulanceRequest",
        "location": request.location,
        "time": request.time
    }

    response = requests.post(orion_url + "v2/entities", json=entity_data)
    if response.status_code == 201:
        print("Dados de solicitação de ambulância publicados com sucesso:", entity_data)
    else:
        print("Falha ao publicar dados de solicitação de ambulância:", entity_data)

    time.sleep(1)  # Aguardar 1 segundo entre cada publicação