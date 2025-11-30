# BigQuery MCP Setup für InsightLoop

## Übersicht

MCP Toolbox v0.7.0 mit vorkonfigurierter BigQuery-Integration.

## Status: Phase 1 KOMPLETT ✅

### Was ist fertig:
- ✅ mcp-toolbox/ Ordner erstellt
- ✅ toolbox-bigquery.exe (v0.7.0) heruntergeladen (88.5 MB)
- ✅ BigQuery prebuilt configuration verfügbar

### Verfügbare BigQuery Tools:
1. `analyze_contribution` - Beitragsanalyse
2. `ask_data_insights` - Dateneinblicke abfragen
3. `execute_sql` - SQL-Abfragen ausführen
4. `forecast` - Vorhersagen erstellen
5. `get_dataset_info` - Dataset-Informationen abrufen
6. `get_table_info` - Tabellen-Informationen abrufen
7. `list_dataset_ids` - Alle Datasets auflisten
8. `list_table_ids` - Alle Tabellen auflisten
9. `search_catalog` - Data Catalog durchsuchen

## Phase 2: Google Cloud Setup (TODO)

### Voraussetzungen:
1. **Google Cloud Projekt**
   - Projekt erstellen oder bestehendes verwenden
   - Billing aktiviert
   - BigQuery API aktiviert

2. **IAM Berechtigungen**
   - `roles/bigquery.user` (BigQuery User)
   - `roles/bigquery.dataViewer` (BigQuery Data Viewer)

3. **Authentication (ADC - Application Default Credentials)**
   ```bash
   # Google Cloud SDK installieren, dann:
   gcloud auth application-default login
   ```

4. **Daten in BigQuery hochladen**
   - CSV/Parquet/JSON Dateien hochladen
   - Oder: Bestehende BigQuery Datasets verwenden

## Phase 3: Claude Code Konfiguration (TODO)

### MCP Server Konfiguration in Claude Code

**Pfad:** Claude Code → Settings → Developer → MCP Servers

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "c:\\Users\\olive\\Desktop\\Projects\\claude\\AI_Agent_Project\\mcp-toolbox\\toolbox-bigquery.exe",
      "args": ["--prebuilt", "bigquery", "--stdio"],
      "env": {
        "BIGQUERY_PROJECT": "IHR_PROJEKT_ID"
      }
    }
  }
}
```

**Wichtig:** Ersetze `IHR_PROJEKT_ID` mit deiner Google Cloud Projekt-ID.

## Phase 4: Integration mit InsightLoop (TODO)

Nach erfolgreicher MCP-Konfiguration:

1. InsightLoop kann BigQuery-Tools über MCP nutzen
2. Claude Code bietet BigQuery-Tools automatisch an
3. Analysen können direkt auf BigQuery-Daten laufen

## Nächste Schritte

**Du entscheidest:**
1. Hast du schon ein Google Cloud Projekt?
2. Sind dort BigQuery Datasets vorhanden?
3. Oder sollen wir zuerst Daten hochladen?

## Test ohne Daten

Um MCP Server zu testen (auch ohne Daten):
```bash
cd mcp-toolbox
.\toolbox-bigquery.exe --prebuilt bigquery --stdio
```

Hinweis: Ohne gültige BIGQUERY_PROJECT Umgebungsvariable wird ein Fehler erscheinen.
