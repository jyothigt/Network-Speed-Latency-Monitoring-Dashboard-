# Network Speed & Latency Monitoring Dashboard

A real-time network monitoring dashboard built with Python and Flask.
Tracks speed, latency, and connection health — automatically classifies
network status and raises alert flags for unstable conditions.

## Features
- Real-time speed and latency monitoring with automated polling
- 3-tier status classification: **Stable** / **Degraded** / **Down**
- Alert flags triggered on unstable network conditions
- 500+ records stored and analysed in SQLite
- Visualisations using Matplotlib

## Tech Stack
`Python` `Flask` `SQLite` `Matplotlib` `HTML` `CSS`

## Screenshots
![Dashboard Screenshot 1](Screenshot%202026-05-22%20223526.png)
![Dashboard Screenshot 2](Screenshot%202026-05-22%20223541.png)

## Getting Started
```bash
git clone https://github.com/jyothigt/Network-Speed-Latency-Monitoring-Dashboard-.git
cd Network-Speed-Latency-Monitoring-Dashboard-
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 in your browser.

## Project Structure
```
app.py              # Main Flask app and polling logic
network_monitor.db  # SQLite database
requirements.txt    # Dependencies
```
