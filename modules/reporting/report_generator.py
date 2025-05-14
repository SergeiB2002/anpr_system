from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import openpyxl
import asyncio

async def generate_daily_pdf(records, output_path):
    doc = SimpleDocTemplate(output_path)
    data = [[r.plate, r.ts, r.status] for r in records]
    t = Table([['Plate','Time','Status']] + data)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.grey)]))
    doc.build([t])

async def generate_daily_xlsx(records, output_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Plate','Time','Status'])
    for r in records:
        ws.append([r.plate, r.ts.isoformat(), r.status])
    wb.save(output_path)