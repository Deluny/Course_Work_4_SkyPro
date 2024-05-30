import requests

from .base_client import VacancyApiClient
from ..dto import Vacancy, Salary


class HeadHunterAPI(VacancyApiClient):

    def get_vacancies(self, search_text: str) -> list[Vacancy]:
        url = 'https://api.hh.ru/vacancies'
        params = {
            'only_with_salary': True,
            'per_page': 100,
            'text': search_text,
            'currency': 'RUR'
        }

        responce = requests.get(url, params=params, timeout=10)
        if not responce.ok:
            print(f'Ошибка получения данных с hh.ru, {responce.content}')
            return {}

        return [
            self._parse_vacancy_data(item) for item in responce.json()['items']
        ]

    def _parse_vacancy_data(self, data: dict) -> Vacancy:
        return Vacancy(
            name=data['name'],
            url=data['alternate_url'],
            employer_name=data['employer']['name'],
            salary=Salary(
                salary_from=data['salary']['from'],
                salary_to=data['salary']['to'],
                currency=data['salary']['currency']
            )
        )
