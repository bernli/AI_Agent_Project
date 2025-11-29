# MCP Toolbox Setup für Claude Code (VSCode) - DuckDB

## 🎯 Was du erreichen wirst

Claude Code in VSCode kann direkt mit deiner DuckDB-Datenbank interagieren:
- ✅ "Claude, zeig mir alle Regions in der Datenbank"
- ✅ "Claude, welche Produkte verkauften sich am besten?"
- ✅ "Claude, erstelle einen SQL Query für Q4 Revenue"

---

## 📋 Voraussetzungen

1. ✅ **VSCode** installiert
2. ✅ **Claude Code Extension** installiert
3. ✅ **Node.js** (für npx) - Version 18+
4. ✅ **DuckDB Database** (erstellen wir gleich)

---

## 🚀 Setup in 10 Minuten

### **Schritt 1: Projekt-Struktur vorbereiten**

```bash
# Erstelle Projekt-Ordner (falls noch nicht vorhanden)
mkdir -p ~/claude-code-mcp-demo
cd ~/claude-code-mcp-demo

# Ordner für MCP Toolbox
mkdir -p mcp-toolbox
mkdir -p data
```

---

### **Schritt 2: MCP Toolbox herunterladen**

```bash
cd mcp-toolbox

# Für Linux
export VERSION=0.21.0
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v$VERSION/linux/amd64/toolbox
chmod +x toolbox

# Für macOS (M1/M2/M3 - ARM)
export VERSION=0.21.0
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v$VERSION/darwin/arm64/toolbox
chmod +x toolbox

# Für macOS (Intel)
export VERSION=0.21.0
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v$VERSION/darwin/amd64/toolbox
chmod +x toolbox

cd ..
```

**Testen:**
```bash
./mcp-toolbox/toolbox --version
# Should output: toolbox version 0.21.0
```

---

### **Schritt 3: Sample Database erstellen**

**Option A: Mit existierendem CSV**

Falls du `retail_sales_data.csv` hast:

```bash
# create_db.py
cat > create_db.py << 'EOF'
import duckdb
import pandas as pd

# CSV laden
df = pd.read_csv('retail_sales_data.csv')

# DuckDB erstellen
conn = duckdb.connect('data/retail_sales.duckdb')

# Tabelle erstellen
conn.execute("""
CREATE TABLE sales AS 
SELECT 
    CAST(date AS DATE) as date,
    region,
    customer_segment,
    product_category,
    CAST(revenue AS DECIMAL(10,2)) as revenue,
    units_sold,
    customer_id
FROM df
""")

# Indexes
conn.execute("CREATE INDEX idx_date ON sales(date)")
conn.execute("CREATE INDEX idx_region ON sales(region)")
conn.execute("CREATE INDEX idx_category ON sales(product_category)")

print(f"✅ Database created with {conn.execute('SELECT COUNT(*) FROM sales').fetchone()[0]} rows")
conn.close()
EOF

python create_db.py
```

**Option B: Demo-Daten generieren**

Falls du kein CSV hast:

```bash
# generate_demo_data.py
cat > generate_demo_data.py << 'EOF'
import duckdb
import random
from datetime import datetime, timedelta

conn = duckdb.connect('data/retail_sales.duckdb')

# Demo-Daten erstellen
conn.execute("""
CREATE TABLE sales (
    date DATE,
    region VARCHAR,
    customer_segment VARCHAR,
    product_category VARCHAR,
    revenue DECIMAL(10,2),
    units_sold INTEGER,
    customer_id VARCHAR
)
""")

# Sample Daten einfügen
regions = ['North America', 'EMEA', 'APAC', 'LATAM']
segments = ['Enterprise', 'SMB']
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors']

start_date = datetime(2023, 1, 1)
for i in range(500):
    date = start_date + timedelta(days=random.randint(0, 730))
    conn.execute("""
        INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date.strftime('%Y-%m-%d'),
        random.choice(regions),
        random.choice(segments),
        random.choice(categories),
        round(random.uniform(10000, 200000), 2),
        random.randint(50, 500),
        f"C{random.randint(1, 100):03d}"
    ))

# Indexes
conn.execute("CREATE INDEX idx_date ON sales(date)")
conn.execute("CREATE INDEX idx_region ON sales(region)")
conn.execute("CREATE INDEX idx_category ON sales(product_category)")

print(f"✅ Demo database created with {conn.execute('SELECT COUNT(*) FROM sales').fetchone()[0]} rows")
conn.close()
EOF

python generate_demo_data.py
```

