# 30-07-2024
# Working as expected to scrape data and convert files into CSV format and folder
# to do: get all links in one go

import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

# Define the folder path
folder_path = ''

url = 'https://docs.oracle.com/en/cloud/saas/financials/24c/oedmf/gljierrorcodes-25963.html'
# url = "https://docs.oracle.com/en/cloud/saas/financials/24c/oedmf/glledgers-25846.html"
# url = "https://docs.oracle.com/en/cloud/saas/financials/24c/oedmf/gljesourcestl-11208.html"

response = requests.get(url)

# if response.status_code == 200:
soup = BeautifulSoup(response.text, 'html.parser')

paragrphas = soup.find_all('p')
text_data = [p.get_text() for p in paragrphas]
# print('text_data: ',text_data[2].split(' ')[0])
file_pre_fix = text_data[2].split(' ')[0]
combined_text = ' '.join(text_data)

folder_path = file_pre_fix
# Check if the folder exists, and if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
else:
    print(f"Folder '{folder_path}' already exists.")


with open(folder_path+'/'+file_pre_fix+'_Summary.txt', 'w', encoding='utf-8') as file:
    file.write(combined_text)

# print('done')

# Find all sections
sections = soup.find_all('section', class_='section')
section_title_list = []

for section in sections:
    try:
        # Extract section title
        section_title = section.find('h2', class_='title sectiontitle').get_text(strip=True)
        
        filename = f"{folder_path+'/'+file_pre_fix+'_'+section_title.replace(' ', '_')}.csv"
        print('filename:', filename)
        section_title_list.append(filename)

        # Find the table within the section
        table = section.find('table')

        # Process table data
        table_data = []
        headers = [header.get_text(strip=True) for header in table.find_all('th')]

        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            row_data = {headers[i]: cell.get_text(strip=True) for i, cell in enumerate(cells)}
            table_data.append(row_data)

        df = pd.DataFrame(table_data)
        # print(df)

        # Save to CSV
        df.to_csv(filename, index=False)

    except Exception as e:
        print('Error:', e)