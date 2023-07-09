def predict_salary(salary_from, salary_to):
    if not salary_from:
        return salary_to * 0.8
    if not salary_to:
        return salary_from * 1.2
    return (salary_from + salary_to) / 2
