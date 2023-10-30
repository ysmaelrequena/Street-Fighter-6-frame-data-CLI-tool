from bs4 import BeautifulSoup
import requests
import asyncio

characters = {
    'aki': 'A.K.I',
    'blanka': 'Blanka',
    'cammy': 'Cammy',
    'chunli': 'Chun-Li',
    'deejay': 'Dee_Jay',
    'dhalsim': 'Dhalsim',
    'honda': 'E.Honda',
    'guile': 'Guile',
    'jamie': 'Jamie',
    'jp': 'JP',
    'juri': 'Juri',
    'ken': 'Ken',
    'kimberly': 'Kimberly',
    'lily': 'Lily',
    'luke': 'Luke',
    'manon': 'Manon',
    'marisa': 'Marisa',
    'rashid': 'Rashid',
    'ryu': 'Ryu',
    'zangief': 'Zangief'
}

html_text = ''
soup = ''
move_names = ''
table = ''
move_nom_data = []
move_name_data = []
character_movelist = {}
character_framedata = []



async def character_scrape():
    character_request = print(f"Which character's data do you want to see?>")
    character_input = input().lower()
    character = characters.get(character_input)

    if character:
        print(character)
    elif character_input in ['a.k.i.', 'a k i']:
        character = characters['aki']
        print(character)
    elif character_input in ['chun', 'chun-li', 'chun li']:
        character = characters['chunli']
        print(character)
    elif character_input in ['dee jay', 'dee_jay']:
        character = characters['deejay']
        print(character)
    elif character_input in ['e.honda', 'ehonda', 'e honda']:
        character = characters['honda']
        print(character)
    elif character_input in ['j.p', 'j.p.']:
        character = characters['jp']
        print(character)
    else:
        print('Character not found, please try again')
    
    if character: 
        html_text = await fetch_character_data(character)

        if html_text:
            soup = BeautifulSoup(html_text, 'lxml')
            move_names = soup.find_all('div', class_='movedata-flex-framedata-name')
            table = soup.find_all('table', attrs={'class':'wikitable citizen-table-nowrap'})

#Organizamoslos nombres de cada movimientos organizados junto a su respecitva nomeclatura
            if move_names:
               
                for move in move_names:
                    nom_divs = move.find('div')
                    name_divs = move.find('div', attrs={'style':"font-size:80%"})
                    moves_full_name = [name_divs.get_text(strip=True)]
                    nomenclature = [div.get_text(strip=True) for div in nom_divs]
                    move_nom_data.extend(nomenclature)
                    move_name_data.extend(moves_full_name)
                for key, value in zip(move_nom_data, move_name_data):
                         character_movelist[key] = value
                         
                print(f'The character has {len(move_nom_data)} moves:')
                
#Recolectar y organizar framedata de cada movimiento
            if table:
                for row in table.find('tr'):
                    row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                print(row_data)
            else:
                print('Table not found')



async def fetch_character_data(character_name):
    url = f'https://wiki.supercombo.gg/w/Street_Fighter_6/{character_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data for {character_name}")
        return None

asyncio.run(character_scrape())


    





