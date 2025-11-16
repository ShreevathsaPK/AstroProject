# AstroProject - Copilot Instructions

## Project Overview
AstroProject is a Vedic astrology analysis platform that aggregates astrological chart data and provides queryable insights. The system has four main phases: (1) data gathering from external sources, (2) data organization into SQLite DB, (3) query execution for astrological pattern analysis, and (4) web deployment for remote access.

## Architecture & Major Components

### Core Data Pipeline
- **`script_to_gen_horoscope_and_stor/dob_to_chart.py`**: ETL engine that creates SQLite schema and populates it from CSV files (personal_info.csv, planet_data.csv)
  - Establishes two related tables: `personal_info` (birth data) and `planet_data` (computed planetary positions, nakshatra, houses)
  - Foreign key relationship: `planet_data.personal_info_id` → `personal_info.id`
- **`chart_generator.py`**: Computes astrological calculations using Swiss Ephemeris library (`swisseph`)
  - Relies on ephemeris files (`de421.bsp`, `seas_18.se1`) for planetary positions
  - Uses Lahiri Ayanamsha (Vedic standard): `swe.set_sid_mode(swe.SIDM_LAHIRI)`
  - Calculates combust status, house placement, nakshatra assignment
  - Sets ephemeris path: `swe.set_ephe_path('/workspace/AstroProject/')`

### Query & Analysis Layer
- **`script_to_gen_horoscope_and_stor/query_script.py`**: Standalone CLI query engine with functions like:
  - `query_planet_by_house_or_sign()`: Search persons by planet placement
  - `query_planet_by_retrograde()`: Retrograde status filtering
  - Uses hardcoded zodiac sign-to-lord mapping (e.g., Aries→Mars, Pisces→Jupiter)
- **`script_to_gen_horoscope_and_stor/dasha_sequence_generator.py`**: Calculates Vimshottari Dasha periods (planetary time cycles)
  - Planetary year cycle: Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17)
  - Recursive calculation of dasha and sub-dasha periods

### Web Interface Layer
- **`script_to_gen_horoscope_and_stor/query_script_with_flask.py`**: Flask API wrapping query functions (REST endpoints for dasha, retrograde, house queries)
- **`script_to_gen_horoscope_and_stor/selenium_script.py`**: Web scraper for external astro sites (e.g., astrotalk.com) using headless Chrome

## Developer Workflows

### Building & Running
```bash
# Local: Default execution
python script_to_gen_horoscope_and_stor/query_script.py

# Docker build (configured for Python 3.6.15)
docker build -t astro-project .

# Docker run with default script
docker run astro-project  # executes run.sh → python query_script.py

# Custom script execution
docker run astro-project python script_to_gen_horoscope_and_stor/dasha_sequence_generator.py
```

### Data Preparation
- Input CSVs must have columns: Name, Date, Time, Place, Latitude, Longitude, Timezone, Sunrise, Sunset, Ayanamsha, Comments
- CSV format is ingested via `dob_to_chart.py` → SQLite tables
- Database file expected at `horoscope.db` (default in `query_script_with_flask.py`)

### Testing
```bash
# Run tests with pytest (only dependency in requirements.txt)
pytest test_test_script.py
```
- Test format: `test_test_script.py` uses subprocess to feed CLI inputs and validate query results

## Project-Specific Patterns

### Database Pattern
- SQLite is the choice (not cloud-based) for portability in Docker
- Schema normalizes personal info from planet data (one-to-many relationship)
- SQL queries use JOINs to correlate birth data with planetary positions

### Astrological Domain Conventions
- **Zodiac Mapping**: Signs mapped to numbers (Aries=1, Pisces=12) for house calculations
- **Combust Ranges**: Define planet-specific degrees (Mercury=8°, Venus=8°, Mars=7°, etc.)
- **Sidereal Ephemeris**: Always use Lahiri Ayanamsha; tropical (tropical==geocentric) is never used
- **House Calculation**: `(planet_sign_num - ascendant_sign_num + 1) % 12` with wrap-around handling

### File Dependencies
- Ephemeris files (`de421.bsp`, `seas_18.se1`) must be in workspace root or `/workspace/AstroProject/` per `chart_generator.py`
- Python 3.6.15 is pinned in Dockerfile (legacy constraint—upgrades require testing combust/dasha logic)

## Integration Points & External Dependencies

| Component | Purpose | Notes |
|-----------|---------|-------|
| `swisseph` | Planetary calculations | Requires BSP/SE1 ephemeris files; uses sidereal mode |
| `selenium` + `webdriver_manager` | Web scraping | Headless Chrome; used for data gathering from astro sites |
| `flask` | HTTP API | Optional—used in `query_script_with_flask.py`; not in main Dockerfile |
| `pandas` | Data manipulation | Used in `chart_generator.py` for Excel/CSV processing |
| `geopy` + `timezonefinder` | Geocoding | Resolves place names to lat/long and timezones |
| `sqlite3` | Database | Standard library; no external installation needed |

## Critical Notes for AI Agents

1. **Ephemeris Path Configuration**: Verify `swe.set_ephe_path()` points to correct location before running chart calculations; Docker default is `/workspace/AstroProject/`
2. **Dasha Period Precision**: Dasha calculations are **recursive and time-dependent**—modifications require testing against sample charts to prevent cumulative errors
3. **CSV→DB Pipeline**: Always validate CSV schema before calling `add_data_from_csv()`; malformed CSVs cause silent failures due to permissive sqlite3 handling
4. **Python 3.6 Constraints**: Some dependencies may be pinned to 3.6-compatible versions; test thoroughly before bumping interpreter version
5. **Zodiac Sign Logic**: Hardcoded mappings in `query_script.py` (zodiac_owners dict) must be updated if query patterns expand beyond current scope
