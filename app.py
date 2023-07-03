import requests
from flask import Flask, render_template

app = Flask(__name__)

class AmbulanceRequest:
    def __init__(self, location, time):
        self.location = location
        self.time = time

class Hospital:
    def __init__(self, name, location, availability):
        self.name = name
        self.location = location
        self.availability = availability

ambulance_requests = []
hospitals = []

# Rota para exibir a interface gráfica
@app.route("/")
def index():
    return render_template("index.html", ambulance_requests=ambulance_requests, hospitals=hospitals)

# Rota para receber novas solicitações de ambulância
@app.route("/add_request", methods=["POST"])
def add_request():
    location = request.form["location"]
    time = request.form["time"]
    request = AmbulanceRequest(location, time)
    ambulance_requests.append(request)
    notify_hospitals(request)
    return redirect("/")

# Função para notificar os hospitais sobre a nova solicitação de ambulância
def notify_hospitals(request):
    orion_url = "http://localhost:1026/"
    headers = {
        "Content-Type": "application/json",
    }

    for hospital in hospitals:
        entity_data = {
            "id": hospital.name.replace(" ", "_"),
            "type": "Hospital",
            "location": {"type": "Point", "coordinates": hospital.location},
            "availability": hospital.availability,
            "ambulance_location": {"type": "Point", "coordinates": request.location}
        }

        response = requests.post(orion_url + "v2/entities", json=entity_data, headers=headers)
        if response.status_code == 201:
            print("Dados atualizados para o hospital:", hospital.name)
        else:
            print("Falha ao atualizar dados para o hospital:", hospital.name)

if __name__ == "__main__":
    app.run()
