# 🚀 Quick Start Guide - Agent System

## Sofort loslegen (5 Minuten)

### 1. Installation ✅

```bash
# Bereits erledigt! Dependencies sind installiert:
pip install -r requirements.txt
```

### 2. Erstes Beispiel ausführen

```bash
# Vollständige Analyse der Beispieldaten
python cli.py example_data.csv
```

**Output:**
```
🤖 Data Analyst Agent MVP
============================================================
✓ Data loaded successfully from example_data.csv
  Shape: 20 rows, 6 columns

============================================================
DATA SUMMARY
============================================================
Dataset: example_data.csv
Rows: 20
Columns: 6
...

============================================================
AUTOMATED INSIGHTS
============================================================
  🔑 'name' appears to be a unique identifier
  📋 'department' has 3 categories

============================================================
CORRELATION ANALYSIS
============================================================
Strong correlations (|r| >= 0.5):
  age <-> experience_years: 0.993
  salary <-> experience_years: 0.911
  age <-> salary: 0.892

✓ Correlation matrix saved to correlation_matrix.png
```

---

## Häufige Anwendungsfälle

### 1. Eigene CSV-Datei analysieren

```bash
# Ersetze example_data.csv mit deiner Datei
python cli.py meine_daten.csv
```

### 2. Nur Summary anzeigen

```bash
python cli.py example_data.csv --summary
```

### 3. Spezifische Spalte analysieren

```bash
# Analysiere die Spalte "salary"
python cli.py example_data.csv --column salary
```

Output:
```
============================================================
ANALYSIS: salary
============================================================

Data Type: int64
Non-null Count: 20/20

Numerical Statistics:
  Mean: 63650.00
  Median: 64500.00
  Std Dev: 7603.84
  Min: 51000.00
  Max: 78000.00
```

### 4. Visualisierung erstellen

```bash
# Erstelle Visualisierung für "age"
python cli.py example_data.csv --visualize age
```

Erstellt: `age_plot.png` mit Histogram und Boxplot

### 5. Nur Korrelationen finden

```bash
# Finde starke Korrelationen (>= 0.7)
python cli.py example_data.csv --correlations --corr-threshold 0.7
```

### 6. Insights generieren

```bash
# Automatische Datenqualitäts-Analyse
python cli.py example_data.csv --insights
```

---

## Als Python-Modul verwenden

### Basis-Verwendung

```python
from data_analyst_agent import DataAnalystAgent

# Agent initialisieren
agent = DataAnalystAgent("example_data.csv")

# Daten-Summary
agent.get_summary()

# Spalte analysieren
agent.analyze_column("salary")

# Visualisierung erstellen
agent.visualize_column("age", "age_distribution.png")

# Korrelationen finden
agent.find_correlations(threshold=0.5)

# Insights generieren
agent.get_insights()
```

### Fortgeschrittenes Beispiel

```python
from data_analyst_agent import DataAnalystAgent
import pandas as pd

# Initialisiere Agent ohne Daten
agent = DataAnalystAgent()

# Lade verschiedene Dateien nacheinander
datasets = ["sales_2023.csv", "sales_2024.csv"]

for dataset in datasets:
    print(f"\n{'='*60}")
    print(f"Analyzing: {dataset}")
    print('='*60)

    agent.load_data(dataset)

    # Custom Analysis
    summary = agent.get_summary()
    insights = agent.get_insights()

    # Speichere Korrelationsmatrix mit spezifischem Namen
    agent.find_correlations(threshold=0.6)

    # Analysiere wichtigste Spalten
    numeric_cols = agent.data.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        agent.analyze_column(col)
        agent.visualize_column(col, f"{dataset}_{col}_plot.png")
```

---

## CLI Optionen im Detail

```bash
python cli.py [DATA_FILE] [OPTIONS]

Optionen:
  DATA_FILE              Pfad zur CSV-Datei (required)

  --summary              Zeige statistische Zusammenfassung
  --column SPALTE        Analysiere spezifische Spalte
  --visualize SPALTE     Erstelle Visualisierung für Spalte
  --correlations         Finde Korrelationen zwischen Spalten
  --corr-threshold N     Korrelations-Schwellenwert (default: 0.5)
  --insights             Zeige automatisierte Insights
  --all                  Führe alle Analysen durch (default wenn keine Option)

Beispiele:
  python cli.py data.csv                          # Alle Analysen
  python cli.py data.csv --summary                # Nur Summary
  python cli.py data.csv --column age             # Spalte "age"
  python cli.py data.csv --visualize salary       # Visualisierung
  python cli.py data.csv --correlations           # Korrelationen
  python cli.py data.csv --corr-threshold 0.7     # Nur starke Korr.
  python cli.py data.csv --insights               # Insights
```

