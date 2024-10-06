import csv
import requests
from bs4 import BeautifulSoup

url = 'https://vzdelavanie.uniza.sk/vzdelavanie/'
code = 316027
response = requests.get(url)
response.encoding = 'windows-1250'

# Create and open a CSV file for writing
with open('subject_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row to the CSV file
    header = ["code", "podmienky", "vysledky", "osnova"]
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
                subj_code = code_col.text.strip().split(": ")[1]

                # Initialize variables for Podmienky, Výsledky, and Osnova
                podmienky = vysledky = osnova = None

                # Loop through rows to find "Podmienky", "Výsledky", and "Osnova"
                for i in range(10, 25):
                    text = rows[i].find_all('td')[0].text
                    if "Podmienky na absolvovanie predmetu" in text:
                        podmienky = text[35:]
                    elif "Výsledky vzdelávania" in text:
                        vysledky = text[21:]
                    elif "Stručná osnova predmetu" in text:
                        osnova = text[24:]

                # Write the data to the CSV
                csv_writer.writerow([subj_code, podmienky, vysledky, osnova])
                print(f"Code {code} processed.")
            else:
                print(f"No table found for code {code}")
        else:
            print(f"Failed to retrieve page for code {code}")

        code += 1  # Move to the next subject code
