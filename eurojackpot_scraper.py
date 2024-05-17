from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

all_data = []

for year in range(2012, 2025):
    URL = f"https://www.euro-jackpot.net/results-archive-{year}"

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    response = requests.get(URL, headers=header)
    response.raise_for_status()  

    web_page = response.text
    soup = BeautifulSoup(web_page, 'html.parser')

    data = []

    results = soup.find_all('tr')
    for result in results:
        date_tag = result.find('a')
        if date_tag:
            date_text = ' '.join(date_tag.getText().split(' ')[1:4])
            date_cleaned = date_text.split()
            date_cleaned[0] = date_cleaned[0].rstrip('thstndr')
            date_cleaned = ' '.join(date_cleaned)
            formatted_date = datetime.strptime(date_cleaned, '%d %B %Y').strftime('%Y-%m-%d')


            all_numbers = result.find('ul', class_='balls small')

            if all_numbers:
                five_numbers = all_numbers.find_all('li', class_='ball')
                five_numbers_list = [five.getText() for five in five_numbers]

                two_numbers = all_numbers.find_all('li', class_='euro')
                two_numbers_list = [two.getText() for two in two_numbers]

                if len(five_numbers_list) == 5 and len(two_numbers_list) == 2:
                    data.append({
                        'Date': formatted_date,
                        'Main1': five_numbers_list[0],
                        'Main2': five_numbers_list[1],
                        'Main3': five_numbers_list[2],
                        'Main4': five_numbers_list[3],
                        'Main5': five_numbers_list[4],
                        'Add1': two_numbers_list[0],
                        'Add2': two_numbers_list[1],
                    })
                else:
                    print(f"Skipped entry with incorrect number of elements on date {formatted_date}")
            else:
                print(f"No number data found for date {formatted_date}")
        else:
            print("No date tag found")

    all_data.extend(data)

df = pd.DataFrame(all_data)

file_name = 'results_2012_to_2024.xlsx'
df.to_excel(file_name, index=False)
