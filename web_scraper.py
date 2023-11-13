from bs4 import BeautifulSoup
import requests
import asyncio
import json

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
table = ''
normal_names = ''
command_normals = ''
tgt_combos = ''
throw_data = ''
drv_sys = ''
specials = ''
supers = ''
taunts = ''
phase = ['Startup', 'Active', 'Recovery', 'Cancel', 'Damage', 'Guard', 'On Hit', 'On Block']


#move names and framedata

#normals
normal_nom_data = []
normal_name_data = []
normal_framedata = []
normal_frame_obj = {'Normals': {}}

#command normals
cmd_nom_data = []
cmd_name_data = []
cmd_framedata = []
cmd_frame_obj = {'Command Normals': {}}

#target combos
tgt_nom_data = []
tgt_name_data = []
tgt_framedata = []
tgt_frame_obj = {'Target Combos': {}}

#throws
throw_nom_data = []
throw_name_data = []
throw_framedata = []
throw_frame_obj = {'Throws': {}}

#drive system
drive_nom_data = []
drive_name_data = []
drive_framedata = []
drive_frame_obj = {'Drive System': {}}

#specials
special_nom_data = []
special_name_data = []
special_framedata = []
special_frame_obj = {'Special Moves': {}}

#supers
super_nom_data = []
super_name_data = []
super_framedata = []
super_frame_obj = {'Super Arts': {}}

#taunts
taunt_nom_data = []
taunt_name_data = []
taunt_framedata = []
taunt_frame_obj = {'Taunts': {}}

group_size = 8

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
            normal_names = soup.find('section', attrs={'id':'section-collapsible-1'})
            command_normals = soup.find('section', attrs={'id':'section-collapsible-2'})
            tgt_combos = soup.find('section', attrs={'id':'section-collapsible-3'})
            throw_data = soup.find('section', attrs={'id':'section-collapsible-4'})
            drv_sys = soup.find('section', attrs={'id':'section-collapsible-5'})
            specials = soup.find('section', attrs={'id':'section-collapsible-6'})
            supers = soup.find('section', attrs={'id':'section-collapsible-7'})
            taunts = soup.find('section', attrs={'id':'section-collapsible-8'})
            table_attributes = soup.find_all('td', attrs={'style':'text-align:center;'})
            
#now let's organize the moves by type and store the names in variables

#normals
            #organize normal moves names
            if normal_names:

                n_divs = normal_names.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

               #get nomenclature of moves 
                for normal in n_divs:
                   nom_div = normal.find('div', attrs={'style':''})
                   if nom_div:
                       normal_nom_data.append(nom_div.text.strip())
                       

                #get full name of moves
                   full_name_divs = normal.find('div', attrs={'style':"font-size:80%"})
                   if full_name_divs:
                       normal_name_data.append(full_name_divs.text.strip())

                #get frame data of moves
                normal_framedata_table = normal_names.find_all('div', class_='movedata-flex-framedata-table')
                for framedata in normal_framedata_table:
                    find_normal_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_normal_data = find_normal_table.find_all('td', attrs={'style':'text-align:center;'})
                    for i, data in enumerate(find_normal_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_normal_data) - 1:
                            normal_framedata.append(current_group)
               
            
            for first_key, second_key, value in zip(normal_nom_data, normal_name_data, normal_framedata):
                if first_key not in normal_frame_obj['Normals']:
                    normal_frame_obj['Normals'][first_key] = {}
                if second_key not in normal_frame_obj['Normals'][first_key]:
                    normal_frame_obj['Normals'][first_key][second_key] = {}
                
                for i in range(8):
                    sub_phase = f'{phase[i]}'
                    sub_value = f'{value[i]}' 
                    normal_frame_obj['Normals'][first_key][second_key][sub_phase] = sub_value
