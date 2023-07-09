import requests
from secondary_functions import predict_salary

def predict_rub_salary_sj(vacancy):
    currency = vacancy.get('currency')
    if currency and currency != 'rub':
        return
    return predict_salary(vacancy.get('payment_from'), 
                          vacancy.get('payment_to'))


def get_sj_vacancy_stats(pl, secret_key, town = 4):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }
    payload = {
        'catalogues': 33,
        'keyword': f'программист {pl}',
        'town': town,
        'count': 100
    }
    salaries = list()

    for page in range(5):
        payload['page'] = page
        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()

        for obj in page_response.json()['objects']:
            salaries.append(predict_rub_salary_sj(obj))

        if not page_response.json()['more']:
            break

    salaries = list(filter(None, salaries))

    return {
        'language': pl,
        'vacancies_found': page_response.json()['total'],
        'vacancies_processed': len(salaries),
        'average_salary': (int(sum(salaries) // len(salaries))
                           if salaries else 0)
    }
