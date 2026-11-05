# ─────────────────────────────────────────────────────────────────────────────
# main.py — Smart Expense Tracker & Budget Management System
# Author : GOWSIYA KHATUN
# Version: 2.0
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        RED=YELLOW=GREEN=CYAN=WHITE=MAGENTA=BLUE=""
    class Style:
        BRIGHT=RESET_ALL=""

from expense_manager import ExpenseManager
from budget_manager import BudgetManager
from analytics_engine import AnalyticsEngine
from filter_engine import FilterEngine
from recurring_manager import RecurringManager
from report_generator import ReportGenerator
from category_manager import CategoryManager

APP_NAME    = "Smart Expense Tracker & Budget Manager"
APP_VERSION = "2.0.0"
APP_AUTHOR  = "GOWSIYA KHATUN"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear()
    print(Fore.CYAN + "=" * 65)
    print(Fore.YELLOW + f"{'':>10}{APP_NAME:^45}")
    print(Fore.CYAN   + f"{'':>15}{'Powered by Python | v' + APP_VERSION:^35}")
    print(Fore.WHITE  + f"{'':>20}{'Author: ' + APP_AUTHOR:^25}")
    print(Fore.CYAN   + "=" * 65)

def pause():
    input(Fore.WHITE + "\n  Press Enter to continue...")

# ── Sub-menus ────────────────────────────────────────────────────────────────

def expense_menu(em, bm):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── EXPENSE MANAGEMENT ──")
        print("  1. Add New Expense")
        print("  2. View All Expenses")
        print("  3. Update Expense")
        print("  4. Delete Expense")
        print("  5. Find Expense by ID")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": em.add(bm);         pause()
        elif choice == "2": em.view_all();       pause()
        elif choice == "3": em.update();         pause()
        elif choice == "4": em.delete();         pause()
        elif choice == "5": em.find_by_id();     pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def budget_menu(bm, em):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── BUDGET MANAGEMENT ──")
        print("  1. Set / Update Budget for a Category")
        print("  2. View Budget Dashboard")
        print("  3. View Budget for Specific Category")
        print("  4. Remove Budget Limit")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": bm.set_budget_interactive();    pause()
        elif choice == "2": bm.dashboard(em);               pause()
        elif choice == "3": bm.view_category_budget(em);    pause()
        elif choice == "4": bm.remove_budget();             pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def analytics_menu(ae):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── ANALYTICS & CHARTS ──")
        print("  1. Category Pie Chart (Current Month)")
        print("  2. Category Pie Chart (Custom Period)")
        print("  3. Monthly Expenditure Bar Chart (12 Months)")
        print("  4. Daily Spending Trend Line (30 Days)")
        print("  5. Category-wise Summary Table")
        print("  6. Monthly Summary Statistics")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": ae.pie_chart();                     pause()
        elif choice == "2": ae.pie_chart_custom();              pause()
        elif choice == "3": ae.bar_chart_monthly();             pause()
        elif choice == "4": ae.trend_line();                    pause()
        elif choice == "5": ae.category_summary_table();        pause()
        elif choice == "6": ae.monthly_summary();               pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def filter_menu(fe, em):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── FILTER & SEARCH ──")
        print("  1. Filter by Date Range")
        print("  2. Filter by Category")
        print("  3. Filter by Amount Range")
        print("  4. Filter by Payment Mode")
        print("  5. Keyword Search (Description)")
        print("  6. Advanced Multi-Filter")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": fe.filter_date_range(em);          pause()
        elif choice == "2": fe.filter_category(em);            pause()
        elif choice == "3": fe.filter_amount_range(em);        pause()
        elif choice == "4": fe.filter_payment_mode(em);        pause()
        elif choice == "5": fe.keyword_search(em);             pause()
        elif choice == "6": fe.advanced_filter(em);            pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def recurring_menu(rm):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── RECURRING EXPENSES ──")
        print("  1. Add Recurring Expense")
        print("  2. View All Recurring Expenses")
        print("  3. View Upcoming Dues (Next 7 Days)")
        print("  4. Process All Due Expenses")
        print("  5. Deactivate Recurring Expense")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": rm.add();               pause()
        elif choice == "2": rm.view_all();           pause()
        elif choice == "3": rm.view_upcoming();      pause()
        elif choice == "4": rm.process_due();        pause()
        elif choice == "5": rm.deactivate();         pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def report_menu(rg):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── EXPORT & REPORTS ──")
        print("  1. Export All Expenses to CSV")
        print("  2. Export Filtered Expenses to CSV")
        print("  3. Generate PDF Financial Report")
        print("  4. Backup All Data Files")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": rg.export_csv();            pause()
        elif choice == "2": rg.export_csv_filtered();   pause()
        elif choice == "3": rg.generate_pdf();          pause()
        elif choice == "4": rg.backup_data();           pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

def category_menu(cm):
    while True:
        display_banner()
        print(Fore.CYAN + "\n  ── CATEGORY MANAGEMENT ──")
        print("  1. View All Categories")
        print("  2. Add Custom Category")
        print("  3. Remove Custom Category")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": cm.view_all();      pause()
        elif choice == "2": cm.add();           pause()
        elif choice == "3": cm.remove();        pause()
        elif choice == "0": break
        else: print(Fore.RED + "  Invalid choice."); pause()

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    em = ExpenseManager()
    bm = BudgetManager()
    ae = AnalyticsEngine(em)
    fe = FilterEngine()
    rm = RecurringManager(em)
    rg = ReportGenerator(em, bm)
    cm = CategoryManager()

    while True:
        display_banner()
        print(Fore.WHITE + "\n  MAIN MENU")
        print(Fore.GREEN  + "  1. Expense Management")
        print(Fore.YELLOW + "  2. Budget Management")
        print(Fore.CYAN   + "  3. Analytics & Charts")
        print(Fore.MAGENTA+ "  4. Filter & Search")
        print(Fore.BLUE   + "  5. Recurring Expenses")
        print(Fore.WHITE  + "  6. Export & Reports")
        print(Fore.WHITE  + "  7. Category Settings")
        print(Fore.RED    + "  0. Exit")
        choice = input(Fore.WHITE + "\n  Enter choice: ").strip()
        if   choice == "1": expense_menu(em, bm)
        elif choice == "2": budget_menu(bm, em)
        elif choice == "3": analytics_menu(ae)
        elif choice == "4": filter_menu(fe, em)
        elif choice == "5": recurring_menu(rm)
        elif choice == "6": report_menu(rg)
        elif choice == "7": category_menu(cm)
        elif choice == "0":
            print(Fore.YELLOW + "\n  Thank you for using Smart Expense Tracker!")
            sys.exit(0)
        else:
            print(Fore.RED + "  Invalid choice. Try again.")
            pause()

if __name__ == "__main__":
    main()
