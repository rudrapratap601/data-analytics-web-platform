# 🏗️ Architecture Documentation

## Overview

The **Data Analytics Web Platform** is a full-stack analytics application built with **Streamlit** (frontend), **PostgreSQL/Supabase** (database), and **Plotly** (visualization). It enables users to upload datasets, create relationships between tables, run dynamic SQL analyses, and generate interactive dashboards.

---

## 📂 Project Structure

```
web_app_analysis_system/
│
├── app/                              # Frontend (Streamlit UI)
│   ├── main.py                       # Application entry point & navigation
│   └── my_pages/                     # Page modules
│       ├── home.py                   # Welcome & instructions
│       ├── upload.py                 # Dataset upload (CSV/XLSX)
│       ├── explorer.py               # Dataset browser & preview
│       ├── cleaner.py                # Column cleaning & datatype conversion
│       ├── relationships.py          # Table relationship manager
│       ├── analysis.py               # SQL query builder
│       └── dashboard.py              # Chart generator & insights
│
├── backend/                          # Data layer (Business logic)
│   ├── db.py                         # Database connection & engine
│   ├── schema.py                     # Schema inspection (tables, columns)
│   ├── data_loader.py                # Chunked data loading with caching
│   ├── query_builder.py              # Dynamic SQL query generator
│   ├── chart_engine.py               # Plotly chart creation & recommendation
│   ├── relationships.py              # Relationship CRUD operations
│   ├── insight_engine.py             # AI insights generator
│   ├── quality_report.py             # Data quality metrics
│   └── export_engine.py              # CSV/Excel export functions
│
├── .streamlit/                       # Streamlit configuration
│   ├── config.toml                   # App theme & settings
│   └── secrets.toml                  # Database credentials (gitignored)
│
├── requirements.txt                  # Python dependencies
├── README.md                         # User-facing documentation
├── ARCHITECTURE.md                   # This file
└── .gitignore                        # Version control exclusions
```

---

## 🔄 Data Flow

### Upload Flow

```
User uploads CSV/XLSX
        ↓
app/my_pages/upload.py
        ↓
Sanitize table & column names
        ↓
backend/db.py (get_engine)
        ↓
Pandas .to_sql() with chunking
        ↓
PostgreSQL (Supabase)
```

### Analysis Flow

```
User selects table(s) + metric + aggregation
        ↓
app/my_pages/analysis.py
        ↓
backend/query_builder.py
        ↓
Generates SQL query (with JOINs if multi-table)
        ↓
backend/data_loader.py (cached)
        ↓
Executes SQL query
        ↓
Returns Pandas DataFrame
        ↓
Display results in Streamlit
```

### Dashboard Flow

```
User selects table(s) + dimension + metric
        ↓
app/my_pages/dashboard.py
        ↓
Aggregation SQL executed on PostgreSQL
        ↓
backend/chart_engine.py
        ↓
Recommend chart type based on datatypes
        ↓
Generate Plotly figure
        ↓
backend/insight_engine.py
        ↓
Generate AI insights
        ↓
Display chart + insights + quality report
```

---

## 🗄️ Database Schema

### User-Uploaded Tables

Dynamic tables created from CSV/XLSX uploads. Schema determined by file content.

### `relationships` Table (Internal Metadata)

| Column  | Type   | Description                  |
| ------- | ------ | ---------------------------- |
| id      | SERIAL | Primary key (auto-increment) |
| table1  | TEXT   | First table name             |
| column1 | TEXT   | Column in first table        |
| table2  | TEXT   | Second table name            |
| column2 | TEXT   | Column in second table       |

**Purpose**: Stores foreign-key-like relationships between uploaded datasets to enable multi-table JOIN queries.

---

## 🧩 Component Responsibilities

### Frontend (`app/`)

| Module             | Responsibility                                              |
| ------------------ | ----------------------------------------------------------- |
| `main.py`          | Navigation router, database health check                    |
| `home.py`          | Platform welcome, feature overview, warnings                |
| `upload.py`        | File upload, name sanitization, PostgreSQL insertion        |
| `explorer.py`      | Dataset preview, schema inspection, missing values report   |
| `cleaner.py`       | Column renaming, datatype conversion, save cleaned dataset  |
| `relationships.py` | Create/delete table relationships for JOINs                 |
| `analysis.py`      | Single/multi-table SQL aggregation builder                  |
| `dashboard.py`     | Full dashboard: chart, insights, quality report, CSV export |

### Backend (`backend/`)

