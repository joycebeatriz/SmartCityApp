import requests

class NotificationService:
    def __init__(self):
        self.subscription_id = None
    
    def create_subscription(self):
        orion_url = "http://localhost:1026/"
        subscription_data = {
            "description": "AmbulanceRequest subscription",
            "subject": {
                "entities": [{"idPattern": ".*", "type": "AmbulanceRequest"}],
                "condition": {"attrs": ["availability"]}
            },
            "notification": {
                "http": {
                    "url": "http://localhost:8000/notify"  # Endpoint para receber as notificações do Orion
                },
                "attrs": ["availability"]
            }
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(orion_url + "v2/subscriptions", json=subscription_data, headers=headers)
        if response.status_code == 201:
            subscription_id = response.headers.get("Location").split("/")[-1]
            self.subscription_id = subscription_id
            print("Assinatura criada com sucesso. ID:", subscription_id)
        else:
            print("Falha ao criar assinatura.")

    def notify_hospitals(self):
        if self.subscription_id:
            # Lógica para notificar os hospitais
            print("Notificando hospitais sobre nova solicitação de ambulância...")
        else:
            print("Assinatura não criada. Não é possível notificar os hospitais.")

# Exemplo de uso
notification_service = NotificationService()

# Criar a assinatura para receber notificações do Orion
notification_service.create_subscription()

# Notificar os hospitais sobre novas solicitações de ambulância
notification_service.notify_hospitals()