**Verifizieren:**
```bash
duckdb data/retail_sales.duckdb "SELECT COUNT(*) as total_rows FROM sales"
```

---

### **Schritt 4: MCP Toolbox konfigurieren**

Erstelle `mcp-toolbox/tools.yaml`:

```bash
cat > mcp-toolbox/tools.yaml << 'EOF'
# MCP Toolbox Configuration for Claude Code
# Database: DuckDB (retail sales data)

sources:
  retail_duckdb:
    kind: duckdb
    database: ../data/retail_sales.duckdb

tools:
  # Tool 1: Flexible SQL query
  query_sales_data:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Execute custom SQL queries on retail sales data. Use for complex queries with custom filters."
    query: |
      SELECT 
        ${columns:*}
      FROM sales
      WHERE 1=1
        ${region_filter:}
        ${date_filter:}
        ${category_filter:}
      ${group_by:}
      ${order_by:}
      LIMIT ${limit:100}
    parameters:
      columns:
        type: string
        description: "Columns to select (default: all). Example: 'region, SUM(revenue) as total'"
        default: "*"
      region_filter:
        type: string
        description: "Region filter. Example: 'AND region = ''North America'''. Leave empty for all."
        default: ""
      date_filter:
        type: string
        description: "Date filter. Example: 'AND date >= ''2024-01-01'''. Leave empty for all."
        default: ""
      category_filter:
        type: string
        description: "Category filter. Example: 'AND product_category = ''Electronics'''"
        default: ""
      group_by:
        type: string
        description: "GROUP BY clause. Example: 'GROUP BY region'"
        default: ""
      order_by:
        type: string
        description: "ORDER BY clause. Example: 'ORDER BY revenue DESC'"
        default: ""
      limit:
        type: integer
        description: "Max rows to return"
        default: 100

  # Tool 2: Regional summary (pre-built)
  get_regional_summary:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Get revenue summary by region. Quick way to see regional performance."
    query: |
      SELECT 
        region,
        COUNT(*) as transaction_count,
        COUNT(DISTINCT customer_id) as unique_customers,
        SUM(revenue) as total_revenue,
        ROUND(AVG(revenue), 2) as avg_transaction,
        SUM(units_sold) as total_units
      FROM sales
      WHERE date >= '${start_date:2023-01-01}'
        AND date <= '${end_date:2025-12-31}'
      GROUP BY region
      ORDER BY total_revenue DESC
    parameters:
      start_date:
        type: string
        description: "Start date (YYYY-MM-DD)"
        default: "2023-01-01"
      end_date:
        type: string
        description: "End date (YYYY-MM-DD)"
        default: "2025-12-31"

  # Tool 3: Product performance
  get_product_performance:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Analyze product category performance across regions"
    query: |
      SELECT 
        product_category,
        region,
        COUNT(*) as transactions,
        SUM(revenue) as total_revenue,
        SUM(units_sold) as total_units,
        ROUND(AVG(revenue), 2) as avg_transaction
      FROM sales
      WHERE date >= '${start_date:2024-01-01}'
        ${region_filter:}
      GROUP BY product_category, region
      ORDER BY total_revenue DESC
      LIMIT ${limit:20}
    parameters:
      start_date:
        type: string
        description: "Start date (YYYY-MM-DD)"
        default: "2024-01-01"
      region_filter:
        type: string
        description: "Optional region filter. Example: 'AND region = ''APAC'''"
        default: ""
      limit:
        type: integer
        description: "Number of results"
        default: 20

  # Tool 4: Monthly trends
  get_monthly_trends:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Get monthly revenue trends with year-over-year comparison"
    query: |
      WITH monthly_data AS (
        SELECT 
          strftime(date, '%Y-%m') as month,
          ${dimension:region} as dimension,
          SUM(revenue) as revenue,
          SUM(units_sold) as units
        FROM sales
        WHERE date >= '${start_date:2023-01-01}'
        GROUP BY month, dimension
      )
      SELECT 
        month,
        dimension,
        revenue,
        units,
        LAG(revenue, 12) OVER (PARTITION BY dimension ORDER BY month) as revenue_last_year,
        ROUND((revenue - LAG(revenue, 12) OVER (PARTITION BY dimension ORDER BY month)) 
              / NULLIF(LAG(revenue, 12) OVER (PARTITION BY dimension ORDER BY month), 0) * 100, 2) 
              as yoy_growth_percent
      FROM monthly_data
      ORDER BY month DESC, revenue DESC
      LIMIT ${limit:50}
    parameters:
      start_date:
        type: string
        description: "Start date for trends"
        default: "2023-01-01"
      dimension:
        type: string
        description: "Grouping dimension: region, product_category, or customer_segment"
        default: "region"
      limit:
        type: integer
        default: 50

  # Tool 5: Top customers
  get_top_customers:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Find top customers by revenue"
    query: |
      SELECT 
        customer_id,
        COUNT(*) as purchase_count,
        SUM(revenue) as total_spent,
        ROUND(AVG(revenue), 2) as avg_purchase,
        MAX(date) as last_purchase,
        STRING_AGG(DISTINCT product_category, ', ') as categories_purchased
      FROM sales
      WHERE date >= '${start_date:2024-01-01}'
      GROUP BY customer_id
      ORDER BY total_spent DESC
      LIMIT ${limit:10}
    parameters:
      start_date:
        type: string
        description: "Start date"
        default: "2024-01-01"
      limit:
        type: integer
        description: "Number of top customers"
        default: 10

toolsets:
  retail_analytics:
    description: "Retail sales analytics tools for Claude Code"
    tools:
      - query_sales_data
      - get_regional_summary
      - get_product_performance
      - get_monthly_trends
      - get_top_customers
EOF
```