| Module              | Responsibility                                                    |
| ------------------- | ----------------------------------------------------------------- |
| `db.py`             | SQLAlchemy engine creation, connection validation                 |
| `schema.py`         | Query information_schema for tables & columns                     |
| `data_loader.py`    | Chunked + cached SQL query execution                              |
| `query_builder.py`  | Build dynamic SQL queries with JOINs, aggregations, GROUP BY      |
| `chart_engine.py`   | Plotly chart generation, type recommendation                      |
| `relationships.py`  | CRUD operations for the `relationships` metadata table            |
| `insight_engine.py` | Statistical insights: avg, max, min, top category, missing values |
| `quality_report.py` | SQL-based data quality metrics (missing values, unique counts)    |
| `export_engine.py`  | Convert DataFrames to CSV/Excel bytes                             |

---

## 🔐 Security & Safety

### SQL Injection Prevention

- **Parameterized queries**: All user inputs use SQLAlchemy's `text()` with parameter binding
- **Double-quoted identifiers**: Table and column names wrapped in `"quotes"` for PostgreSQL safety
- **Name sanitization**: Table and column names stripped of special characters

### Data Validation

- **Empty dataset checks**: Functions validate non-empty DataFrames before processing
- **Column type validation**: Numeric operations restricted to INT/FLOAT/DECIMAL columns
- **Relationship validation**: Multi-table queries fail gracefully if no relationship exists

### Secrets Management

- Database credentials stored in `.streamlit/secrets.toml` (gitignored)
- Passwords URL-encoded to handle special characters

---

## ⚡ Performance Optimizations

### Caching Strategy

| Function        | Cache Type           | TTL    | Purpose                               |
| --------------- | -------------------- | ------ | ------------------------------------- |
| `get_engine()`  | `@st.cache_resource` | ∞      | Reuse database engine across sessions |
| `get_columns()` | `@st.cache_data`     | 10 min | Avoid repeated schema queries         |
| `load_data()`   | `@st.cache_data`     | 5 min  | Cache query results                   |

### Memory Management

- **Chunked reading**: `pd.read_sql()` with `chunksize=50,000` prevents memory overflow
- **Preview limits**: Dashboard preview defaults to 1,000 rows (full dataset aggregated via SQL)
- **SQL-side aggregation**: Aggregations run in PostgreSQL, not Pandas (reduces data transfer)

### Query Efficiency

- **SQL LIMIT**: Explorer and Dashboard use `LIMIT` for previews
- **Selective columns**: Dashboard queries only needed columns (not `SELECT *` for aggregations)
- **COUNT queries**: Quality reports use `COUNT(*)` and `COUNT(column)` instead of loading full data

---

## 🔗 Dependencies

### Core Stack

- **streamlit** 1.37.1: Web application framework
- **pandas** 2.2.2: Data manipulation and analysis
- **sqlalchemy** 2.0.31: SQL toolkit and ORM
- **psycopg2-binary** 2.9.9: PostgreSQL database adapter
- **plotly** 5.22.0: Interactive visualization library

### Supporting Libraries

- **numpy** 1.26.4: Numerical computing (Pandas dependency)
- **openpyxl** 3.1.5: Excel file reading/writing
- **python-dotenv** 1.0.1: Environment variable management

---

## 🚀 Deployment Architecture

### Current Setup (Production)

- **Frontend**: Streamlit Cloud (`dataset-insight-platform.streamlit.app`)
- **Database**: Supabase PostgreSQL (cloud-hosted)
- **SSL**: Required for all database connections

---

## 🧪 Testing Strategy

### Current State

- **Manual testing**: UI flows tested through Streamlit interface
- **Database validation**: SQL queries tested against real PostgreSQL instance

### Future Enhancements

- Unit tests for backend modules (pytest)
- Integration tests for query_builder.py
- End-to-end tests with test database fixtures

---

## 🎯 Design Decisions

### Why Streamlit?

- Rapid prototyping for data applications
- Built-in widgets reduce development time
- Native caching decorators for performance
- Easy deployment to Streamlit Cloud

### Why PostgreSQL?

- Robust SQL engine for complex JOINs and aggregations
- Handles large datasets efficiently
- Supabase provides free tier with reasonable limits

### Why SQL-Side Aggregation?

- Offloads computation to database (optimized C code)
- Reduces network transfer (only aggregated results sent to frontend)
- Prevents browser memory issues with large datasets

### Why Chunked Loading?

- Prevents out-of-memory errors on large CSV uploads
- Allows progress tracking for long-running uploads
- Compatible with Pandas `.to_sql()` method

---

## 📊 Supported Features Matrix

