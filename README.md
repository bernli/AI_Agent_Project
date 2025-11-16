# Data Analyst Agent MVP

Ein einfacher KI-Agent für automatisierte Datenanalyse. Analysiert CSV-Dateien und liefert statistische Insights, Visualisierungen und Korrelationen.

## 📚 Dokumentation

- **[QUICK_START.md](QUICK_START.md)** - Schnellstart Guide (5 Minuten)
- **[AGENT_SYSTEM_GUIDE.md](AGENT_SYSTEM_GUIDE.md)** - Vollständiger Guide zu Agent-Architekturen
  - Single-Agent vs Multi-Agent Systeme
  - Agent Shutton Multi-Agent Architektur
  - Wie man Multi-Agent Systeme baut
  - Praktische Beispiele & Best Practices

## Features

- **Automatische Datenanalyse**: Lädt CSV-Dateien und erstellt umfassende statistische Zusammenfassungen
- **Spaltenanalyse**: Detaillierte Analyse einzelner Datenspalten (numerisch und kategorial)
- **Visualisierungen**: Automatische Erstellung von Histogrammen, Boxplots und Balkendiagrammen
- **Korrelationsanalyse**: Findet Zusammenhänge zwischen numerischen Variablen
- **Automated Insights**: KI-generierte Erkenntnisse über Datenqualität und Auffälligkeiten
- **CLI Interface**: Einfache Kommandozeilen-Bedienung

## Installation

```bash
# Repository klonen
git clone <repository-url>
cd AI_Agent_Project

# Dependencies installieren
pip install -r requirements.txt

# Optional: Architektur-Diagramme erstellen
python visualize_agent_architectures.py
```

## Schnellstart

### Beispiel-Analyse durchführen

```bash
# Vollständige Analyse der Beispieldaten
python cli.py example_data.csv

# Nur Summary anzeigen
python cli.py example_data.csv --summary

# Spezifische Spalte analysieren
python cli.py example_data.csv --column salary

# Korrelationen finden
python cli.py example_data.csv --correlations

# Automated Insights
python cli.py example_data.csv --insights
```

### Als Python-Modul verwenden

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

## CLI Optionen

```
usage: cli.py [-h] [--summary] [--column COLUMN] [--visualize VISUALIZE]
              [--correlations] [--corr-threshold CORR_THRESHOLD]
              [--insights] [--all]
              data_file

Optionen:
  data_file              Pfad zur CSV-Datei
  --summary              Zeige Daten-Zusammenfassung
  --column COLUMN        Analysiere spezifische Spalte
  --visualize VISUALIZE  Erstelle Visualisierung für Spalte
  --correlations         Finde Korrelationen
  --corr-threshold       Korrelations-Schwellenwert (default: 0.5)
  --insights             Zeige automatisierte Insights
  --all                  Führe alle Analysen durch
```

## Tests

```bash
# Einfacher Funktionstest
python test_agent.py
```

## Projektstruktur

```
AI_Agent_Project/
├── data_analyst_agent.py   # Hauptklasse des Agenten
├── cli.py                   # Command-line Interface
├── test_agent.py           # Test-Script
├── example_data.csv        # Beispieldaten
├── requirements.txt        # Python Dependencies
├── .gitignore             # Git-Konfiguration
└── README.md              # Diese Datei
```

## Agent-Funktionen im Detail

### 1. Data Summary
Zeigt grundlegende Statistiken:
- Anzahl Zeilen und Spalten
- Datentypen
- Fehlende Werte
- Statistische Kennzahlen (Mean, Median, Std, etc.)

### 2. Column Analysis
Analysiert einzelne Spalten:
- **Numerisch**: Mean, Median, Std Dev, Min, Max
- **Kategorial**: Unique Values, Top 5 Werte

### 3. Visualizations
Erstellt automatisch passende Visualisierungen:
- **Numerisch**: Histogram + Boxplot
- **Kategorial**: Balkendiagramm der Top-10 Werte

### 4. Correlation Analysis
- Findet Korrelationen zwischen numerischen Spalten
- Erstellt Correlation-Heatmap
- Filtert nach Korrelations-Schwellenwert

### 5. Automated Insights
Erkennt automatisch:
- Fehlende Daten (> 10%)
- Duplikate
- Outliers (IQR-Methode)
- Unique Identifiers
- Kategorien-Anzahl

## Beispiel-Output

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

Column Types:
name                  object
age                    int64
salary                 int64
department            object
experience_years       int64
performance_score    float64
...

============================================================
AUTOMATED INSIGHTS
============================================================

  📋 'department' has 3 categories
  📊 'salary' has 0 potential outliers (0.0%)
  ✓ No major issues detected
```

## Anforderungen

- Python 3.8+
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- numpy >= 1.24.0

## Lizenz

MIT License

## Entwicklung

Dies ist ein MVP (Minimum Viable Product) zu Testzwecken.

Mögliche Erweiterungen:
- Support für weitere Datenformate (Excel, JSON, SQL)
- Erweiterte ML-Features (Clustering, Classification)
- Interactive Dashboards
- Natural Language Queries
- Export-Funktionen (PDF Reports)