**Testen:**
```bash
cd mcp-toolbox
./toolbox --tools-file tools.yaml

# Expected output:
# INFO "Initialized 1 sources."
# INFO "Initialized 5 tools."
# INFO "Initialized 1 toolsets."
# INFO "Server ready to serve!"
```

Drücke `Ctrl+C` um zu stoppen.

---

### **Schritt 5: Claude Code konfigurieren**

**Option A: CLI Wizard (Empfohlen für Anfänger)**

```bash
# MCP Server hinzufügen
claude mcp add

# Wizard wird fragen:
# Name: toolbox-retail
# Transport: stdio
# Command: /absolute/path/to/mcp-toolbox/toolbox
# Args: --tools-file /absolute/path/to/mcp-toolbox/tools.yaml
```

**⚠️ WICHTIG:** Verwende **absolute Pfade**!

```bash
# Absolute Pfade herausfinden:
echo "Command: $(pwd)/mcp-toolbox/toolbox"
echo "Args: --tools-file $(pwd)/mcp-toolbox/tools.yaml"
```

---

**Option B: JSON direkt (Empfohlen für Fortgeschrittene)**

```bash
# Finde absolute Pfade
TOOLBOX_PATH="$(pwd)/mcp-toolbox/toolbox"
CONFIG_PATH="$(pwd)/mcp-toolbox/tools.yaml"

# JSON generieren
MCP_JSON=$(cat <<EOF
{
  "command": "$TOOLBOX_PATH",
  "args": ["--tools-file", "$CONFIG_PATH"]
}
EOF
)

# MCP Server hinzufügen
claude mcp add-json "toolbox-retail" "$MCP_JSON"
```

