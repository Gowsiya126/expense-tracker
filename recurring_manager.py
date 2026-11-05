import os
from datetime import datetime, timedelta
from colorama import Fore
from tabulate import tabulate
from storage_utils import read_json, write_json, DATA_DIR

REC_FILE = os.path.join(DATA_DIR, 'recurring.json')
FREQS    = ['daily','weekly','monthly','annual']

def _next_due(current_str, freq):
    dt = datetime.strptime(current_str, '%Y-%m-%d')
    if   freq == 'daily':   dt += timedelta(days=1)
    elif freq == 'weekly':  dt += timedelta(weeks=1)
    elif freq == 'monthly':
        m = dt.month % 12 + 1
        y = dt.year + (1 if dt.month == 12 else 0)
        import calendar
        d = min(dt.day, calendar.monthrange(y, m)[1])
        dt = dt.replace(year=y, month=m, day=d)
    elif freq == 'annual':  dt = dt.replace(year=dt.year+1)
    return dt.strftime('%Y-%m-%d')

class RecurringManager:
    def __init__(self, em):
        self.em        = em
        self.recurring = read_json(REC_FILE)

    def _save(self):
        write_json(REC_FILE, self.recurring)

    def _gen_id(self):
        return f'REC-{len(self.recurring)+1:03d}'

    def add(self):
        print(Fore.CYAN+"\n  ── ADD RECURRING EXPENSE ──")
        name = input("  Name (e.g. Netflix): ").strip()
        if not name: print(Fore.RED+"  Name required."); return
        try:
            amount = float(input("  Amount (INR): "))
            if amount <= 0: raise ValueError
        except ValueError:
            print(Fore.RED+"  Invalid amount."); return
        cats = self.em.cm.get_all()
        for i, c in enumerate(cats, 1): print(f"  {i:>2}. {c}")
        try:
            cat = cats[int(input("  Category: "))-1]
        except (ValueError, IndexError):
            print(Fore.RED+"  Invalid."); return
        for i, f in enumerate(FREQS, 1): print(f"  {i}. {f}")
        try:
            freq = FREQS[int(input("  Frequency: "))-1]
        except (ValueError, IndexError):
            print(Fore.RED+"  Invalid."); return
        start = input("  Start date [YYYY-MM-DD] (blank=today): ").strip()
        if not start: start = datetime.now().strftime('%Y-%m-%d')
        record = {
            'id': self._gen_id(), 'name': name, 'amount': round(amount,2),
            'category': cat, 'frequency': freq, 'start_date': start,
            'next_due': start, 'is_active': True,
            'created_at': datetime.now().isoformat()
        }
        self.recurring.append(record)
        self._save()
        print(Fore.GREEN+f"  ✓ Recurring '{name}' added (INR {amount:,.2f} / {freq})")

    def view_all(self):
        if not self.recurring:
            print(Fore.YELLOW+"  No recurring expenses configured."); return
        today = datetime.now().strftime('%Y-%m-%d')
        rows = []
        for r in self.recurring:
            due   = r['next_due']
            days  = (datetime.strptime(due,'%Y-%m-%d') - datetime.now()).days
            st    = Fore.GREEN+"Active" if r['is_active'] else Fore.RED+"Inactive"
            due_s = (Fore.RED if days <= 0 else Fore.YELLOW if days <= 3 else "")+due
            rows.append([r['id'], r['name'], r['category'],
                         f"INR {r['amount']:,.2f}", r['frequency'], due_s, st])
        print(Fore.CYAN+"\n  ── ALL RECURRING EXPENSES ──")
        print(tabulate(rows, headers=['ID','Name','Category','Amount','Freq','Next Due','Status'],
                       tablefmt='fancy_grid'))

    def view_upcoming(self, days=7):
        today    = datetime.now().date()
        deadline = today + timedelta(days=days)
        upcoming = [r for r in self.recurring
                    if r['is_active'] and
                    today <= datetime.strptime(r['next_due'],'%Y-%m-%d').date() <= deadline]
        if not upcoming:
            print(Fore.GREEN+f"\n  No recurring dues in the next {days} days."); return
        upcoming.sort(key=lambda x: x['next_due'])
        rows = []
        for r in upcoming:
            d    = (datetime.strptime(r['next_due'],'%Y-%m-%d').date() - today).days
            note = "TODAY!" if d==0 else f"in {d} day(s)"
            rows.append([r['id'], r['name'], f"INR {r['amount']:,.2f}", r['frequency'], r['next_due'], note])
        print(Fore.YELLOW+f"\n  ── UPCOMING DUES (Next {days} Days) ──")
        print(tabulate(rows, headers=['ID','Name','Amount','Freq','Due Date','When'], tablefmt='fancy_grid'))

    def process_due(self):
        today = datetime.now().strftime('%Y-%m-%d')
        count = 0
        for r in self.recurring:
            if not r['is_active']: continue
            if r['next_due'] <= today:
                self.em.expenses.append({
                    'id': self.em._gen_id(),
                    'amount': r['amount'], 'category': r['category'],
                    'description': f"[Auto] Recurring: {r['name']}",
                    'date': r['next_due'], 'payment_mode': 'Auto',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                })
                r['next_due'] = _next_due(r['next_due'], r['frequency'])
                count += 1
        if count:
            self.em._save()
            self._save()
            print(Fore.GREEN+f"  ✓ {count} recurring expense(s) processed.")
        else:
            print(Fore.YELLOW+"  No dues to process today.")

    def deactivate(self):
        active = [r for r in self.recurring if r['is_active']]
        if not active:
            print(Fore.YELLOW+"  No active recurring expenses."); return
        for i, r in enumerate(active, 1):
            print(f"  {i}. {r['name']} — INR {r['amount']:,.2f} / {r['frequency']}")
        try:
            idx = int(input("  Select to deactivate: "))-1
            rec = active[idx]
        except (ValueError, IndexError):
            print(Fore.RED+"  Invalid."); return
        rec['is_active'] = False
        self._save()
        print(Fore.GREEN+f"  ✓ '{rec['name']}' deactivated.")
