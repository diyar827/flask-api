import os
import csv
import io
import random
from datetime import datetime
from flask import Flask, make_response
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
analytics_ns = api.namespace('analytics', description='Data analyse operationer')
telemetry_ns = api.namespace('telemetry', description='Realtids telemetri fra ladestandere')

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
charger_model = api.model('Charger', {
    'location': fields.String(required=True, description='Placering'),
    'status': fields.String(required=True, description='Status'),
    'power_kw': fields.Float(required=True, description='Effekt i kW')
})

@chargers_ns.route('/')
class ChargerList(Resource):
    def get(self):
        """Hent alle ladestandere"""
        chargers = Charger.query.all()
        return [{"id": c.id, "location": c.location, "status": c.status, "power_kw": c.power_kw} for c in chargers]

    @chargers_ns.expect(charger_model)
    def post(self):
        """Opret ny ladestander"""
        data = api.payload
        charger = Charger(location=data['location'], status=data['status'], power_kw=data['power_kw'])
        db.session.add(charger)
        db.session.commit()
        return {"message": "Ladestander oprettet", "id": charger.id}, 201

# --- SESSIONS ---
session_model = api.model('Session', {
    'charger_id': fields.Integer(required=True, description='Ladestander ID'),
    'user_id': fields.String(required=True, description='Bruger ID'),
    'energy_kwh': fields.Float(required=True, description='Energi i kWh'),
    'status': fields.String(required=True, description='Status')
})

@sessions_ns.route('/')
class SessionList(Resource):
    def get(self):
        """Hent alle ladesessioner"""
        sessions = Session.query.all()
        return [{"id": s.id, "charger_id": s.charger_id, "user_id": s.user_id, "energy_kwh": s.energy_kwh, "status": s.status} for s in sessions]

    @sessions_ns.expect(session_model)
    def post(self):
        """Opret ny ladesession"""
        data = api.payload
        session = Session(charger_id=data['charger_id'], user_id=data['user_id'], energy_kwh=data['energy_kwh'], status=data['status'])
        db.session.add(session)
        db.session.commit()
        return {"message": "Session oprettet", "id": session.id}, 201

# --- BILLING ---
invoice_model = api.model('Invoice', {
    'session_id': fields.Integer(required=True, description='Session ID'),
    'amount': fields.Float(required=True, description='Beløb'),
    'currency': fields.String(required=True, description='Valuta'),
    'status': fields.String(required=True, description='Status')
})

@billing_ns.route('/')
class BillingList(Resource):
    def get(self):
        """Hent afregningsdata"""
        invoices = Invoice.query.all()
        return [{"id": i.id, "session_id": i.session_id, "amount": i.amount, "currency": i.currency, "status": i.status} for i in invoices]

    @billing_ns.expect(invoice_model)
    def post(self):
        """Opret ny faktura"""
        data = api.payload
        invoice = Invoice(session_id=data['session_id'], amount=data['amount'], currency=data['currency'], status=data['status'])
        db.session.add(invoice)
        db.session.commit()
        return {"message": "Faktura oprettet", "id": invoice.id}, 201
    
    # --- ANALYTICS ---
@analytics_ns.route('/summary')
class AnalyticsSummary(Resource):
    def get(self):
        """Hent analytics oversigt over ladesessioner"""
        total_sessions = Session.query.count()
        total_energy = db.session.query(db.func.sum(Session.energy_kwh)).scalar() or 0
        avg_energy = db.session.query(db.func.avg(Session.energy_kwh)).scalar() or 0
        active_sessions = Session.query.filter_by(status='active').count()
        available_chargers = Charger.query.filter_by(status='available').count()

        return {
            "total_sessions": total_sessions,
            "total_energy_kwh": round(float(total_energy), 2),
            "avg_energy_per_session_kwh": round(float(avg_energy), 2),
            "active_sessions": active_sessions,
            "available_chargers": available_chargers
        }
    
    # --- TELEMETRY ---
@telemetry_ns.route('/<int:charger_id>')
class ChargerTelemetry(Resource):
    def get(self, charger_id):
        """Hent realtids telemetri for en ladestander"""
        charger = Charger.query.get_or_404(charger_id)
        return {
            "charger_id": charger_id,
            "location": charger.location,
            "timestamp": datetime.utcnow().isoformat(),
            "power_kw": round(random.uniform(0, charger.power_kw), 2),
            "voltage": round(random.uniform(220, 240), 1),
            "current_amp": round(random.uniform(10, 32), 1),
            "status": charger.status,
            "uptime_pct": round(random.uniform(95, 100), 2)
        }

# --- CSV EXPORT ---
@analytics_ns.route('/export/chargers')
class ExportChargers(Resource):
    def get(self):
        """Eksporter ladestandere som CSV"""
        chargers = Charger.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'location', 'status', 'power_kw'])
        for c in chargers:
            writer.writerow([c.id, c.location, c.status, c.power_kw])
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=chargers.csv'
        return response

@analytics_ns.route('/export/sessions')
class ExportSessions(Resource):
    def get(self):
        """Eksporter sessioner som CSV"""
        sessions = Session.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'charger_id', 'user_id', 'energy_kwh', 'status'])
        for s in sessions:
            writer.writerow([s.id, s.charger_id, s.user_id, s.energy_kwh, s.status])
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=sessions.csv'
        return response

@analytics_ns.route('/export/billing')
class ExportBilling(Resource):
    def get(self):
        """Eksporter billing som CSV"""
        invoices = Invoice.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'session_id', 'amount', 'currency', 'status'])
        for i in invoices:
            writer.writerow([i.id, i.session_id, i.amount, i.currency, i.status])
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=billing.csv'
        return response

@analytics_ns.route('/export/telemetry')
class ExportTelemetry(Resource):
    def get(self):
        """Eksporter telemetri som CSV"""
        chargers = Charger.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['charger_id', 'location', 'timestamp', 'power_kw', 'voltage', 'current_amp', 'status', 'uptime_pct'])
        for c in chargers:
            writer.writerow([c.id, c.location, datetime.utcnow().isoformat(), round(random.uniform(0, c.power_kw), 2), round(random.uniform(220, 240), 1), round(random.uniform(10, 32), 1), c.status, round(random.uniform(95, 100), 2)])
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=telemetry.csv'
        return response

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