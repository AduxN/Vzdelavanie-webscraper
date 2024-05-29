import csv
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import random

url = 'https://vzdelavanie.uniza.sk/vzdelavanie/'
code = 316027
response = requests.get(url)


# Create and open a CSV file for writing
with open('grades.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row to the CSV file
    header = ["code", "count", "grade_A", "grade_B", "grade_C", "grade_D", "grade_E", "grade_FX", "average_grade"]
    csv_writer.writerow(header)

    while code < 316313: #316313
        page_url = f'{url}/planinfo.php?kod={code}&lng=sk'  # Construct the URL for the current page
        response = requests.get(page_url)
        # print(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            main_table = soup.find('table', id='id-tabulka-inf-list-predmetu')

            code_row = main_table.find_all('tr')[3]
            code_col = code_row.find_all('td')[0]
            subj_code = code_col.text.strip().split(": ")[1]
            # print(subj_code)

            count_row = main_table.find_all('tr')[-7]
            # print(count_row)
            count_col = count_row.find_all('td')[0]
            count = count_col.text.strip().split(": ")[1].split("\n")[0]
            # print(count)

            grade_table = soup.find('table', class_='ilstat')

            grades = []

            # Iterate over each row in the table (skipping the first header row)
            for row in grade_table.find_all('tr')[1:]:
                # Extract columns from the row
                cols = row.find_all('td')
                # Extract text from each column and store in a list
                grade_data = [col.text.strip().split(" ")[0] for col in cols]
                # Add the extracted data to the grades list
                grades.append(grade_data)
            print(grades)

            percentages = [float(p) for p in grades[0]]

            # Map each grade to a numerical value
            grade_values = {
                "grade_A": 1.0,
                "grade_B": 2.0,
                "grade_C": 3.0,
                "grade_D": 4.0,
                "grade_E": 5.0,
                "grade_FX": 6.0
            }

            grade_names = ["grade_A", "grade_B", "grade_C", "grade_D", "grade_E", "grade_FX"]

            weighted_sum = sum(grade_values[grade_names[i]] * percentages[i] for i in range(len(grade_names)))
            average_grade_value = weighted_sum / 100

            csv_writer.writerow([subj_code, count, grades[0][0], grades[0][1], grades[0][2], grades[0][3], grades[0][4], grades[0][5], average_grade_value])
            print(f"Code {code} processed.")
        code += 1
