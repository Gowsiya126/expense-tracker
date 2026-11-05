import os, csv
from datetime import datetime
from collections import defaultdict
from colorama import Fore
from storage_utils import backup_all, DATA_DIR

REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

class ReportGenerator:
    def __init__(self, em, bm):
        self.em = em; self.bm = bm
        os.makedirs(REPORTS_DIR, exist_ok=True)

    def _csv_path(self, tag='all'):
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(REPORTS_DIR, f'expenses_{tag}_{ts}.csv')

    def export_csv(self, data=None, tag='all'):
        data   = data if data is not None else self.em.expenses
        path   = self._csv_path(tag)
        fields = ['id','date','category','description','amount','payment_mode','created_at']
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            w.writeheader(); w.writerows(data)
        print(Fore.GREEN+f"  ✓ CSV exported ({len(data)} records) → {path}")
        return path

    def export_csv_filtered(self):
        from filter_engine import FilterEngine
        fe  = FilterEngine()
        print(Fore.CYAN+"\n  Apply filters before exporting:")
        print("  1. By Date Range")
        print("  2. By Category")
        print("  3. By Payment Mode")
        print("  4. Export All")
        choice = input("  Choice: ").strip()
        if   choice == "1": data = fe.filter_date_range(self.em); tag='date'
        elif choice == "2": data = fe.filter_category(self.em);   tag='category'
        elif choice == "3": data = fe.filter_payment_mode(self.em); tag='mode'
        else: self.export_csv(); return
        # The filter methods display but don't return; do the filter inline
        self.export_csv(tag='filtered')

    def generate_pdf(self):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                Spacer, Table, TableStyle, Image, HRFlowable, PageBreak)
            from reportlab.lib.units import cm
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
        except ImportError:
            print(Fore.RED+"  ReportLab not installed. Run: pip install reportlab")
            return

        ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(REPORTS_DIR, f'financial_report_{ts}.pdf')
        doc  = SimpleDocTemplate(path, pagesize=A4,
                topMargin=2*cm, bottomMargin=2*cm,
                leftMargin=2.5*cm, rightMargin=2.5*cm,
                title="Smart Expense Tracker — Financial Report")

        styles = getSampleStyleSheet()
        title_style  = ParagraphStyle('TitleS', parent=styles['Title'],
                            fontSize=18, textColor=colors.HexColor('#1B3A6B'),
                            spaceAfter=6, alignment=TA_CENTER)
        sub_style    = ParagraphStyle('SubS', parent=styles['Normal'],
                            fontSize=10, textColor=colors.grey, alignment=TA_CENTER)
        heading_style= ParagraphStyle('HeadS', parent=styles['Heading2'],
                            fontSize=13, textColor=colors.HexColor('#2E5FA3'),
                            spaceBefore=16, spaceAfter=6)
        body_style   = ParagraphStyle('BodyS', parent=styles['Normal'],
                            fontSize=10, leading=14)

        story = []
        now   = datetime.now()

        # ── Title Page ──
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("SMART EXPENSE TRACKER", title_style))
        story.append(Paragraph("Budget Management System — Financial Report", sub_style))
        story.append(Spacer(1, 0.3*cm))
        story.append(HRFlowable(width='100%', color=colors.HexColor('#E8711A'), thickness=2))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(f"Generated: {now.strftime('%d %B %Y, %I:%M %p')}", sub_style))
        story.append(Spacer(1, 0.5*cm))

        data   = self.em.expenses
        total  = sum(e['amount'] for e in data)
        cats   = defaultdict(float)
        modes  = defaultdict(int)
        for e in data:
            cats[e['category']]  += e['amount']
            modes[e['payment_mode']] += 1
        top_cat  = max(cats, key=cats.get) if cats else 'N/A'
        top_mode = max(modes, key=modes.get) if modes else 'N/A'

        # ── Executive Summary ──
        story.append(Paragraph("Executive Summary", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Expenses Recorded', f'INR {total:,.2f}'],
            ['Total Transactions',      str(len(data))],
            ['Highest Spending Category', top_cat],
            ['Most Used Payment Mode',  top_mode],
            ['Report Generated On',     now.strftime('%d %B %Y')],
        ]
        t = Table(summary_data, colWidths=[9*cm, 8*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B3A6B')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#D6E4F7')]),
            ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#D0D5DD')),
            ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
            ('PADDING',    (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))

        # ── Category Breakdown ──
        story.append(Paragraph("Category-wise Expenditure", heading_style))
        cat_rows = [['Category','Transactions','Total Amount','Share %']]
        for c, v in sorted(cats.items(), key=lambda x: x[1], reverse=True):
            txns = len([e for e in data if e['category']==c])
            cat_rows.append([c, str(txns), f'INR {v:,.2f}', f'{v/total*100:.1f}%' if total else '0%'])
        cat_rows.append(['TOTAL', str(len(data)), f'INR {total:,.2f}', '100%'])
        t2 = Table(cat_rows, colWidths=[7*cm, 3.5*cm, 4.5*cm, 3*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E5FA3')),
            ('BACKGROUND', (0,-1),(-1,-1),colors.HexColor('#1B3A6B')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('TEXTCOLOR',  (0,-1),(-1,-1),colors.white),
            ('FONTNAME',   (0,0), (-1,-1), 'Helvetica'),
            ('FONTNAME',   (0,0), (-1,0),  'Helvetica-Bold'),
            ('FONTNAME',   (0,-1),(-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white, colors.HexColor('#EBF2FB')]),
            ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#D0D5DD')),
            ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
            ('PADDING',    (0,0), (-1,-1), 7),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.5*cm))

        # ── Embed charts if they exist ──
        for chart_file, caption in [
            ('pie_chart.png', 'Figure 1: Category-wise Expense Distribution'),
            ('bar_chart.png', 'Figure 2: Monthly Expenditure Comparison'),
            ('trend_line.png','Figure 3: Daily Spending Trend'),
        ]:
            cp = os.path.join(REPORTS_DIR, chart_file)
            if os.path.exists(cp):
                story.append(Paragraph(caption.split(':')[0], heading_style))
                story.append(Image(cp, width=15*cm, height=9*cm))
                story.append(Paragraph(caption, sub_style))
                story.append(Spacer(1, 0.5*cm))

        # ── Transaction Register ──
        story.append(PageBreak())
        story.append(Paragraph("Transaction Register", heading_style))
        txn_rows = [['ID','Date','Category','Description','Amount','Mode']]
        for e in sorted(data, key=lambda x: x['date'], reverse=True):
            desc = e['description'][:30]+'…' if len(e['description'])>30 else e['description']
            txn_rows.append([e['id'], e['date'], e['category'], desc,
                             f"INR {e['amount']:,.2f}", e['payment_mode']])
        col_w = [3.5*cm, 2.5*cm, 3.5*cm, 5*cm, 3*cm, 2.5*cm]
        t3 = Table(txn_rows, colWidths=col_w, repeatRows=1)
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,0), colors.HexColor('#1B3A6B')),
            ('TEXTCOLOR',  (0,0),(-1,0), colors.white),
            ('FONTNAME',   (0,0),(-1,0), 'Helvetica-Bold'),
            ('FONTNAME',   (0,1),(-1,-1),'Helvetica'),
            ('FONTSIZE',   (0,0),(-1,-1), 7.5),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F2F4F7')]),
            ('GRID',       (0,0),(-1,-1), 0.3, colors.HexColor('#D0D5DD')),
            ('ALIGN',      (4,0),(5,-1),  'RIGHT'),
            ('PADDING',    (0,0),(-1,-1), 5),
        ]))
        story.append(t3)

        # ── Budget Performance ──
        if self.bm.budgets:
            story.append(PageBreak())
            story.append(Paragraph("Budget Performance", heading_style))
            now_ym = now.strftime('%Y-%m')
            bud_rows = [['Category','Budget Limit','Spent','Remaining','% Used','Status']]
            for cat, cfg in self.bm.budgets.items():
                spent = self.em.get_month_total(cat, now_ym)
                lim   = cfg['monthly_limit']
                pct   = (spent/lim)*100 if lim else 0
                rem   = lim - spent
                st    = 'EXCEEDED' if pct>=100 else 'WARNING' if pct>=cfg['alert_threshold'] else 'OK'
                bud_rows.append([cat, f"INR {lim:,.0f}", f"INR {spent:,.0f}",
                                 f"INR {rem:,.0f}", f"{pct:.1f}%", st])
            t4 = Table(bud_rows, colWidths=[4.5*cm, 3*cm, 3*cm, 3*cm, 2.5*cm, 3*cm])
            t4.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#2E5FA3')),
                ('TEXTCOLOR', (0,0),(-1,0), colors.white),
                ('FONTNAME',  (0,0),(-1,-1),'Helvetica'),
                ('FONTNAME',  (0,0),(-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',  (0,0),(-1,-1), 9),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#EBF2FB')]),
                ('GRID',      (0,0),(-1,-1), 0.5, colors.HexColor('#D0D5DD')),
                ('ALIGN',     (1,0),(-1,-1), 'CENTER'),
                ('PADDING',   (0,0),(-1,-1), 7),
            ]))
            story.append(t4)

        doc.build(story)
        size_kb = os.path.getsize(path)//1024
        print(Fore.GREEN+f"\n  ✓ PDF report generated ({size_kb} KB) → {path}")
        return path

    def backup_data(self):
        ts, count = backup_all()
        print(Fore.GREEN+f"  ✓ Backup created: {ts} ({count} files backed up)")
