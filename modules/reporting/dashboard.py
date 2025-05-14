from fastapi import APIRouter, Request
from jinja2 import Environment, FileSystemLoader
import plotly.graph_objs as go
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

env = Environment(loader=FileSystemLoader('templates'))

@router.get('/dashboard')
async def dashboard(request: Request, db: AsyncSession):
    result = await db.execute('SELECT status, COUNT(*) FROM recognition_events GROUP BY status')
    data = result.fetchall()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    graph = fig.to_html(full_html=False)
    template = env.get_template('dashboard.html')
    return template.render(request=request, graph=graph)