from config import service, spreadsheet_id, driver
from services import write_specs

#Получение ссылки из таблицы
yandex_links = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A2:A',
    majorDimension='ROWS'
).execute()
links_list = [link[0] for link in yandex_links['values']]

if __name__ == '__main__':
    for link in links_list:
        write_specs(link)
    driver.close()