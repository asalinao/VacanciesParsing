from hh_parser import get_vacancies
from uploadToGoogleSheets import upload_vacancies

if __name__ == '__main__':
    get_vacancies()
    upload_vacancies()