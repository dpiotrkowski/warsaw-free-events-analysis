import requests
from bs4 import BeautifulSoup
import csv
import re

url = 'https://waw4free.pl/'

# Lista dzielnic Warszawy
districts = [
    "okolice Warszawy","Mokotów", "Śródmieście", "Praga-Południe", "Praga-Północ", 
    "Wola", "Ursynów", "Bielany", "Targówek", "Ochota", 
    "Włochy", "Bemowo", "Żoliborz", "Rembertów", "Wawer", 
    "Białołęka", "Mokotów"
]

# GET request
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Szukamy wszystkich div z klasą 'box-text'
    box_texts = soup.find_all('div', class_='box-text')

    # Zapisujemy do csv
    with open('../data/events_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Wydarzenie', 'Data', 'Godzina', 'Miejsce', 'Kategorie'])  # Nagłówki

        for box in box_texts:
            box_title = box.find('div', class_='box-title')  
            box_data = box.find('div', class_='box-data')    

            title_text = box_title.get_text(strip=True) if box_title else 'Brak'
            date_text = 'Brak'
            time_text = 'Brak'
            place_text = 'Brak'  # Nowa zmienna dla miejsca
            categories_list = []  # Lista kategorii

            if box_data:
                # Tekst z box_data
                box_data_text = box_data.get_text(strip=True)

                # Wzorzec regex do dat i godzin
                date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})\s*,?\s*(\d{1,2}:\d{2})|dzisiaj\s*,?\s*(\d{1,2}:\d{2})|od dzisiaj\s*,?\s*(\d{1,2}:\d{2})|do\s*(\d{1,2}\.\d{1,2}\.\d{4})'
                matches = re.findall(date_pattern, box_data_text)

                for match in matches:
                    if match[0]:  # Data
                        date_text = match[0]
                    if match[1]:  # Godzina
                        time_text = match[1]
                    if match[2]:  # "dzisiaj" z godziną
                        time_text = match[2]
                    if match[4]:  # "do" z datą
                        date_text = match[4]

                # Sprawdzenie, czy w box_data_text znajduje się któraś z dzielnic
                for district in districts:
                    if district in box_data_text:
                        place_text = district
                        break  # Przerwij po znalezieniu pierwszej dzielnicy

            # Kategoria
            category_items = box.find_all(class_=re.compile(r'^b-c'))
            categories_list = [cat.get_text(strip=True) for cat in category_items]

            categories_text = ', '.join(categories_list) if categories_list else 'Brak'

            writer.writerow([title_text, date_text, time_text, place_text, categories_text])  # Zapisz dane
    print("Dane zapisano do events_data.csv")
else:
    print(f"Wystąpił błąd. Status code: {response.status_code}")
