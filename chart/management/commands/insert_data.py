import csv
from django_chart.settings import BASE_DIR
from django.core.management.base import BaseCommand
from chart.models import (Country, Year, SuicideCase)


# DATA_FORMAT1 ={
#     "country": [
#         {"year": "1977", "total_case": ""},
#         {"year": "1977", "total_case": ""},
#         {"year": "1978", "total_case": ""},
#     ],
#     "country2": [
#         {"year": "1977", "total_case": ""},
#         {"year": "1977", "total_case": ""},
#         {"year": "1978", "total_case": ""},
#     ]
# }
#
# DATA_FORMAT2 ={
#     "1977": {"country": "", "year": "", "cases": ""},
#     "1978": {"country": "", "year": "", "cases": ""},
#     "1979": {"country": "", "year": "", "cases": ""}
# }
#
# FINAL_ENTRIES =[
#     {"year": "1977", "country": "", "total_case": ""},
#     {"year": "1978", "country": "", "total_case": ""},
#     {"year": "1979", "country": "", "total_case": ""},
# ]


def build_db_entries(list_of_rows):
    db_entries = []
    entries = {}

    for row in list_of_rows:
        country = row['country']
        entries.setdefault(str(country), [])
        entries[country] = entries.get(country)+[{"year": row["year"], "cases": int(row["suicides_no"])}]

    for country in entries:
        date_list = entries.get(country)
        year_entries = {}
        for data in date_list:
            year = data['year']
            year_entries.setdefault(str (year), {"country": country, "year": year, "cases": data['cases']})
            year_entries[str (year)]['cases'] = year_entries[str(year)]['cases'] + data['cases']

        db_entries += list(year_entries.values())
        year_entries = {}

    return db_entries


class Command(BaseCommand):
    def handle(self, *args, **options):

        print("Creating database...")

        file_path = BASE_DIR / 'data/master.csv'
        csv_file = open(file_path,'r')
        fields = ['country','year','sex','age','suicides_no','population','suicides/100k pop','country-year','HDI for year', 'gdp_for_year ($)' ,'gdp_per_capita ($)','generation']
        reader = csv.DictReader(csv_file, fieldnames=fields)
        next(reader)
        entries = build_db_entries([row for row in reader])

        for entry in entries:
            country,_ = Country.objects.get_or_create(name=entry['country'])
            year,_ = Year.objects.get_or_create(name=entry['year'])
            SuicideCase.objects.create(
                country=country,
                year=year,
                cases=entry['cases']
            )
        print("Completed creating database.")
        return None