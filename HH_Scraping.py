import json
import requests
import bs4
import fake_headers

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

vacancies = []

def vacancy_parse():
    vacancies_links_soup = soup.findAll('a', attrs={'class': 'bloko-link', 'target': '_blank'})
    for vacancy_link in vacancies_links_soup:
        while vacancies_links_soup.count(vacancy_link) > 1:
            vacancies_links_soup.remove(vacancy_link)
    for vacancy_link in vacancies_links_soup:
        if 'vacancy' in vacancy_link['href']:
            response_vacancy = requests.get(vacancy_link['href'], headers=gen_headers())
            html_data_vacancy = response_vacancy.text
            soup_vacancy = bs4.BeautifulSoup(html_data_vacancy, "lxml")
            vacancy_description = soup_vacancy.find('div', attrs = {'data-qa': 'vacancy-description'})
            if vacancy_description != None:
                if 'Django' in vacancy_description.text and 'Flask' in vacancy_description.text:
                    vacancy_name = soup_vacancy.find('h1', attrs = {'data-qa': 'vacancy-title', 'class': 'bloko-header-section-1'})
                    vacancy_company_name = soup_vacancy.find('span', attrs = {'data-qa': 'bloko-header-2', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
                    city_name = soup_vacancy.find('span', attrs = {'data-qa': 'vacancy-view-raw-address'})
                    if city_name == None:
                        city_name = soup_vacancy.find('p', attrs={'data-qa': 'vacancy-view-location'})
                    vacancy_salary = soup_vacancy.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-gross',
                                                                    'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
                    if vacancy_salary == None:
                        vacancy_salary = soup_vacancy.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-net',
                                                                        'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
                    if vacancy_salary == None: vacancy_salary = "не указана"
                    else: vacancy_salary = vacancy_salary.text
                    vacancies.append("--------------------------------------------------------")
                    vacancies.append(f'Требуется "{vacancy_name.text}" в "{vacancy_company_name.text}"')
                    vacancies.append("Ссылка - " + vacancy_link['href'])
                    vacancies.append(f'Зарплата: {vacancy_salary}')
                    vacancies.append(f'Адрес: {city_name.text}')


response = requests.get("https://spb.hh.ru/search/vacancy",
                        params={'L_save_area': 'true',
                                'text': 'Python',
                                'currency_code': 'USD',
                                'area': '1'},
                        headers=gen_headers())
html_data = response.text
soup = bs4.BeautifulSoup(html_data, "lxml")
vacancy_parse()

response = requests.get("https://spb.hh.ru/search/vacancy",
                        params={'L_save_area': 'true',
                                'text': 'Python',
                                'currency_code': 'USD',
                                'area': '2'},
                        headers=gen_headers())
html_data = response.text
soup = bs4.BeautifulSoup(html_data, "lxml")
vacancy_parse()

with open("Вакансии.json", "w", encoding="utf-8") as f:
    json.dump(vacancies,f,indent=4,ensure_ascii=False)