from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, 
    version='1.0', 
    title='VoltEdge API',
    description='Smart EV Charging Infrastructure API'
)

# Namespaces (svarer til domæner)
chargers_ns = api.namespace('chargers', description='Ladestander operationer')
sessions_ns = api.namespace('sessions', description='Ladesession operationer')
billing_ns = api.namespace('billing', description='Afregning operationer')

# --- CHARGERS ---
@chargers_ns.route('/')
class ChargerList(Resource):
    def get(self):
        """Hent alle ladestandere"""
        return [
            {"id": 1, "location": "København N", "status": "available", "power_kw": 22},
            {"id": 2, "location": "Aarhus C", "status": "occupied", "power_kw": 50},
        ]

# --- SESSIONS ---
@sessions_ns.route('/')
class SessionList(Resource):
    def get(self):
        """Hent alle ladesessioner"""
        return [
            {"sessionId": "S001", "chargerId": 1, "userId": "U123", "energyKwh": 15.4, "status": "completed"},
            {"sessionId": "S002", "chargerId": 2, "userId": "U456", "energyKwh": 8.2, "status": "active"},
        ]

# --- BILLING ---
@billing_ns.route('/')
class BillingList(Resource):
    def get(self):
        """Hent afregningsdata"""
        return [
            {"invoiceId": "INV001", "sessionId": "S001", "amount": 45.50, "currency": "DKK", "status": "paid"},
        ]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)