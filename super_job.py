import requests
import math
from secondary_functions import predict_salary


def predict_rub_salary_sj(vacancy):
    currency = vacancy.get('currency')
    if currency and currency != 'rub':
        return
    return predict_salary(vacancy.get('payment_from'),
                          vacancy.get('payment_to'))


def get_sj_vacancy_stats(language, secret_key, town=4, page_dimension=100):
    max_vacancies = 500
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }
    payload = {
        'catalogues': 33,
        'keyword': f'программист {language}',
        'town': town,
        'count': page_dimension
    }
    salaries = list()

    for page in range(math.ceil(max_vacancies / page_dimension)):
        payload['page'] = page
        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        response_dict = page_response.json()

        for vacancy in response_dict['objects']:
            salaries.append(predict_rub_salary_sj(vacancy))

        if not response_dict['more']:
            break

    salaries = list(filter(None, salaries))

    return {
        'language': language,
        'vacancies_found': response_dict['total'],
        'vacancies_processed': len(salaries),
        'average_salary': (int(sum(salaries) // len(salaries))
                           if salaries else 0)
    }
