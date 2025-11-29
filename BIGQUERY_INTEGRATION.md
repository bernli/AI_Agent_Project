# BigQuery Integration in InsightLoop

## ✅ Setup abgeschlossen (29.11.2024)

### Was wurde gemacht:

1. **MCP Toolbox v0.7.0 installiert**
   - BigQuery MCP Server konfiguriert
   - Service Account mit BigQuery Zugriff erstellt
   - `.mcp.json` konfiguriert

2. **InsightLoop erweitert**
   - Agent instruction aktualisiert
   - Automatisches Routing: BigQuery vs. CSV
   - **Keine Code-Änderungen nötig** - nur Instruction!

3. **Sicherheit**
   - Service Account Key in `.gitignore`
   - Niemals in Git committed

---

## 🎯 Wie es funktioniert

### Smart Routing (Keyword-basiert)

**User sagt "ecommerce"** → BigQuery MCP Tools
**User gibt Dateipfad** → Lokale CSV Analyse

### Architektur (extrem einfach!)

```
User Question
     ↓
InsightLoop Agent
     ↓
  Keywords erkannt?
     ↓
┌─────────────┬──────────────┐
│ "ecommerce" │  Dateipfad   │
│ "thelook"   │  "CSV"       │
│ "shop"      │              │
└─────────────┴──────────────┘
     ↓              ↓
BigQuery        CSV Tools
MCP Tools       (Python)
```

---

## 📊 Verfügbare Daten

### BigQuery E-Commerce Dataset
**Dataset:** `bigquery-public-data.thelook_ecommerce`

**Tabellen:**
1. `orders` - Bestellungen
2. `order_items` - Einzelne Bestellpositionen
3. `products` - Produktkatalog
4. `users` - Kundeninformationen
5. `distribution_centers` - Verteilzentren
6. `events` - User Events/Tracking
7. `inventory_items` - Lagerbestand
8. `thelook_ecommerce-table` - Zusätzliche Daten

---

## 🚀 Beispiel-Nutzung

### BigQuery Analysen

**Frage 1:**
```
Wie viele Produkte haben im Jahr 2023 in unserem ecommerce Geschäft verdient?
```

**Frage 2:**
```
Zeige mir die Top 10 Produkte nach Umsatz im thelook ecommerce Dataset.
```

**Frage 3:**
```
Analysiere die Bestellungen nach Land in unserem online shop.
```

### CSV Analysen (wie bisher)

```
Analysiere die Datei data/sales.csv und zeige mir Trends.
```

---

## 🔧 Technische Details

### MCP Configuration (.mcp.json)
```json
{
  "mcpServers": {
    "bigquery": {
      "command": "...\\toolbox-bigquery.exe",
      "args": ["--prebuilt", "bigquery", "--stdio"],
      "env": {
        "BIGQUERY_PROJECT": "gen-lang-client-0152066550",
        "GOOGLE_APPLICATION_CREDENTIALS": "...\\service-account-key.json"
      }
    }
  }
}
```

### Agent Instruction (insight_loop/agent.py)
- Erweitert um BigQuery Data Source
- Keywords für automatisches Routing
- MCP Tools werden direkt genutzt
- Keine Python-Wrapper nötig

---

## ✨ Vorteile dieser Lösung

✅ **Extrem einfach** - Nur Instruction geändert
✅ **Robust** - Keine neuen Dependencies
✅ **MCP-native** - Nutzt BigQuery Tools direkt
✅ **Automatisch** - Agent entscheidet selbst
✅ **Erweiterbar** - Später mehr Keywords/Datasets möglich
✅ **Wartbar** - Minimale Komplexität

---

## 🔮 Zukünftige Erweiterungen (optional)

1. **Mehr Datasets:**
   - Eigene BigQuery Datasets hinzufügen
   - Weitere public datasets

2. **Hybrid-Analysen:**
   - BigQuery + CSV kombinieren
   - Cross-source Analysen

3. **Python-Wrapper:**
   - Falls mehr Kontrolle gewünscht
   - Custom BigQuery Tools

4. **Caching:**
   - BigQuery Ergebnisse lokal cachen
   - Kosten sparen

---

## 📝 Changelog

**29.11.2024 - Initial BigQuery Integration**
- MCP Toolbox v0.7.0 installiert
- Service Account erstellt
- InsightLoop instruction erweitert
- Keyword-basiertes Routing implementiert
- Status: ✅ Produktiv

---

**Nächste Schritte:** Testen mit echten ecommerce-Fragen!
