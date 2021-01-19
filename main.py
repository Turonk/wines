from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint

import datetime
import pandas

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

# Расчет количества лет в заголовок
start = datetime.datetime(year=1920, month=1, day=1)
now = datetime.datetime.now()

delta = now - start
delta = int(delta.days // 365)

# Считывание таблицы вин
excel_data_df = pandas.read_excel('wine2.xlsx')  # ,usecols=['Название', 'Сорт', 'Цена', 'Картинка'])

wines = excel_data_df.to_dict(orient='records')
groups_wines = defaultdict(list)
for wine in wines:
    groups_wines[wine['Категория']].append(wine)

#pprint(groups_wines)

#print(groups_wines.keys())
rendered_page = template.render(groups=groups_wines, years_old=delta)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
