# VoltEdge API – Smart EV Charging Infrastructure

## Overblik
VoltEdge API er en cloud-baseret REST API løsning til håndtering af ladeinfrastruktur for elbiler. Løsningen er bygget med Flask og implementerer Domain-Driven Design principper med fokus på Predictive Maintenance, Machine Learning og datadrevne services.

## Tech Stack
| Teknologi | Formål |
|-----------|--------|
| Python / Flask | API framework |
| Flask-RESTX / Swagger | API dokumentation |
| PostgreSQL (Render) | Database |
| SQLAlchemy | ORM |
| Docker | Containerisering |
| GitHub Actions | CI/CD pipeline |
| Render | Cloud hosting |
| Power BI | Business Intelligence dashboard |
| scikit-learn | Machine Learning (Linear Regression + Decision Tree) |

## Live URL
https://flask-api-c5qd.onrender.com

## Swagger UI
API dokumentation og test: https://flask-api-c5qd.onrender.com

## API Endpoints

### Chargers
- `GET /chargers/` – Hent alle ladestandere
- `POST /chargers/` – Opret ny ladestander
- `DELETE /chargers/{id}` – Slet en ladestander

### Sessions
- `GET /sessions/` – Hent alle ladesessioner
- `POST /sessions/` – Opret ny ladesession

### Billing
- `GET /billing/` – Hent afregningsdata
- `POST /billing/` – Opret ny faktura
- `DELETE /billing/{id}` – Slet en faktura

### Analytics
- `GET /analytics/summary` – Hent analytics oversigt
- `GET /analytics/export/chargers` – Eksporter ladestandere som CSV
- `GET /analytics/export/sessions` – Eksporter sessioner som CSV
- `GET /analytics/export/billing` – Eksporter billing som CSV
- `GET /analytics/export/telemetry` – Eksporter telemetri som CSV
- `GET /analytics/performance` – Hent performance statistik

### Telemetry
- `GET /telemetry/{charger_id}` – Hent realtids telemetri for en ladestander

### Maintenance (Predictive Maintenance)
- `GET /maintenance/anomaly/{charger_id}` – Detektér anomalier og health score

### Machine Learning
- `GET /ml/predict/energy` – Forudsig energiforbrug baseret på historiske sessioner (Linear Regression + Decision Tree)

## Domain-Driven Design
Løsningen er struktureret omkring følgende bounded contexts:
- **Charging & Session Management** – håndtering af ladesessioner
- **Billing & Settlement** – afregning og fakturering
- **Data & Analytics** – datadrevne services og analyse
- **Predictive Maintenance** – anomaly detection og vedligeholdelse
- **Machine Learning** – energiforudsigelse baseret på historiske data

## Kom i gang lokalt

### Forudsætninger
- Python 3.11
- PostgreSQL database
- Docker (valgfrit)

### Installation
```bash
git clone https://github.com/diyar827/flask-api.git
cd flask-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Konfiguration
nævnt i .env fil: 

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
docker run -p 5001:10000 -e DATABASE_URL=din_url voltedge-api
```

## CI/CD
Projektet bruger GitHub Actions til automatisk test og deployment:
- Ved hvert push til `main` køres alle 7 unit tests automatisk
- Render deployer automatisk ved godkendt build
- Tests dækker: chargers, sessions, billing, analytics, anomaly detection

## Business Intelligence
Power BI dashboard forbinder direkte til PostgreSQL databasen og visualiserer en række grafer der vil gøre det intuitivt at følge med i performance.

## Arkitektur
GitHub → GitHub Actions (CI/CD) → Render (Flask API) → PostgreSQL (Database)
↓
Power BI Dashboard
