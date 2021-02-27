import plotly
from flask import Blueprint, render_template, json
from flask_login import current_user
import matplotlib.pyplot as plt

from dash_app.recyclingchart import RecyclingChart
from dash_app.recyclingdata import RecyclingData

main_bp = Blueprint('main', __name__)


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.firstname
    return render_template('index.html', title='Home page', name=name)


@main_bp.route('/mpl')
def mpl():
    data = RecyclingData()
    data.process_data_for_area('London')
    url = create_mpl_chart(period='2018/19', data=data)
    return render_template('chart_mpl.html', url=url, title="Matplotlib chart")


@main_bp.route('/px')
def px():
    plot = create_px_chart('London')
    return render_template('chart_px.html', plot=plot, title="Plotly Express chart")


def create_mpl_chart(period, data):
    data = data.recycling
    data = data.loc[data['Year'] == period]
    data = data.sort_values('Recycling_Rates', ascending=False)
    x = data['Area']
    y = data['Recycling_Rates']
    fig = plt.figure()
    ax = fig.subplots()
    ax.barh(x, y)
    ax.set_title(f'Recycling by area in {period}')
    ax.set_xlabel('Area')
    ax.set_ylabel('Recycling Rate')
    ax.tick_params(axis='x', labelsize='small')
    plt.tight_layout()
    url = 'static/img/plot.png'
    fig.savefig(url)
    return url


def create_px_chart(area):
    data = RecyclingData()
    data.process_data_for_area(area)
    rc = RecyclingChart(data)
    fig = rc.create_chart(area)
    # Encode the plot as JSON
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
