# Smart Expense Tracker & Budget Management System
**Author:** GOWSIYA KHATUN  
**Version:** 2.0  
**Language:** Python 3.10+

## Quick Start
```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
# Windows:- .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

## Features
- Full CRUD expense management
- Category-wise budget limits with 3-tier alerts
- Matplotlib charts (pie, bar, trend)
- Advanced filter & search
- Recurring expense management
- PDF & CSV export
- Automatic data backup
- 100% offline — no internet required

## Project Structure
```
expense_tracker/
├── main.py               # Entry point
├── expense_manager.py    # CRUD operations
├── budget_manager.py     # Budget & alerts
├── analytics_engine.py   # Charts & stats
├── filter_engine.py      # Search & filter
├── recurring_manager.py  # Recurring expenses
├── report_generator.py   # PDF & CSV export
├── category_manager.py   # Category management
├── storage_utils.py      # File I/O utilities
├── validators.py         # Input validation
├── requirements.txt      # Dependencies
└── data/                 # Auto-created
    ├── expenses.json
    ├── budget_config.json
    ├── categories.json
    ├── recurring.json
    └── backups/
```
