![Alt Text](https://github.com/ysmaelrequena/Street-Fighter-6-frame-data-CLI-tool/blob/main/sf6.jpg)
                     
                     
                     
                     
                     
                     
##                                       The premiere Street Fighter 6 Frame Data CLI Tool (Kind of a long title, isn't it?)
                                                                                                                          
This CLI tool, in essence is a web scraper that takes the info that is on the most commonly used wiki for competitive Street Fighter (https://wiki.supercombo.gg/),
and saves you the time of going to the website and then finding the character you want to explore, and then looking for the movement; instead, here you only 
introduce the name of the character you want to see in the console, and the app will show you the frame data of said character in a readable format (json).
                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
##                                                                    How did I build it?
                                                    
The app was built using Python and the 'BeautifulSoup' library mainly. The idea was to build something that wasn't extremely complicated and was useful, so in the
source code I first fetch the information contained in the Supercombo wiki with an async function called 'fetch_character_data()', then in the main function,
I'm just looping through the divs that were fetched to be able to get the info; based on the move type, I'm storing the info in dictionaries that
are initialized as global variables with empty dictionaries as their initial value, finally, after I've adquired all the info and I've stored it, I'm storing 
everything as subdictionaries in a main dictionary called 'character_framedata' and then I'm printing the dictionary as a json to the console.

For user convenience, I also used 'pyinstaller' to include an executable version of the program.
                                                                                                      
                                                                                                      
                                                                                                                                                                                                           
##                                                                   Why did I build it?
                                                    
I think ease of access to information can motivate players to learn more about the game, which in turn, will help them improve, I have no scientific evidence of this,
but it has worked with me (due to my own laziness of navigating through the wiki).
                                                                                                      
                                                                                                      
                                                                                                      
##                                                                      Quick Start
                                                        
                                                                                                                                                              
- Run the script in your terminal, the program will ask you which character's data do you want to see
- Write the character's name in the terminal and press enter, the program will fetch the data and show it to you.
                                                                                                      
                                                                                                      
##                                                                        Usage

  Here's the list of currently available characters, as more get added to the game, I'll update the list:

- A.K.I
- Blanka
- Cammy
- Chun-Li
- Dee_Jay
- Dhalsim
- E.Honda
- Guile
- Jamie
- JP
- Juri
- Ken
- Kimberly
- Lily
- Luke
- Manon
- Marisa
- Rashid
- Ryu
- Zangief

Just input one of these names after the first prompt appears in the console and the scraper will do the rest for you.


##                                                                  Contributing 

Clone the repo

```bash
git clone
https://github.com/ysmaelrequena/web_scraper_sf6
cd web_scraper
```

Run the project
```
You can either run the script with 'python main.py' or, you can go to the "dist" folder and use an executable
version of the program.
```

Run the tests

```
For testing, you can import the 'unittest' framework, which, as the name suggests, can help you run unit tests on the code to ensure everything is going well,
or you can use the 'pytest' library ('pip install pytest').
```

## Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
                                                                                                      
                                                                                                    
