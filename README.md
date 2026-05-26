# VoltEdge API – Smart EV Charging Infrastructure

## Overblik
VoltEdge API er en cloud-baseret REST API løsning til håndtering af ladeinfrastruktur for elbiler. Løsningen er bygget med Flask og implementerer Domain-Driven Design principper med fokus på Predictive Maintenance og datadrevne services.

## Tech Stack
| Teknologi | Formål |
|-----------|--------|
| Python / Flask | API framework |
| Flask-RESTX / Swagger | API dokumentation |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Docker | Containerisering |
| GitHub Actions | CI/CD pipeline |
| Render | Cloud hosting |

## API Endpoints

### Chargers
- `GET /chargers/` – Hent alle ladestandere
- `POST /chargers/` – Opret ny ladestander

### Sessions
- `GET /sessions/` – Hent alle ladesessioner
- `POST /sessions/` – Opret ny ladesession

### Billing
- `GET /billing/` – Hent afregningsdata
- `POST /billing/` – Opret ny faktura

### Analytics
- `GET /analytics/summary` – Hent analytics oversigt
- `GET /analytics/export/chargers` – Eksporter ladestandere som CSV
- `GET /analytics/export/sessions` – Eksporter sessioner som CSV
- `GET /analytics/export/billing` – Eksporter billing som CSV
- `GET /analytics/export/telemetry` – Eksporter telemetri som CSV

### Telemetry
- `GET /telemetry/{charger_id}` – Hent realtids telemetri for en ladestander

### Maintenance (Predictive Maintenance)
- `GET /maintenance/anomaly/{charger_id}` – Detektér anomalier og health score

## Domain-Driven Design
Løsningen er struktureret omkring følgende bounded contexts:
- **Charging & Session Management** – håndtering af ladesessioner
- **Billing & Settlement** – afregning og fakturering
- **Data & Analytics** – datadrevne services og analyse
- **Predictive Maintenance** – anomaly detection og vedligeholdelse

## Kom i gang lokalt

### Forudsætninger
- Python 3.11
- PostgreSQL database

### Installation
```bash
git clone https://github.com/diyar827/flask-api.git
cd flask-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Konfiguration
Opret en `.env` fil:

### Start API
```bash
flask run
```

### Kør tests
```bash
pytest test_app.py -v
```

### Docker
```bash
docker build -t voltedge-api .
docker run -p 5001:10000 -e DATABASE_URL=postgresql://voltedge_db_su9j_user:slk7DQZxvZ21SDzEQVODg3C8sgc4QfHa@dpg-d872l9ojo89c73b5t4dg-a.oregon-postgres.render.com/voltedge_db_su9j voltedge-api
```

## CI/CD
Projektet bruger GitHub Actions til automatisk test og deployment:
- Ved hvert push til `main` køres alle unit tests
- Render deployer automatisk ved godkendt build

## Live URL
https://flask-api-c5qd.onrender.com

## Swagger UI
API dokumentation er tilgængelig på:
https://flask-api-c5qd.onrender.com