#command normals
     
            #organize command normal names    
            if command_normals:
                cmd_divs = command_normals.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for cmd in cmd_divs:
                    #get command normals nomenclature
                    cmd_nom_div = cmd.find('div', attrs={'style':''})
                    if cmd_nom_div:
                        cmd_nom_data.append(cmd_nom_div.text.strip())
                    #get command normals full names
                    cmd_name_div = cmd.find('div', attrs={'style':"font-size:80%"})
                    if cmd_name_div:
                        cmd_name_data.append(cmd_name_div.text.strip())

                #get frame data of moves
                cmd_framedata_table = command_normals.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in cmd_framedata_table:
                    find_cmd_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_cmd_data = find_cmd_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_cmd_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_cmd_data) - 1:
                            cmd_framedata.append(current_group)
               
                for first_key, second_key, value in zip(cmd_nom_data, cmd_name_data, cmd_framedata):
                    if first_key not in cmd_frame_obj['Command Normals']:
                        cmd_frame_obj['Command Normals'][first_key] = {}
                    if second_key not in cmd_frame_obj['Command Normals'][first_key]:
                        cmd_frame_obj['Command Normals'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        cmd_frame_obj['Command Normals'][first_key][second_key][sub_phase] = sub_value

          
#target combos
           
            #organize target combo names    
            if tgt_combos:
                tgt_divs = tgt_combos.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for target in tgt_divs:
                    #get command normals nomenclature
                    tgt_nom_div = target.find('div', attrs={'style':''})
                    if tgt_nom_div:
                        tgt_nom_data.append(tgt_nom_div.text.strip())
                    #get command normals full names
                    tgt_name_div = target.find('div', attrs={'style':"font-size:80%"})
                    if tgt_name_div:
                        tgt_name_data.append(tgt_name_div.text.strip())
            
                #get frame data of moves
                tgt_framedata_table = tgt_combos.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in tgt_framedata_table:
                    find_tgt_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_tgt_data = find_tgt_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_tgt_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_tgt_data) - 1:
                            tgt_framedata.append(current_group)
               
                for first_key, second_key, value in zip(tgt_nom_data, tgt_name_data, tgt_framedata):
                    if first_key not in tgt_frame_obj['Target Combos']:
                        tgt_frame_obj['Target Combos'][first_key] = {}
                    if second_key not in tgt_frame_obj['Target Combos'][first_key]:
                        tgt_frame_obj['Target Combos'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        tgt_frame_obj['Target Combos'][first_key][second_key][sub_phase] = sub_value
            
            
            #organize throw data
            if throw_data:
                throw_divs = throw_data.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for throw in throw_divs:
                    #get command normals nomenclature
                    throw_nom_div = throw.find('div', attrs={'style':''})
                    if throw_nom_div:
                        throw_nom_data.append(throw_nom_div.text.strip())
                    #get command normals full names
                    throw_name_div = throw.find('div', attrs={'style':"font-size:80%"})
                    if throw_name_div:
                        throw_name_data.append(throw_name_div.text.strip())
                
                #get frame data of moves
                throw_framedata_table = throw_data.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in throw_framedata_table:
                    find_throw_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_throw_data = find_throw_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_throw_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_throw_data) - 1:
                            throw_framedata.append(current_group)
               
                for first_key, second_key, value in zip(throw_nom_data, throw_name_data, throw_framedata):
                    if first_key not in throw_frame_obj['Throws']:
                        throw_frame_obj['Throws'][first_key] = {}
                    if second_key not in throw_frame_obj['Throws'][first_key]:
                        throw_frame_obj['Throws'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        throw_frame_obj['Throws'][first_key][second_key][sub_phase] = sub_value
            
            
            #organize Drive System data
            if drv_sys:
                drive_divs = drv_sys.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for drive in drive_divs:
                    #get drive system nomenclature
                    drive_nom_div = drive.find('div', attrs={'style':''})
                    if drive_nom_div:
                        drive_nom_data.append(drive_nom_div.text.strip())
                    #get drive system full names
                    drive_name_div = drive.find('div', attrs={'style':"font-size:80%"})
                    if drive_name_div:
                        drive_name_data.append(drive_name_div.text.strip())

                #get frame data of moves
                drv_framedata_table = drv_sys.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in drv_framedata_table:
                    find_drv_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_drv_data = find_drv_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_drv_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_drv_data) - 1:
                            drive_framedata.append(current_group)
               
                for first_key, second_key, value in zip(drive_nom_data, drive_name_data, drive_framedata):
                    if first_key not in drive_frame_obj['Drive System']:
                        drive_frame_obj['Drive System'][first_key] = {}
                    if second_key not in drive_frame_obj['Drive System'][first_key]:
                        drive_frame_obj['Drive System'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        drive_frame_obj['Drive System'][first_key][second_key][sub_phase] = sub_value
            
            
            if specials:
                special_divs = specials.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for special in special_divs:
                    #get drive system nomenclature
                    special_nom_div = special.find('div', attrs={'style':''})
                    if special_nom_div:
                        special_nom_data.append(special_nom_div.text.strip())
                    #get drive system full names
                    special_name_div = special.find('div', attrs={'style':"font-size:80%"})
                    if special_name_div:
                        special_name_data.append(special_name_div.text.strip())

                #get frame data of moves
                special_framedata_table = specials.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in special_framedata_table:
                    find_special_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_special_data = find_special_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_special_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_special_data) - 1:
                            special_framedata.append(current_group)
               
               
                for first_key, second_key, value in zip(special_nom_data, special_name_data, special_framedata):
                    if first_key not in special_frame_obj['Special Moves']:
                        special_frame_obj['Special Moves'][first_key] = {}
                    if second_key not in special_frame_obj['Special Moves'][first_key]:
                        special_frame_obj['Special Moves'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        special_frame_obj['Special Moves'][first_key][second_key][sub_phase] = sub_value  
                         
          
            if supers:
                super_divs = supers.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for super in super_divs:
                    #get drive system nomenclature
                    super_nom_div = super.find('div', attrs={'style':''})
                    if super_nom_div:
                        super_nom_data.append(super_nom_div.text.strip())
                    #get drive system full names
                    super_name_div = super.find('div', attrs={'style':"font-size:80%"})
                    if super_name_div:
                        super_name_data.append(super_name_div.text.strip())

                #get frame data of moves
                super_framedata_table = supers.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in super_framedata_table:
                    find_super_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_super_data = find_super_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_super_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_super_data) - 1:
                            super_framedata.append(current_group)
               
                for first_key, second_key, value in zip(super_nom_data, super_name_data, super_framedata):
                    if first_key not in super_frame_obj['Super Arts']:
                        super_frame_obj['Super Arts'][first_key] = {}
                    if second_key not in super_frame_obj['Super Arts'][first_key]:
                        super_frame_obj['Super Arts'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        super_frame_obj['Super Arts'][first_key][second_key][sub_phase] = sub_value

             
           
            if taunts:
                taunt_divs = taunts.find_all('div', class_='movedata-flex-framedata-name-item movedata-flex-framedata-name-item-middle')

                for taunt in taunt_divs:
                    #get drive system nomenclature
                    taunt_nom_div = taunt.find('div', attrs={'style':''})
                    if taunt_nom_div:
                        taunt_nom_data.append(taunt_nom_div.text.strip())
                    #get drive system full names
                    taunt_name_div = taunt.find('div', attrs={'style':"font-size:80%"})
                    if taunt_name_div:
                        taunt_name_data.append(taunt_name_div.text.strip())

                #get frame data of moves
                taunt_framedata_table = taunts.find_all('div', class_='movedata-flex-framedata-table')
                
                for framedata in taunt_framedata_table:
                    find_taunt_table = framedata.find('table', class_='wikitable citizen-table-nowrap')
                    find_taunt_data = find_taunt_table.find_all('td', attrs={'style':'text-align:center;'})

                    for i, data in enumerate(find_taunt_data):
                        
                        if i % group_size == 0:
                            current_group = []

                        current_group.append(data.text.replace('\n',''))

                        if (i + 1) % group_size == 0 or i == len(find_super_data) - 1:
                            taunt_framedata.append(current_group)
               
                for first_key, second_key, value in zip(taunt_nom_data, taunt_name_data, taunt_framedata):
                    if first_key not in taunt_frame_obj['Taunts']:
                        taunt_frame_obj['Taunts'][first_key] = {}
                    if second_key not in taunt_frame_obj['Taunts'][first_key]:
                        taunt_frame_obj['Taunts'][first_key][second_key] = {}

                    for i in range(8):
                        sub_phase = f'{phase[i]}'
                        sub_value = f'{value[i]}' 
                        taunt_frame_obj['Taunts'][first_key][second_key][sub_phase] = sub_value

            character_framedata.update(normal_frame_obj)
            character_framedata.update(cmd_frame_obj)
            character_framedata.update(tgt_frame_obj)
            character_framedata.update(throw_frame_obj)
            character_framedata.update(drive_frame_obj)
            character_framedata.update(special_frame_obj)
            character_framedata.update(super_frame_obj)
            character_framedata.update(taunt_frame_obj)
            print(json.dumps(character_framedata, indent=2))
    
async def fetch_character_data(character_name):
    url = f'https://wiki.supercombo.gg/w/Street_Fighter_6/{character_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data for {character_name}")
        return None



asyncio.run(character_scrape())


    