---

## Projektstruktur verstehen

```
AI_Agent_Project/
│
├── data_analyst_agent.py   # 🧠 Haupt-Agent Klasse
│   ├── __init__()          #    Agent initialisieren
│   ├── load_data()         #    CSV laden
│   ├── get_summary()       #    Statistiken
│   ├── analyze_column()    #    Spalten-Analyse
│   ├── visualize_column()  #    Charts erstellen
│   ├── find_correlations() #    Korrelationen finden
│   └── get_insights()      #    Auto-Insights
│
├── cli.py                   # 💻 Command-Line Interface
│   └── main()              #    Argumente parsen & Agent aufrufen
│
├── test_agent.py           # ✅ Test-Script
├── example_data.csv        # 📊 Beispiel-Daten
├── requirements.txt        # 📦 Dependencies
│
├── README.md               # 📖 Projekt-Dokumentation
├── QUICK_START.md          # 🚀 Dieser Guide
└── AGENT_SYSTEM_GUIDE.md   # 📚 Vollständige Agent-Architektur Erklärung
```

---

## Was die Beispieldaten enthalten

```csv
name,age,salary,department,experience_years,performance_score
Alice Johnson,28,55000,Engineering,3,8.5
Bob Smith,35,72000,Engineering,8,9.2
Charlie Brown,42,65000,Sales,12,7.8
...
```

**Spalten:**
- `name`: Mitarbeiter-Name (string)
- `age`: Alter (integer)
- `salary`: Gehalt (integer)
- `department`: Abteilung (string: Engineering, Sales, Marketing)
- `experience_years`: Jahre Erfahrung (integer)
- `performance_score`: Performance-Score (float, 0-10)

---

## Test ausführen

```bash
# Einfacher Funktionstest
python test_agent.py
```

---

## Nächste Schritte

### Level 1: Basis-Verwendung ✅
- [x] Projekt installiert
- [ ] Beispieldaten analysiert
- [ ] Eigene CSV-Datei analysiert
- [ ] Visualisierungen erstellt

### Level 2: Python Integration 🐍
- [ ] Agent als Modul verwendet
- [ ] Custom Analysis-Script geschrieben
- [ ] Mehrere Dateien automatisch analysiert

### Level 3: Multi-Agent System 🚀
- [ ] AGENT_SYSTEM_GUIDE.md gelesen
- [ ] Multi-Agent Architektur verstanden
- [ ] Eigenes Multi-Agent System entworfen
- [ ] Agent Shutton Konzepte angewendet

---

## Hilfe & Ressourcen

### Dokumentation
- **README.md**: Projekt-Übersicht
- **AGENT_SYSTEM_GUIDE.md**: Vollständige Agent-Architektur Erklärung
- **Dieser Guide**: Quick Start

### Bei Problemen

**Fehler: "ModuleNotFoundError"**
```bash
# Dependencies neu installieren
pip install -r requirements.txt
```

**Fehler: "File not found"**
```bash
# Prüfe ob Datei existiert
ls -la *.csv

# Verwende absoluten Pfad
python cli.py /vollständiger/pfad/zu/datei.csv
```

**Fehler: "No module named 'data_analyst_agent'"**
```bash
# Stelle sicher, dass du im Projekt-Ordner bist
cd /home/user/AI_Agent_Project

# Dann ausführen
python cli.py example_data.csv
```

---

## Erweiterte Funktionen (Coming Soon)

Mögliche Erweiterungen für dein Agent System:

1. **Multi-Format Support**
   - Excel (.xlsx)
   - JSON
   - SQL Datenbanken

2. **Erweiterte ML-Features**
   - Clustering
   - Anomaly Detection
   - Predictive Modeling

3. **Interactive Dashboards**
   - Web-Interface mit Flask/Streamlit
   - Live-Updates
   - Interactive Charts

4. **Natural Language Queries**
   - "Zeige mir alle Mitarbeiter mit Gehalt > 60000"
   - "Welche Abteilung hat die höchste Performance?"

5. **PDF/HTML Reports**
   - Automatische Report-Generierung
   - Export-Funktionen

6. **Multi-Agent Erweiterung**
   - DataQualityAgent
   - MachineLearningAgent
   - ReportGeneratorAgent

---

## Feedback & Fragen

Wenn du mehr über Multi-Agent Systeme lernen möchtest:
📖 Lies: `AGENT_SYSTEM_GUIDE.md`

Viel Erfolg! 🎉
