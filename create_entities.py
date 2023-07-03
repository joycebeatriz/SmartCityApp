import requests
from config import ORION_URL, HEADERS, AMBULANCE_ENTITY_ID, HOSPITAL_ENTITY_ID

def create_entities():
    # Criação da entidade de solicitação de ambulância
    ambulance_entity = {
        "id": AMBULANCE_ENTITY_ID,
        "type": "Ambulance",
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [0, 0]  # Defina as coordenadas desejadas para a localização da ambulância
            }
        }
    }
    create_entity(ambulance_entity)

    # Criação da entidade do hospital
    hospital_entity = {
        "id": HOSPITAL_ENTITY_ID,
        "type": "Hospital",
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [0, 0]  # Defina as coordenadas desejadas para a localização do hospital
            }
        },
        "availability": True  # Defina a disponibilidade do hospital conforme necessário
    }
    create_entity(hospital_entity)

def create_entity(entity):
    url = f"{ORION_URL}/entities/{entity['id']}/attrs"
    response = requests.post(url, json=entity, headers=HEADERS)

    if response.status_code == 201:
        print(f"Entidade {entity['id']} criada com sucesso!")
    else:
        print(f"Erro ao criar a entidade {entity['id']}: {response.status_code} {response.text}")

if __name__ == "__main__":
    create_entities()

def delete_entities():
    delete_entity(AMBULANCE_ENTITY_ID)
    delete_entity(HOSPITAL_ENTITY_ID)

def delete_entity(entity_id):
    url = f"{ORION_URL}/entities/{entity_id}"
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 204:
        print(f"Entidade {entity_id} removida com sucesso!")
    else:
        print(f"Erro ao remover a entidade {entity_id}: {response.status_code} {response.text}")

if __name__ == "__main__":
    delete_entities()
    create_entities()
