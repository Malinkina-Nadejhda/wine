import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from text_formatting import get_year_string


WINE_XLSX_FILE = "wine.xlsx"
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"
FOUNDING_DATE = 1920
SERVER_ADDRESS = ('0.0.0.0', 8000)

today = datetime.date.today().year
winery_age = today - FOUNDING_DATE
age_string = f"Уже {winery_age} {get_year_string(winery_age)} с вами"

wine_data_exc = pandas.read_excel(
    WINE_XLSX_FILE,
    na_values=None,
    keep_default_na=False,
)
wine_records = wine_data_exc.to_dict(orient="records")
wines_by_categories = defaultdict(list)
for wine in wine_records:
    category = wine["Категория"]
    wines_by_categories[category].append(wine)

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"])
)

template = env.get_template(TEMPLATE_FILE)

rendered_page= template.render(
    winery_age=age_string,
    wine_data=wines_by_categories,
)

with open(OUTPUT_FILE, 'w', encoding="utf8") as file:
    file.write(rendered_page)

print(f"Сервер запущен на http://localhost:{SERVER_ADDRESS[1]}")
server = HTTPServer(SERVER_ADDRESS, SimpleHTTPRequestHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nСервер остановлен")
    server.server_close()
