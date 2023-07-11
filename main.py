from terminaltables import AsciiTable
from environs import Env
from head_hunter import get_hh_vacancy_stats
from super_job import get_sj_vacancy_stats
HH_TOP_LIST = [
    'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#',
    'C', 'Go', 'Objective-C', 'Scala', 'Swift', 'TypeScript'
]


def print_salary_table(title, salary_dict):
    salary_headers = [[
        'Язык программирования', 'Вакансий найдено',
        'Вакансий обработано', 'Средняя зарплата'
    ]]
    salary_rows = [[pl,
                    salary_dict[pl]['vacancies_found'],
                    salary_dict[pl]['vacancies_processed'],
                    salary_dict[pl]['average_salary']]
            for pl in salary_dict.keys()]
    salary_table = salary_headers + salary_rows
    table_instance = AsciiTable(salary_table, title)
    print(table_instance.table)


def main():
    env = Env()
    env.read_env()
    sj_secret_key = env('SJ_SECRET_KEY')

    hh_salaries = {}
    sj_salaries = {}
    for language in HH_TOP_LIST:
        hh_salaries[language] = get_hh_vacancy_stats(language)
        sj_salaries[language] = get_sj_vacancy_stats(language, sj_secret_key)
    print_salary_table('HeadHunter Moscow', hh_salaries)
    print_salary_table('SuperJob Moscow', sj_salaries)


if __name__ == '__main__':
    main()
