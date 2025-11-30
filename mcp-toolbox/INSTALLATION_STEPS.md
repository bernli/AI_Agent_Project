# BigQuery MCP Installation - Schritt für Schritt

## Status: Phase 1 ✅ | Phase 2 in Arbeit ⏳

### Phase 1: MCP Toolbox Setup ✅
- [x] toolbox-bigquery.exe v0.7.0 heruntergeladen
- [x] Projekt-ID erhalten: `gen-lang-client-0152066550`
- [x] Dataset identifiziert: `bigquery-public-data.thelook_ecommerce`

---

## Phase 2: Google Cloud Authentication (JETZT)

### Schritt 1: Google Cloud SDK installieren

**Prüfen ob bereits installiert:**
```bash
gcloud --version
```

**Falls nicht installiert:**
- Download: https://cloud.google.com/sdk/docs/install
- Installer ausführen
- Nach Installation: Neue Command Prompt öffnen

### Schritt 2: Authentication einrichten

**In Command Prompt oder PowerShell:**

```bash
# 1. Application Default Credentials setzen
gcloud auth application-default login
```
→ Browser öffnet sich → Mit Google Account anmelden → Berechtigung erteilen

```bash
# 2. Projekt setzen
gcloud config set project gen-lang-client-0152066550
```

```bash
# 3. Verifizieren
gcloud config get-value project
```
Sollte ausgeben: `gen-lang-client-0152066550`

### Schritt 3: BigQuery Zugriff testen

```bash
# Liste alle Datasets im Projekt
gcloud bigquery ls

# Teste Zugriff auf public dataset
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM \`bigquery-public-data.thelook_ecommerce.orders\` LIMIT 1"
```

---

## Phase 3: Claude Code MCP Konfiguration (DANACH)

### Schritt 1: MCP Config in Claude Code einfügen

**Pfad:** Claude Code → Settings → Developer → MCP Servers

**Komplette Konfiguration kopieren aus:**
```
c:\Users\olive\Desktop\Projects\claude\AI_Agent_Project\mcp-toolbox\claude-code-mcp-config.json
```

**Oder manuell einfügen:**
```json
{
  "mcpServers": {
    "bigquery": {
      "command": "c:\\Users\\olive\\Desktop\\Projects\\claude\\AI_Agent_Project\\mcp-toolbox\\toolbox-bigquery.exe",
      "args": ["--prebuilt", "bigquery", "--stdio"],
      "env": {
        "BIGQUERY_PROJECT": "gen-lang-client-0152066550"
      }
    }
  }
}
```

### Schritt 2: Claude Code neu starten

- Schließe Claude Code komplett
- Öffne Claude Code neu
- MCP Server sollte automatisch starten

### Schritt 3: BigQuery Tools verifizieren

In Claude Code Chat fragen:
```
List all BigQuery tools available via MCP
```

Erwartete Tools:
1. analyze_contribution
2. ask_data_insights
3. execute_sql
4. forecast
5. get_dataset_info
6. get_table_info
7. list_dataset_ids
8. list_table_ids
9. search_catalog

---

## Phase 4: Erste Analyse mit InsightLoop

### Test Query 1: Dataset erkunden
```
Show me the structure of bigquery-public-data.thelook_ecommerce dataset
```

### Test Query 2: Erste Analyse
```
How many orders are in the thelook_ecommerce.orders table?
```

### Test Query 3: Komplexe Analyse
```
Analyze revenue trends by month from the orders table
```

---

## Troubleshooting

### Fehler: "BIGQUERY_PROJECT not set"
→ MCP Config falsch eingetragen → Prüfe claude-code-mcp-config.json

### Fehler: "Authentication failed"
→ `gcloud auth application-default login` erneut ausführen

### Fehler: "Permission denied"
→ Projekt-Berechtigungen prüfen:
```bash
gcloud projects get-iam-policy gen-lang-client-0152066550
```

### MCP Server startet nicht
1. Claude Code komplett schließen
2. Prüfe ob toolbox-bigquery.exe existiert
3. Prüfe Pfad in MCP Config (Backslashes verdoppelt: `\\`)
4. Claude Code neu starten

---

## Nächste Schritte

**Du bist hier:** Phase 2 - Authentication ⏳

**Als nächstes:**
1. ✅ Führe `gcloud auth application-default login` aus
2. ✅ Setze Projekt mit `gcloud config set project`
3. ✅ Teste BigQuery Zugriff
4. → Melde dich, dann machen wir Phase 3 (MCP Config in Claude Code)

---

**Fragen? Problem?** Sag Bescheid!
