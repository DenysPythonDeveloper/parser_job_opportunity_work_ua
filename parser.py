from bs4 import BeautifulSoup
import requests
import lxml
import csv


class Work:
    """ Parsing the site Work.ua """

    def __init__(self, url):
        self.url = url
        self.headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/81.0.4044.138 Safari/537.36',
                        'accept': '*/*'
                        }
        self.host = 'https://www.work.ua'
        self.html = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.html.text, 'lxml')
        self.FILE_NAME = 'Job.csv'


    def file_entry(self, job_opportunity):
        with open(self.FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Вакансия', 'Ссылка', 'Название компании'])
            for job in job_opportunity:
                writer.writerow([job['title'], job['href'], job['company_name']])
        return 'Запись выполнена успешно!'


    def page_pagination_parser(self):
        pagination = self.soup.find_all('ul', class_='pagination hidden-xs')

        if pagination:
            pagination_number = pagination[-1].get_text()
            pagination_number = pagination_number.split()
            del pagination_number[-1]
            print(pagination_number)
            return pagination_number[-1]
        else:
            pagination_number = 1
            return pagination_number


    def main_parser(self, args):
        if self.html.status_code == 200:
            pagination_number = self.page_pagination_parser()
            job_opportunity = []

            for page in range(1, int(pagination_number) + 1):
                html = requests.get(args + f'?page={page}', headers=self.headers)
                print(args + f'?page={page}')
                soup = BeautifulSoup(html.text, 'lxml')
                cards = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')

                for item in cards:
                    job_opportunity.append({
                    'title': item.find('h2', class_='').find_next('a').get_text(),
                    'href': self.host + item.find('h2', class_='').find_next('a').get('href'),
                    'company_name': item.find('div', class_='add-top-xs').find_next('span').get_text()
                    })
        return self.file_entry(job_opportunity)


    def main_run(self, args):
        print(self.main_parser(args))


if __name__ == '__main__':
    url = 'https://www.work.ua/jobs-python/'
    work = Work(url)
    work.main_run(url)
