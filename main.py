from terminaltables import AsciiTable
from environs import Env
from head_hunter import get_hh_vacancy_stats
from super_job import get_sj_vacancy_stats

HH_TOP_LIST = [
    'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#',
    'C', 'Go', 'Objective-C', 'Scala', 'Swift', 'TypeScript'
]


def print_table(title, salary_dict):
    headers = [[
        'Язык программирования', 'Вакансий найдено',
        'Вакансий обработано', 'Средняя зарплата'
    ]]
    rows = [[pl, 
             salary_dict[pl]['vacancies_found'], 
             salary_dict[pl]['vacancies_processed'],
             salary_dict[pl]['average_salary']]
            for pl in salary_dict.keys()]
    data = headers + rows
    table_instance = AsciiTable(data, title)
    print(table_instance.table)



def main():
    env = Env()
    env.read_env()
    secret_key = env('SECRET_KEY')

    hh_result = {}
    sj_result = {}
    for pl in HH_TOP_LIST:
        hh_result[pl] = get_hh_vacancy_stats(pl)
        sj_result[pl] = get_sj_vacancy_stats(pl, secret_key)
    print_table('HeadHunter Moscow', hh_result)
    print_table('SuperJob Moscow', sj_result)


if __name__ == '__main__':
    main()
