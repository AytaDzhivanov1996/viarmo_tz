from bs4 import BeautifulSoup

from config import driver, service, spreadsheet_id

def get_specs(url):
    """Функция получения характеристик через ссылку на карточку товара с Яндекс Маркета"""
    driver.get(url)
    source_code = driver.page_source
    soup = BeautifulSoup(source_code, 'html.parser')
    specs_data = soup.find_all('div', {'class': "_198Aj cXkP_ _3wss4 _1XOOj"})
    specs = {}
    for line in specs_data:
        name = line.find('span', {'class': "_2NZVF _15CQ5 _32rOe _25vcL"}).get_text(strip=True)
        value_code = line.find('div', {'class': "_3K3f3"})
        value = value_code.find('span').get_text(strip=True)
        specs.update({name: value})
    return specs

def write_specs(page):
    """Запись полученных характеристик в Google Sheets"""
    specs = get_specs(page)
    table_data = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "B1:1",
                    "majorDimension": "COLUMNS",
                    "values": [[key] for key in list(specs.keys())]},
                    {"range": "B2:2",
                    "majorDimension": "COLUMNS",
                    "values": [[value] for value in list(specs.values())]}
            ]
            }
        ).execute()
    return table_data