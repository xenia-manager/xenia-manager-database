import os
import json
import requests
from bs4 import BeautifulSoup

def download_image(url, target_path):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    })
    with open(target_path, 'wb') as f:
        f.write(response.content)

def scrape_and_download():
    # Scrape data from the website
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
                front_cover_full_size = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Full Size/Xbox 360 " + name + " Front Cover.jpg"
                front_cover_thumbnail = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Thumbnail/Xbox 360 " + name + " Front CoverThumbnail.jpg"

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
                back_cover_full_size = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Full Size/Xbox 360 " + name + " Back Cover.jpg"
                back_cover_thumbnail = "https://andydecarli.com/Video Games/Collection/Xbox 360/Scans/Thumbnail/Xbox 360 " + name + " Back CoverThumbnail.jpg"

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
        
        # Download and organize images
        download_and_organize_images(game_data)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

def download_and_organize_images(game_data):
    for game in game_data:
        game_name = game['Name']

        for side in game:
            if side == 'Name':
                continue
            url = game[side]['Thumbnail']
            if url:
                image_name = f"{game_name.replace(' ', '_')}.jpg"
                folder_path = os.path.join('Assets',side.replace(' ', '_'))
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, image_name)
                download_image(url, file_path)
                print(f"Downloaded: {file_path}")

            else:
                print(f"No image found for {game_name} {side}.")

if __name__ == "__main__":
    scrape_and_download()