---

**Option C: Config-File direkt editieren (Für Experten)**

```bash
# Config-File öffnen
nano ~/.claude/claude.json
```

Füge hinzu:

```json
{
  "mcpServers": {
    "toolbox-retail": {
      "command": "/ABSOLUTE/PATH/TO/mcp-toolbox/toolbox",
      "args": ["--tools-file", "/ABSOLUTE/PATH/TO/mcp-toolbox/tools.yaml"]
    }
  }
}
```

**Ersetze `/ABSOLUTE/PATH/TO/` mit deinem echten Pfad!**

---

### **Schritt 6: Verifizieren**

```bash
# MCP Server auflisten
claude mcp list

# Expected output:
# toolbox-retail (stdio)
#   Command: /path/to/mcp-toolbox/toolbox
#   Args: --tools-file /path/to/mcp-toolbox/tools.yaml
```

---

## 🧪 Testen in VSCode

### **1. VSCode öffnen**

```bash
cd ~/claude-code-mcp-demo
code .
```

### **2. Claude Code Extension aktivieren**

- Klicke auf das **Spark Icon** (⚡) in der Sidebar
- Oder drücke `Cmd/Ctrl + Shift + P` → "Claude Code: Open"

### **3. Test-Queries**

**Test 1: Tools auflisten**
```
List all available MCP tools
```

Claude sollte anzeigen:
- query_sales_data
- get_regional_summary
- get_product_performance
- get_monthly_trends
- get_top_customers

---

**Test 2: Einfache Query**
```
Use the get_regional_summary tool to show me revenue by region for 2024
```

Claude sollte:
1. Tool `get_regional_summary` aufrufen
2. Parameter setzen: `start_date: "2024-01-01"`, `end_date: "2024-12-31"`
3. Ergebnisse in Tabelle zeigen

---

**Test 3: Produkt-Analyse**
```
Which product categories performed best in North America in 2024?
Use the get_product_performance tool
```

---

**Test 4: Custom SQL**
```
Use query_sales_data to show me the top 5 regions by revenue in Q4 2024.
Filter: date >= '2024-10-01' AND date <= '2024-12-31'
Group by region, order by revenue DESC, limit 5
```

---

**Test 5: Trends**
```
Show me monthly revenue trends for Electronics category with year-over-year growth
```

---

## 💡 Best Practices

### **1. Klare Instruktionen geben**

✅ **Gut:**
```
Use get_regional_summary tool with start_date='2024-01-01' to show Q1-Q4 2024 revenue by region
```

❌ **Schlecht:**
```
Show me revenue
```

---

### **2. Tool-Namen explizit nennen**

Claude wählt automatisch, aber du kannst forcieren:

```
Use the query_sales_data tool to create a custom query that shows...
```

---

### **3. Parameter validieren lassen**

```
Before running the query, show me the exact SQL that will be executed
```

---

### **4. Bei Fehlern: Logs checken**

```bash
# Claude Code Logs
tail -f ~/.claude/logs/mcp.log

# MCP Toolbox Logs (wenn im Wizard mode)
# Sichtbar in VSCode Output Panel
```

---

## 🐛 Troubleshooting

### **Problem 1: "MCP server not found"**

**Lösung:**
```bash
# Verifiziere Server-Liste
claude mcp list

# Wenn nicht da:
claude mcp add-json "toolbox-retail" '{
  "command": "/absolute/path/to/toolbox",
  "args": ["--tools-file", "/absolute/path/to/tools.yaml"]
}'

# VSCode neustarten
```

---

### **Problem 2: "Connection failed"**

