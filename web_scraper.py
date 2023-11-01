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
character_framedata = {}



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
            table_attributes = soup.find_all('td', attrs={'style':'text-align:center;'})

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
                print(character_movelist)
                
                
#Recolectar y organizar framedata de cada movimiento

    if table_attributes:
        group_size = 8
        framedata_attributes = []
        for i, move_attributes in enumerate(table_attributes):
            if i % group_size == 0:
            # Start a new group of moves
                current_group = []

            # Extract the text from the td element and append it to the current group
            current_group.append(move_attributes.get_text(strip=True))

            if (i + 1) % group_size == 0 or i == len(table_attributes) - 1:
            # If we've collected 8 attributes or it's the last one, add the current_group to the list
                framedata_attributes.append(current_group)

        print(framedata_attributes)
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


    





