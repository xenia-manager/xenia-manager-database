import requests
from bs4 import BeautifulSoup
import json

response = requests.get('https://andydecarli.com/Video%20Games/Collection%20Pages/Collection%20Xbox%20360.html', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
})

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[1].find_all('table')[2].find_all("tr")

    game_data = []

    for row in table[1:]:
        row_list = row.findAll('td')
        name = row_list[0].text.strip()

        # Extract front cover image URL (Full Size and Thumbnail)
        front_cover_img = row_list[1].find('a')
        if front_cover_img:
            try:
                front_cover_full_size = front_cover_img['href'].replace("..","https://andydecarli.com/Video Games")
            except:
                front_cover_full_size = None
            try:
                front_cover_thumbnail = front_cover_img.find('img')['src'].replace("..","https://andydecarli.com/Video Games")
            except:
                front_cover_thumbnail = None
        else:
            front_cover_img = row_list[1]
            if front_cover_img:
                try:
                    front_cover_full_size = front_cover_img['href'].replace("..","https://andydecarli.com/Video Games")
                except:
                    front_cover_full_size = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Full Size/Xbox 360 " + name + " Front Cover.jpg"
                try:
                    front_cover_thumbnail = front_cover_img.find('img')['src'].replace("..","https://andydecarli.com/Video Games")
                except:
                    front_cover_thumbnail = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Thumbnail/Xbox 360 " + name + " Front CoverThumbnail.jpg"
            else:
                front_cover_full_size = None
                front_cover_thumbnail = None

        # Extract back cover image URL (Full Size and Thumbnail)
        back_cover_img = row_list[2].find('a')
        if back_cover_img:
            try:
                back_cover_full_size = back_cover_img['href'].replace("..","https://andydecarli.com/Video Games")
            except:
                back_cover_full_size = None
            try:
                back_cover_thumbnail = back_cover_img.find('img')['src'].replace("..","https://andydecarli.com/Video Games")
            except:
                back_cover_thumbnail = None
        else:
            back_cover_img = row_list[2]
            if back_cover_img:
                try:
                    back_cover_full_size = back_cover_img['href'].replace("..","https://andydecarli.com/Video Games")
                except:
                    back_cover_full_size = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Full Size/Xbox 360 " + name + " Back Cover.jpg"
                try:
                    back_cover_thumbnail = back_cover_img.find('img')['src'].replace("..","https://andydecarli.com/Video Games")
                except:
                    back_cover_thumbnail = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Thumbnail/Xbox 360 " + name + " Back CoverThumbnail.jpg"
            else:
                back_cover_full_size = None
                back_cover_thumbnail = None

        # Create an object for the current game
        game = {
            'Name': name,
            'Front': {
                'Full Size': front_cover_full_size,
                'Thumbnail': front_cover_thumbnail
            },
            'Back': {
                'Full Size': back_cover_full_size,
                'Thumbnail': back_cover_thumbnail
            }
        }
        print(game)
        
        # Append the game dictionary to the game_data list
        game_data.append(game)
    
    with open('games_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(game_data, json_file, ensure_ascii=False, indent=4)

    print("Data scraped and saved successfully!")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)