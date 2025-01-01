## LEVANTA UN SERVIDOR WEB EN FLASK 
## PARA CONSUMIR UNA API REST DE ORACLE AUTONOMOUS DATABASE

## SE EJECUTA EN SEGUNDO PLANO EN UNA INSTANCIA DE ORACLE
## DEPLOY EN LA IP PÚBLICA DE LA INSTANCIA
## AUTORIZA LO QUE DURA EL TOKEN DE ACCESO
## SE RENUEVA DESDE OCI ALDB MODULO SEGURIDAD

from flask import Flask, render_template, request
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

app = Flask(__name__)

# Import credentials from a secure file
from oauth2creds import token_url, client_id, client_secret

# OAuth2 setup
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Fetch the token once (you may add a caching mechanism here)
token = oauth.fetch_token(token_url, client_id=client_id, client_secret=client_secret)
bearer_token = token['access_token']

# API Base URL
BASE_URL = "https://<alfanumérico>-<dirwebcloud>/ords/admin/busqclientapi/cust_id/"

@app.route("/", methods=["GET", "POST"])
def index():
    client_data = None
    error_message = None

    if request.method == "POST":
        client_id = request.form.get("client_id")
        url = f"{BASE_URL}{client_id}"

        try:
            response = requests.get(url, headers={'Authorization': f'Bearer {bearer_token}'})
            response.raise_for_status()
            data = response.json()

            if data.get("items"):
                client_data = data["items"][0]  # Get the first item
            else:
                error_message = "No data found for the provided client ID."

        except Exception as e:
            error_message = f"Error fetching data: {str(e)}"

    return render_template("index.html", client_data=client_data, error_message=error_message)

@app.route("/index.html")
def serve_html():
    # This will serve the index.html from the /var/www/html directory
    return send_from_directory('/var/www/html', 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
