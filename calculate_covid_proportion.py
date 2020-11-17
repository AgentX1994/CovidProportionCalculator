import operator
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Grab current US statistics
page = requests.get('https://www.worldometers.info/coronavirus/country/us/')

# Parse HTML
soup = BeautifulSoup(page.text, 'html.parser')

# get table
table = soup.find(id='usa_table_countries_today').tbody

# get rows

data = []
for row in table.find_all('tr'):
    if row.has_attr('class') and 'total_row_usa' in row['class']: continue

    # order of fields
    #  0   state number
    #  1   state name
    #  2   total cases
    #  3   new cases
    #  4   total deaths
    #  5   new deaths
    #  6   total recovered
    #  7   active cases
    #  8   total cases / 1M pop
    #  9   deaths / 1M pop
    #  10  total tests
    #  11  tests / 1M pop
    #  12  population
    #  13  source
    #  14  projections
    fields = list(row.find_all('td'))
    name = fields[1].get_text(strip=True)
    try:
        active = int(fields[7].get_text(strip=True).replace(',',''))
        pop = int(fields[12].get_text(strip=True).replace(',',''))
        active_cases_per_million = active / (pop / 1000000)
        data.append((name, active_cases_per_million))
    except:
        data.append((name, -1.0))

data.sort(key=operator.itemgetter(1), reverse=True)

# Replace -1's with N/A now that we've sorted the data
for index, (state, active_cases_per_million) in enumerate(data):
    if active_cases_per_million == -1.0:
        data[index] = (state, 'N/A')

print(tabulate(data, ['State Name', 'Active Cases / 1M Population'], colalign=('right', 'decimal',), showindex=True))
