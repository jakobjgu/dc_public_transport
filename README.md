# DC Metro Traffic Explorer (v2.0)

An interactive web application visualizing Washington, D.C. Metrorail station ridership (entries and exits) for May 2012. The app is deployed at [insightdatallc.com](https://insightdatallc.com) via an AWS-based stack.

---

## Table of Contents

* [Features](#features)
* [Live Demo](#live-demo)
* [Tech Stack](#tech-stack)
* [Architecture](#architecture)
* [Data Sources](#data-sources)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running Locally](#running-locally)
* [Deployment](#deployment)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* **Interactive network graph** of Metrorail stations, with nodes positioned by GPS coordinates.
* Toggle between **entry** and **exit** ridership data.
* Color‑coding by Metro line and hover tooltips with station details.
* Zoom & pan, and node sizing by passenger volumes.

---

## Live Demo

[https://insightdatallc.com](https://insightdatallc.com)

---

## Tech Stack

| Layer                                 | Technology                                                                                                                         |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Data Loading & Wrangling**          | Python · Pandas · NetworkX · DuckDB (local testing)                                                                                |
| **Data Warehousing & Transformation** | dbt · Snowflake                                                                                                                    |
| **Frontend**                          | React · React Router · React Bootstrap · react-force-graph-2d · D3-Geo                                                             |
| **Backend API**                       | Python · Flask · pickled NetworkX graph                                                                                            |
| **Hosting & Delivery**                | AWS S3 (static React build) · AWS Lambda + API Gateway (Flask endpoints) · AWS CloudFront (CDN & routing) · Route 53 DNS · ACM TLS |
| **Local Dev DB**                      | DuckDB (for preprocessing and local testing)                                                                                       |


---

## Architecture

```text
Client Browser
   │
   ▼
React Frontend (SPA)
   │  fetch('/graph/exits') or fetch('/graph/entries')
   ▼
Nginx Reverse Proxy ──► Flask API on port 5001
   │                          │
   ▼                          ▼
 Static build files         pickled NetworkX graph

```

---

## Data Sources

1. **Aggregated traffic (May 2012)**
   Public CSV download: [https://planitmetro.com/2012/10/31/data-download-metrorail-ridership-by-origin-and-destination/](https://planitmetro.com/2012/10/31/data-download-metrorail-ridership-by-origin-and-destination/)
2. **Station metadata & GPS**
   WMATA API: [https://developer.wmata.com/api-details#api=5476364f031f590f38092507\&operation=5476364f031f5909e4fe330c](https://developer.wmata.com/api-details#api=5476364f031f590f38092507&operation=5476364f031f5909e4fe330c)

All raw data is preprocessed into a NetworkX graph, serialized via `pickle`, and served by Flask.

---

## Getting Started

### Prerequisites

* Node.js >= 18 & npm >= 9
* Python >= 3.9
* Git

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/dc-metro-traffic-explorer.git
cd dc-metro-traffic-explorer

# Backend dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend dependencies
cd react_frontend
npm install
```

### Running Locally

```bash
# 1) Start Flask API
cd ../flask_api
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5001

# 2) Start React Dev Server
dd react_frontend
npm start
```

Then open [http://localhost:3000](http://localhost:3000).


---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

MIT © Insight Data LLC
