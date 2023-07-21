import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathvalidate import sanitize_filename


 
# -- Functions --

# Carry out set up requirements
def init():
    global driver

    # global f, driver

    # filename = "Player by season 22-23.csv"

    # f = open(filename, "w", encoding="utf-8")

    # headers = "Rank, Player, Country, Appearances, Club, Profile, \n"

    # f.write(headers)

    driver = webdriver.Chrome()
    
    if platform.system() == 'Windows':
        driver.maximize_window()

    driver.get("https://www.premierleague.com/stats/top/players/appearances")  



# Open file and name it based on current search
def open_file(filename):
    global f

    filename = "Player by " + filename.lower() +".csv"

    filename = sanitize_filename(filename,"-")

    f = open(filename, "w", encoding="utf-8")

    headers = "Rank, Player, Country, Appearances, Club, Profile, \n"

    f.write(headers)



# This is where we put any code that clears the decks before we interact with the page
def crap_cutter():

    # find and click the Accept Cookies button
    cookies = driver.find_element(By.XPATH,"//button[contains(text(),'Accept All Cookies')]")

    if cookies.is_displayed():

        cookies.click()


    # remove spurious ad that (was) appearing
    advertClose = driver.find_element(By.ID, "advertClose")

    if advertClose.is_displayed():

        advertClose.click()
        

    time.sleep(2)



# Find an element by a class name
def get_element_by_class(element, class_name = "playerCountry"):

    class result:
        text = ''

    try:
        result = element.find_element(By.CLASS_NAME, class_name)
    
    except:
        result.text = "'" + class_name + "' not found"

    return result


# Find the element (div) that opens the drop-down list when clicked
def get_drop_list_button(text):

    button = driver.find_element(By.XPATH,".//div[text()='" + text + "']")

    return button


# Open the drop-down list
def show_drop_list(button):

    if button.is_displayed():

        button.click()


# Find the parent of the supplied element
def get_parent_element(element):

    return element.find_element(By.XPATH,"..")


# Find one element in a ul in order to find all its li elements
def get_drop_list_elements(text):

    li = driver.find_element(By.XPATH,".//li[text()='" + text + "']")

    ul = get_parent_element(li)

    return ul.find_elements(By.TAG_NAME,"li")


# Get rows in a table
def get_table_rows(table):

    return table.find_elements(By.TAG_NAME,"tr")


# Print rows to console and/or file
def print_row(text):

    print(text)

    f.write(text +"\n")



# Set the active season
def set_active_season(first_item = "2023/24",target_season="2022/23"):

    drop_down_button = get_drop_list_button(first_item)

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(first_item)

    for item in item_list:
        
       if item.text == target_season:
            
            item.click()

            time.sleep(2)

            break
        

# Get country
def get_country(record):
    return get_element_by_class(record, 'playerCountry').text


# Get player
def get_player(record):
    playerCol =  get_element_by_class(record, 'playerName')

    player = playerCol.text
    href = "Player link not found"

    if player != "'playerName' not found":
            href = playerCol.get_attribute('href')
    
    return {"name":player,"link":href}


# Get stat
def get_stat(record):
    return get_element_by_class(record, 'stats-table__main-stat').text


# Get team
def get_team(record):
    team_badge = get_element_by_class(record, 'badge-image-container')

    if team_badge.text:
        return "No club found"

    else:
        return get_parent_element(team_badge).text



# Iterate through a dropdown list...
def extract_list(first_item = "All Clubs"):

    open_file(first_item)

    drop_down_button = get_drop_list_button(first_item)

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(first_item)
        

    for item in item_list:

        time.sleep(2)

        current_item = item.text

        if current_item != first_item:

            print_row(current_item)

            item.click()
        
            get_result_table_by_class()

            show_drop_list(drop_down_button)



# Get player stats from table
def get_result_table_by_class(class_name = 'statsTableContainer'):
    
    table = driver.find_element(By.CLASS_NAME, class_name)

    time.sleep(1)

    results = get_table_rows(table)

    x = 0

    for record in results:
        x = x + 1

        country = get_country(record)

        player = get_player(record)

        stat = get_stat(record)

        team = get_team(record)

        print_row(str(x) + ", " + player["name"] + ", " + country + ", " + stat + ", " + team +  ", " + player["link"])



# Go

init()

crap_cutter()

set_active_season()

# extract_list()

# extract_list('All Nationalities')

# extract_list('2022/23')

extract_list('All Positions')