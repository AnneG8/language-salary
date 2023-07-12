import requests
import time
from itertools import count
from secondary_functions import predict_salary


def predict_rub_salary_hh(vacancy):
    salary = vacancy.get('salary')
    if not salary or salary.get('currency') != 'RUR':
        return
    return predict_salary(salary.get('from'), salary.get('to'))


def get_hh_vacancy_stats(language, area='1', period=30):
    url = 'https://api.hh.ru/vacancies/'
    payload = {
        'text': f'программист {language}',
        'area': area,
        'period': period,
    }
    salaries = list()

    for page in count(0):
        payload['page'] = page
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()
        response_dict = page_response.json()

        for vacancy in response_dict['items']:
            salaries.append(predict_rub_salary_hh(vacancy))

        if page >= response_dict['pages'] - 1:
            break
        time.sleep(0.15)

    salaries = list(filter(None, salaries))

    return {
        'language': language,
        'vacancies_found': response_dict['found'],
        'vacancies_processed': len(salaries),
        'average_salary': (int(sum(salaries) // len(salaries))
                           if salaries else 0)
    }
