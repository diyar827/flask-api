import os
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app,
    version='1.0',
    title='VoltEdge API',
    description='Smart EV Charging Infrastructure API'
)

# Namespaces
chargers_ns = api.namespace('chargers', description='Ladestander operationer')
sessions_ns = api.namespace('sessions', description='Ladesession operationer')
billing_ns = api.namespace('billing', description='Afregning operationer')

# --- MODELLER (database tabeller) ---
class Charger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    status = db.Column(db.String(50))
    power_kw = db.Column(db.Float)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charger_id = db.Column(db.Integer, db.ForeignKey('charger.id'))
    user_id = db.Column(db.String(50))
    energy_kwh = db.Column(db.Float)
    status = db.Column(db.String(50))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10))
    status = db.Column(db.String(50))

# --- CHARGERS ---
@chargers_ns.route('/')
class ChargerList(Resource):
    def get(self):
        """Hent alle ladestandere"""
        chargers = Charger.query.all()
        return [{"id": c.id, "location": c.location, "status": c.status, "power_kw": c.power_kw} for c in chargers]

# --- SESSIONS ---
@sessions_ns.route('/')
class SessionList(Resource):
    def get(self):
        """Hent alle ladesessioner"""
        sessions = Session.query.all()
        return [{"id": s.id, "charger_id": s.charger_id, "user_id": s.user_id, "energy_kwh": s.energy_kwh, "status": s.status} for s in sessions]

# --- BILLING ---
@billing_ns.route('/')
class BillingList(Resource):
    def get(self):
        """Hent afregningsdata"""
        invoices = Invoice.query.all()
        return [{"id": i.id, "session_id": i.session_id, "amount": i.amount, "currency": i.currency, "status": i.status} for i in invoices]

# Opret tabeller og seed data
with app.app_context():
    db.create_all()
    if Charger.query.count() == 0:
        db.session.add_all([
            Charger(location="København N", status="available", power_kw=22),
            Charger(location="Aarhus C", status="occupied", power_kw=50),
        ])
        db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)