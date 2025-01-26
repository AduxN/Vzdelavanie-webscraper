import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://vzdelavanie.uniza.sk/vzdelavanie/'
code = 316027
response = requests.get(url)
response.encoding = 'windows-1250'

# Create and open a CSV file for writing
with open('subjects.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row to the CSV file
    header = ["name", "code", "abbreviation"]
    csv_writer.writerow(header)

    while code < 316313:
        page_url = f'{url}/planinfo.php?kod={code}&lng=sk'  # Construct the URL for the current page
        response = requests.get(page_url)
        response.encoding = 'windows-1250'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            main_table = soup.find('table', id='id-tabulka-inf-list-predmetu')

            if main_table:  # Ensure the table exists
                rows = main_table.find_all('tr')

                # Extract the subject code
                code_row = rows[3]

                code_col = code_row.find_all('td')[0]
                name_col = code_row.find_all('td')[1]

                subj_code = code_col.text.strip().split(": ")[1]
                full_name = name_col.text.strip().split(": ")[1]
                name = full_name.split(" (")[0]
                abbreviation = full_name.split(" (")[1].replace(")", "")

                # Write the data to the CSV
                csv_writer.writerow([name, subj_code, abbreviation])
                print(f"Code {code} processed.")
            else:
                print(f"No table found for code {code}")
        else:
            print(f"Failed to retrieve page for code {code}")

        code += 1  # Move to the next subject code

df = pd.read_csv('csv/subjects.csv')
df_cleaned = df.drop_duplicates()
df_cleaned.to_csv('csv/subjects_cleaned.csv', index=False)
print("Duplicates removed and saved to 'csv/subjects_cleaned.csv'")
