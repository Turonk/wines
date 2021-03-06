import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

YEAR_BASE = 1920


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    return template


def get_age_winery():
    winery_age = datetime.datetime.now().year - YEAR_BASE

    if (winery_age % 10) == 1 and (winery_age % 100) != 11:
        numeral_year = 'год'
    elif (winery_age % 10) in [2, 3, 4] and \
            (winery_age % 100) not in [12, 13, 14]:
        numeral_year = 'года'
    else:
        numeral_year = 'лет'
    return winery_age, numeral_year


def main():
    parser = argparse.ArgumentParser(
        description='File in xlsx format with data for the site'
    )
    parser.add_argument('src_file', nargs='?',
                        default='wine', type=str,
                        help='Input data file for the site')
    args = parser.parse_args()

    excel_data_df = pandas.read_excel(
        f'{args.src_file}.xlsx',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    wines = excel_data_df.to_dict(orient='records')

    groups_wines = defaultdict(list)
    for wine in wines:
        groups_wines[wine['Категория']].append(wine)
    groups_wines = sorted(groups_wines.items())

    template = get_template()
    age_winery, numeral_year = get_age_winery()
    rendered_page = template.render(
        assortment=groups_wines,
        years_old=age_winery,
        numeral_year=numeral_year
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
