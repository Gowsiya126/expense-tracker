from colorama import Fore
from tabulate import tabulate

class FilterEngine:

    def _display(self, em, results, title="FILTER RESULTS"):
        if not results:
            print(Fore.YELLOW+f"\n  No records matched the filter."); return
        em.view_all(results, title=title)

    def filter_date_range(self, em):
        start = input("  Start date [YYYY-MM-DD]: ").strip()
        end   = input("  End date   [YYYY-MM-DD]: ").strip()
        res   = [e for e in em.expenses if start <= e['date'] <= end]
        self._display(em, res, f"DATE RANGE: {start} → {end}")

    def filter_category(self, em):
        cats = em.cm.get_all()
        for i, c in enumerate(cats, 1): print(f"  {i:>2}. {c}")
        try:
            idx = int(input("  Select category: "))-1
            cat = cats[idx]
        except (ValueError, IndexError):
            print(Fore.RED+"  Invalid."); return
        res = [e for e in em.expenses if e['category'].lower()==cat.lower()]
        self._display(em, res, f"CATEGORY: {cat}")

    def filter_amount_range(self, em):
        try:
            lo = float(input("  Min amount (INR): "))
            hi = float(input("  Max amount (INR): "))
        except ValueError:
            print(Fore.RED+"  Invalid amount."); return
        res = [e for e in em.expenses if lo <= e['amount'] <= hi]
        self._display(em, res, f"AMOUNT: INR {lo:,.2f} – INR {hi:,.2f}")

    def filter_payment_mode(self, em):
        modes = ['Cash','UPI','Card','NetBanking','Cheque','Other']
        for i, m in enumerate(modes, 1): print(f"  {i}. {m}")
        try:
            idx  = int(input("  Select mode: "))-1
            mode = modes[idx]
        except (ValueError, IndexError):
            print(Fore.RED+"  Invalid."); return
        res = [e for e in em.expenses if e['payment_mode'].lower()==mode.lower()]
        self._display(em, res, f"PAYMENT MODE: {mode}")

    def keyword_search(self, em):
        kw = input("  Search keyword: ").strip().lower()
        if not kw: print(Fore.RED+"  Empty keyword."); return
        res = [e for e in em.expenses if kw in e['description'].lower()
               or kw in e['category'].lower()]
        self._display(em, res, f"KEYWORD: '{kw}'")

    def advanced_filter(self, em):
        print(Fore.CYAN+"\n  ── ADVANCED FILTER (leave blank to skip) ──")
        params = {}
        s = input("  Start date [YYYY-MM-DD]: ").strip()
        e = input("  End date   [YYYY-MM-DD]: ").strip()
        if s: params['start'] = s
        if e: params['end']   = e
        cat = input("  Category (or blank): ").strip()
        if cat: params['category'] = cat
        lo = input("  Min amount (or blank): ").strip()
        hi = input("  Max amount (or blank): ").strip()
        if lo:
            try: params['min'] = float(lo)
            except: pass
        if hi:
            try: params['max'] = float(hi)
            except: pass
        mode = input("  Payment mode (or blank): ").strip()
        if mode: params['mode'] = mode
        kw = input("  Keyword (or blank): ").strip()
        if kw: params['kw'] = kw.lower()

        res = list(em.expenses)
        if 'start' in params and 'end' in params:
            res = [x for x in res if params['start'] <= x['date'] <= params['end']]
        if 'category' in params:
            res = [x for x in res if x['category'].lower()==params['category'].lower()]
        if 'min' in params:
            res = [x for x in res if x['amount'] >= params['min']]
        if 'max' in params:
            res = [x for x in res if x['amount'] <= params['max']]
        if 'mode' in params:
            res = [x for x in res if x['payment_mode'].lower()==params['mode'].lower()]
        if 'kw' in params:
            res = [x for x in res if params['kw'] in x['description'].lower()]
        self._display(em, res, "ADVANCED FILTER RESULTS")
