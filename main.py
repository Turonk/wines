from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

excel_data_df = pandas.read_excel('wine.xlsx', usecols=['Название', 'Сорт', 'Цена', 'Картинка'])

#print('Excel Sheet to JSON:', excel_data_df.to_dict(orient='records'))
template = env.get_template('template.html')
start = datetime.datetime(year = 1920, month = 1, day =1 )
now = datetime.datetime.now()

delta = now - start
delta =  int(delta.days//365.25)

#    wine1_name="Белая леди",
#    wine1_grade="Дамский пальчик",
#    wine1_price="399 р.",
#    wine1_img="images/belaya_ledi.png",
    
#    wine2_name="Изабелла",
#    wine2_grade="Изабелла",
#    wine2_price="350 р.",
#    wine2_img="images/izabella.png",
    
#    wine3_name="Гранатовый браслет",
#    wine3_grade="Мускат розовый",
#    wine3_price="350 р.",
#    wine3_img="images/granatovyi_braslet.png",
    
#    wine4_name="Шардоне",
#    wine4_grade="Шардоне",
#    wine4_price="320 р.",
#    wine4_img="images/shardone.png",
    
#    wine5_name="Ркацители",
#    wine5_grade="Ркацители",
#    wine5_price="499 р.",
#    wine5_img="images/rkaciteli.png",
    
#    wine6_name="Хванчкара",
#    wine6_grade="Александраули",
#    wine6_price="550 р.",
#    wine6_img="images/hvanchkara.png",

wines =excel_data_df.to_dict(orient='records')

rendered_page = template.render(wines = wines)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()