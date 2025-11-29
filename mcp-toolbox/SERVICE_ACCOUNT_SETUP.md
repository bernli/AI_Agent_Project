# Service Account Setup für BigQuery MCP

## Problem
- `gcloud` CLI hat Python-Konfigurationsproblem
- Application Default Credentials funktionieren nicht

## Lösung: Service Account Key

### Schritt 1: Service Account erstellen (Google Cloud Console)

1. **Öffne Google Cloud Console:**
   https://console.cloud.google.com/

2. **Navigiere zu IAM & Admin → Service Accounts:**
   https://console.cloud.google.com/iam-admin/serviceaccounts?project=gen-lang-client-0152066550

3. **Klicke "CREATE SERVICE ACCOUNT"**

4. **Service Account Details:**
   - Name: `bigquery-mcp-service-account`
   - ID: `bigquery-mcp-service-account` (wird automatisch generiert)
   - Description: "Service account for BigQuery MCP Server"
   - Klicke **"CREATE AND CONTINUE"**

5. **Grant Permissions (Rolle zuweisen):**
   - Rolle 1: **BigQuery User** (`roles/bigquery.user`)
   - Rolle 2: **BigQuery Data Viewer** (`roles/bigquery.dataViewer`)
   - Klicke **"CONTINUE"**

6. **Grant users access (optional):**
   - Kannst du überspringen
   - Klicke **"DONE"**

### Schritt 2: JSON Key herunterladen

1. **Finde den neu erstellten Service Account in der Liste**

2. **Klicke auf die drei Punkte (⋮) rechts → "Manage keys"**

3. **Klicke "ADD KEY" → "Create new key"**

4. **Wähle Key type: JSON**

5. **Klicke "CREATE"**
   - Eine JSON-Datei wird heruntergeladen (z.B. `gen-lang-client-0152066550-abc123.json`)

6. **Verschiebe die Datei:**
   - Verschiebe die JSON-Datei nach:
   ```
   c:\Users\olive\Desktop\Projects\claude\AI_Agent_Project\mcp-toolbox\service-account-key.json
   ```

### Schritt 3: .mcp.json aktualisieren

Ich werde die `.mcp.json` automatisch aktualisieren, sobald du mir sagst dass der Key heruntergeladen ist.

Die neue Config wird so aussehen:
```json
{
  "mcpServers": {
    "bigquery": {
      "command": "c:\\Users\\olive\\Desktop\\Projects\\claude\\AI_Agent_Project\\mcp-toolbox\\toolbox-bigquery.exe",
      "args": ["--prebuilt", "bigquery", "--stdio"],
      "env": {
        "BIGQUERY_PROJECT": "gen-lang-client-0152066550",
        "GOOGLE_APPLICATION_CREDENTIALS": "c:\\Users\\olive\\Desktop\\Projects\\claude\\AI_Agent_Project\\mcp-toolbox\\service-account-key.json"
      }
    }
  }
}
```

### Schritt 4: VS Code neu laden & testen

Nach dem Update:
1. VS Code neu laden (`Ctrl + Shift + P` → "Reload Window")
2. Im Claude Chat testen:
   ```
   List tables in bigquery-public-data.thelook_ecommerce
   ```

---

## Sicherheit

**WICHTIG:**
- Die `service-account-key.json` Datei ist **GEHEIM**!
- Füge sie zu `.gitignore` hinzu (ich mache das automatisch)
- Teile sie NIEMALS in Git oder öffentlich

---

## Nächste Schritte

1. **Öffne Google Cloud Console** (Link oben)
2. **Erstelle Service Account** mit den beiden BigQuery Rollen
3. **Lade JSON Key herunter**
4. **Speichere als:** `c:\Users\olive\Desktop\Projects\claude\AI_Agent_Project\mcp-toolbox\service-account-key.json`
5. **Sag mir Bescheid** → Ich update die `.mcp.json` automatisch

---

**Fragen?** Sag Bescheid!