| Feature                 | Status | Notes                             |
| ----------------------- | ------ | --------------------------------- |
| CSV Upload              | ✅     | UTF-8 encoding, chunked           |
| Excel Upload            | ✅     | .xlsx only (openpyxl engine)      |
| Single-Table Analysis   | ✅     | SUM, AVG, COUNT, MAX, MIN         |
| Multi-Table Analysis    | ✅     | INNER JOIN via relationships      |
| Dynamic GROUP BY        | ✅     | Any column                        |
| Time-Series Aggregation | ✅     | DATE_TRUNC by Day/Month/Year      |
| Bar Charts              | ✅     | Plotly Express                    |
| Line Charts             | ✅     | Plotly Express                    |
| Pie Charts              | ✅     | Plotly Express                    |
| Scatter Plots           | ✅     | Plotly Express                    |
| AI Insights             | ✅     | Statistical summaries             |
| Data Quality Reports    | ✅     | Missing values, unique counts     |
| CSV Export              | ✅     | UTF-8 encoded                     |
| Excel Export            | ⚠️     | Code exists but not exposed in UI |
| Duplicate Removal       | ❌     | Planned (cleaner.py enhancement)  |
| NULL Filling            | ❌     | Planned (cleaner.py enhancement)  |
| Outer JOINs             | ❌     | Only INNER JOIN supported         |

---

## 🛠️ Extension Points

### Adding a New Chart Type

1. Add chart generation logic to `backend/chart_engine.py::create_chart()`
2. Update recommendation logic in `recommend_chart()` if needed
3. Add chart type option in `app/my_pages/dashboard.py`

### Adding a New Aggregation Function

1. Add function name to aggregation dropdown in `analysis.py` and `dashboard.py`
2. No backend changes needed (SQL functions passed directly)

### Adding a New Page

1. Create `app/my_pages/new_page.py` with `show()` function
2. Import and route in `app/main.py`
3. Add navigation option to sidebar radio

### Supporting New File Formats (JSON, Parquet, etc.)

1. Add file type to `upload.py` file_uploader `type` parameter
2. Add conditional reading logic (e.g., `pd.read_json()`, `pd.read_parquet()`)
3. Update documentation

---

## 🐛 Known Limitations

1. **Sleep Mode Delay**: Supabase free tier databases sleep after 1 week of inactivity (30-60s wake time)
2. **No Authentication**: Platform is public; anyone with the link can upload data
3. **Basic Cleaning**: Dataset cleaner doesn't handle duplicates, nulls, or outliers
4. **INNER JOIN Only**: Multi-table analysis doesn't support LEFT/RIGHT/OUTER joins
5. **Single Relationship Per Pair**: Can't define multiple join keys between same two tables
6. **No Query Cancellation**: Long-running queries block the UI (Streamlit limitation)

---

## 📈 Future Roadmap

### High Priority

- [ ] User authentication (login/logout)
- [ ] Private workspaces per user
- [ ] Enhanced dataset cleaner (null handling, duplicate removal)
- [ ] Query history and saved queries
- [ ] Dashboard templates and presets

### Medium Priority

- [ ] LEFT/RIGHT/OUTER JOIN support
- [ ] Calculated columns (formula builder)
- [ ] Scheduled report generation
- [ ] Export to Excel with charts embedded
- [ ] Dark mode theme

### Low Priority

- [ ] Real-time collaboration
- [ ] Dataset versioning
- [ ] API access for programmatic queries
- [ ] Machine learning model integration
- [ ] Natural language query interface (LLM-powered)

---

## 📝 Coding Conventions

### Naming

- **Functions**: `snake_case` (e.g., `get_tables()`)
- **Classes**: `PascalCase` (not used in this project)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_CHUNK_SIZE`)
- **Private functions**: Prefix with underscore (e.g., `_internal_helper()`)

### Comments

- Module docstrings at top of every file
- Function docstrings with Args, Returns, Examples
- Inline comments for complex logic blocks
- Section headers with `# ===` borders

### SQL Style

- **Keywords**: UPPERCASE (`SELECT`, `FROM`, `WHERE`)
- **Identifiers**: Double-quoted (`"table_name"`, `"column_name"`)
- **Indentation**: 4 spaces per level
- **Parameterization**: Always use `:param_name` placeholders

---

## 👤 Contact & Credits

**Author**: Rudrapratap Sarma  
**Institution**: Manipal University Jaipur (BCA Student)  
**GitHub**: [rudrapratap601](https://github.com/rudrapratap601)  
**Live Demo**: [dataset-insight-platform.streamlit.app](https://dataset-insight-platform.streamlit.app/)

**Purpose**: Learning project for full-stack data application development, SQL integration, and interactive dashboard design.

---
