import requests
from bs4 import BeautifulSoup

class UepgWrapper():
    def __init__(self, login, password):
        session = requests.Session()

        url = {
            'index': "https://sistemas.uepg.br/academicoonline/login/index",
            'auth': "https://sistemas.uepg.br/academicoonline/login/authenticate",
        }

        user = {'login': login, 'password': password}

        index = session.request("GET", url['index'])

        self.cookie = {'cookie': f'JSESSIONID={requests.utils.dict_from_cookiejar(session.cookies)["JSESSIONID"]}; __utma=241181661.1990841241.1518980587.1520085361.1520277780.4; __utmz=241181661.1518980587.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'}

        auth = session.request("POST", url['auth'], user, headers=self.cookie)
        self.session = session

    def get_table(self):
        url = {'notas': "https://sistemas.uepg.br/academicoonline/avaliacaoDesempenho/index"}

        notas = self.session.request("GET", url['notas'], headers=self.cookie)
        soup = BeautifulSoup(notas.text, 'html.parser')
        table = soup.find('table')

        return table

    def parse_rows(self, rows):
        results = []
        for row in rows:
            table_headers = row.find_all('th')
            if table_headers:
                results.append([headers.get_text() for headers in table_headers])

            table_data = row.find_all('td')
            if table_data:
                results.append([data.get_text() for data in table_data])
        return results

    def parse_table(self):
        table = self.get_table()

        return self.parse_rows(table.find_all('tr'))

    def parse_table_frequency(self):
        table = self.parse_table()

        table_t = list(map(list, zip(*table)))

        table_n = list(zip(table_t[1], table_t[4]))
        dict_n = dict((x, y) for x, y in table_n[1:])

        return dict_n


