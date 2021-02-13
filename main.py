import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

parser = argparse.ArgumentParser(
    description='File in xlsx format with data for the site')
parser.add_argument('src_file', nargs='?', default='wine', type=str,
                    help='Input data file for the site')
args = parser.parse_args()

YEAR_BASE = 1920
age_winery = datetime.datetime.now().year - YEAR_BASE

if (age_winery % 10) == 1 and (age_winery % 100) != 11:
    numeral_year = 'год'
elif (age_winery % 10) in [2, 3, 4] and (age_winery % 100) not in [12, 13, 14]:
    numeral_year = 'года'
else:
    numeral_year = 'лет'

excel_data_df = pandas.read_excel(f'{args.src_file}.xlsx',
                                  na_values=['N/A', 'NA'],
                                  keep_default_na=False)

wines = excel_data_df.to_dict(orient='records')
groups_wines = defaultdict(list)
for wine in wines:
    groups_wines[wine['Категория']].append(wine)

rendered_page = template.render(groups=groups_wines, years_old=age_winery,
                                numeral_year=numeral_year)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
