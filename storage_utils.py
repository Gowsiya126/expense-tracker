import json, os, shutil
from datetime import datetime

DATA_DIR   = os.path.join(os.path.dirname(__file__), 'data')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

def _ensure():
    os.makedirs(DATA_DIR,   exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def read_json(path):
    _ensure()
    filename = os.path.basename(path)
    if not os.path.exists(path):
        return [] if 'expense' in filename or 'recurring' in filename else {}
    with open(path, 'r', encoding='utf-8') as f:
        try:    return json.load(f)
        except: return [] if 'expense' in filename or 'recurring' in filename else {}

def write_json(path, data):
    _ensure()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

def backup_all():
    _ensure()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    count = 0
    for fn in ['expenses.json','budget_config.json','categories.json','recurring.json']:
        src = os.path.join(DATA_DIR, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BACKUP_DIR, f'{ts}_{fn}'))
            count += 1
    return ts, count
