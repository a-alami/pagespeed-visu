from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
import datetime, pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pagespeed"]
scores_col = db["scores"]
urls_col = db["urls"]

pages = {url_doc['page_name']: url_doc['url'] for url_doc in urls_col.find()}

x, y = range(5), range(10, 60, 10)
source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(tools="crosshair,pan,reset,save,wheel_zoom")
plot.line('x', 'y', source=source)

def update(attrname, old, new):
    platform = platform_drop.value
    page = page_drop.value
    print "Im here", {'platform': platform, 'page': page}
    docs = scores_col.find({'platform': platform, 'page': page})
    ti, sc = [], []
    for doc in docs:
        ti.append((doc['timestamp'].year*100 + doc['timestamp'].month) * 100 +doc['timestamp'].day)
        sc.append(doc['score'])
    source.data = dict(x=ti, y=sc)

# Set up widgets
platform_drop = Select(title='platform', value='Desktop', options=['desktop', 'moblie'])
platform_drop.on_change('value', update)

page_drop = Select(title='page', value='home_page', options=pages.keys())
page_drop.on_change('value', update)

# Set up layouts and add to document
inputs = column(platform_drop, page_drop)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "page"