**Lösung:**
```bash
# Teste Toolbox manuell
cd mcp-toolbox
./toolbox --tools-file tools.yaml

# Sollte starten ohne Fehler
# Wenn Fehler → Database Pfad in tools.yaml checken
```

---

### **Problem 3: "Database file not found"**

**In `tools.yaml`:**
```yaml
sources:
  retail_duckdb:
    kind: duckdb
    database: ../data/retail_sales.duckdb  # Relativer Pfad zum toolbox binary
```

**Testen:**
```bash
# Von mcp-toolbox/ aus:
ls -lh ../data/retail_sales.duckdb

# Sollte existieren
```

---

### **Problem 4: "Tool execution failed"**

**Debugging:**

```bash
# 1. Teste Tool direkt
cd mcp-toolbox
./toolbox --tools-file tools.yaml --ui

# 2. Öffne http://localhost:5000/ui
# 3. Click auf Tool → "Run Tool"
# 4. Siehe Error-Message
```

---

### **Problem 5: Claude nutzt die Tools nicht**

**Lösungen:**

1. **Explizit fragen:**
   ```
   List all available MCP tools. Then use get_regional_summary to show revenue.
   ```

2. **Tool-Namen prüfen:**
   ```bash
   # In VSCode:
   # Cmd+Shift+P → "MCP: List Servers" → toolbox-retail → "Show Output"
   # Sollte Tools auflisten
   ```

3. **Extension neustarten:**
   ```
   Cmd+Shift+P → "Developer: Reload Window"
   ```

---

## 📊 Demo-Scenario (Copy-Paste)

**Öffne Claude Code und paste:**

```
Hi Claude! I have a retail sales database connected via MCP Toolbox. 
Let's explore it step by step:

1. First, list all available MCP tools
2. Use get_regional_summary for 2024 to show revenue by region
3. Then use get_product_performance to show top 3 product categories in North America
4. Finally, use get_monthly_trends to show monthly growth for Electronics category

Show results in clean tables.
```

Claude sollte alle 4 Queries ausführen und Ergebnisse zeigen!

---

## 🎯 Nächste Schritte

### **Mehr Tools hinzufügen:**

Edit `mcp-toolbox/tools.yaml`:

```yaml
tools:
  # ... existing tools ...
  
  # NEW: Inventory check
  check_inventory:
    kind: duckdb-sql
    source: retail_duckdb
    description: "Check which products need restocking"
    query: |
      SELECT 
        product_category,
        region,
        SUM(units_sold) as total_sold,
        COUNT(DISTINCT customer_id) as demand
      FROM sales
      WHERE date >= CURRENT_DATE - INTERVAL '30 days'
      GROUP BY product_category, region
      HAVING SUM(units_sold) > ${threshold:1000}
      ORDER BY total_sold DESC
    parameters:
      threshold:
        type: integer
        description: "Minimum units sold to flag"
        default: 1000
```

Restart MCP server:
```bash
# VSCode neustarten oder:
claude mcp remove toolbox-retail
claude mcp add-json "toolbox-retail" '...'
```

---

### **PostgreSQL hinzufügen:**

Siehe separate Anleitung für Multi-Database Setup.

---

## ✅ Zusammenfassung

**Was du jetzt hast:**

1. ✅ MCP Toolbox läuft lokal
2. ✅ DuckDB Database mit Sales-Daten
3. ✅ 5 vorkonfigurierte Tools
4. ✅ Claude Code kann DB abfragen
5. ✅ Ready für Entwicklung!

**Du kannst jetzt:**
- "Claude, zeig mir Top-Kunden"
- "Claude, analysiere Q4 Performance"
- "Claude, erstelle einen SQL Query für..."
- "Claude, vergleiche Regionen"

---

**Happy Coding! 🚀**

Bei Fragen: `claude mcp list` → Check Logs → Tools.yaml checken → Database testen
