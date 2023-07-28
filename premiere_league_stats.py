import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathvalidate import sanitize_filename



 
# ------------ Init ------------

# Carry out set up requirements
def init():
    global driver, current_season, default_stat

    current_season = "2023/24"
    default_stat = "Appearances"

    driver = webdriver.Chrome()
    
    if platform.system() == 'Windows':
        driver.maximize_window()

    driver.get("https://www.premierleague.com/stats/top/players/appearances")  

    crap_cutter()


# Shut down the web browser etc
def shut_down():
    driver.close


# This is where we put any code that clears the decks before we interact with the page
def crap_cutter():

    # find and click the Accept Cookies button
    cookies = driver.find_element(By.XPATH,"//button[contains(text(),'Accept All Cookies')]")

    if cookies.is_displayed():

        cookies.click()

    advertClose()

    time.sleep(2)
    

# remove spurious ad that (was) appearing
def advertClose():   
    advertClose = driver.find_element(By.ID, "advertClose")

    if advertClose.is_displayed():

        advertClose.click()



# ------------ File Handling ------------

# Open file and name it based on current search
def open_file(filename):
    global f, active_season, active_stat

    filename = "Player " + active_stat.lower() + " " + filename.lower() + " " + active_season + ".csv"

    filename = sanitize_filename(filename,"-")

    f = open(filename, "w", encoding="utf-8")

    headers = "Number, Player, Country, " + active_stat + ", Appearances, Club, Profile, \n"

    f.write(headers)


# Print rows to console and/or file
def print_row(text):

    print(text)

    f.write(text +"\n")


# Close the current file
def close_file():
    global f

    f.close



# ------------ DOM Utilities ------------

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


# Find the parent of the supplied element
def get_parent_element(element):

    return element.find_element(By.XPATH,"..")


# Find one element in a ul in order to find all its li elements
def get_drop_list_elements(text, element='li'):

    li = driver.find_element(By.XPATH,".//" + element + "[text()='" + text + "']")

    ul = get_parent_element(li)

    return ul.find_elements(By.TAG_NAME,"li")


# Get rows in a table
def get_table_rows(table):

    if no_content(table):
        return []

    return table.find_elements(By.TAG_NAME,"tr")


def no_content(table):
    if get_element_by_class(table,"noContentContainer").text == "'noContentContainer' not found":
        return False
    
    return True


# Open drop-down list
def show_drop_list(button):

    if button.is_displayed():

        button.click()



# ------------ Record Fields ------------

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


# Get country
def get_country(record):
    return get_element_by_class(record, 'playerCountry').text



# ------------ Results ------------

# Get results table
def get_result_table_by_class(class_name = 'statsTableContainer'):
    global record_index
    
    record_index = 0

    table = get_element_by_class(driver, class_name)
    return table


# Check for pagination button..
def has_pagination_next_button():
    paginationNextButton = get_element_by_class(driver, 'paginationNextContainer')
    if paginationNextButton != "'paginationNextContainer' not found":
        return True
    else:
        return False
    

# Check if more records exist...
def show_more_results():
    paginationNextButton = get_element_by_class(driver, 'paginationNextContainer')
    classes = paginationNextButton.get_attribute("class")
    if classes.find("inactive") == -1:
        paginationNextButton.click()
        return True
    else:
        return False


# ------------ MAIN Loop ------------

# Set the active stat
def set_active_stat(target_stat="Appearances"):
    global default_stat, active_stat

    drop_down_button = get_drop_list_button(default_stat)

    show_drop_list(drop_down_button)

    # item = driver.find_element(By.LINK_TEXT,default_stat)

    # item.click()

    # advertClose()

    item = driver.find_element(By.LINK_TEXT,target_stat)

    item.click()

    advertClose()

    active_stat = target_stat

    time.sleep(2)

       

# Set the active season
def set_active_season(target_season="2022/23"):
    global current_season, active_season

    drop_down_button = get_drop_list_button(current_season)

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(current_season)

    for item in item_list:
        
       if item.text == target_season:
            
            active_season = target_season
            current_season = target_season
            
            item.click()

            time.sleep(2)

            break
        

# Find the required drop-down list...
def set_search_list(find_list = "All Clubs"):
    global first_list_item, drop_down_button

    first_list_item = find_list

    # open_file(find_list)

    drop_down_button = get_drop_list_button(find_list)


# Iterate through a dropdown list...
def extract_list():
    global first_list_item, drop_down_button
   
    open_file(first_list_item)

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(first_list_item)
        

    for item in item_list:

        time.sleep(0.5)

        current_item = item.text

        if current_item != first_list_item:

            print_row(current_item)

            item.click()
        
            table = get_result_table_by_class()

            while print_result_page(table):
                print("More records found...")

            show_drop_list(drop_down_button)


    close_file()


# Print a page of results
def print_result_page(table): 
    global record_index

    time.sleep(1.5)

    results = get_table_rows(table)

    for record in results:
        record_index = record_index + 1

        country = get_country(record)

        player = get_player(record)

        stat = get_stat(record)

        team = get_team(record)

        print_row(str(record_index) + ", " + player["name"] + ", " + country + ", " + stat + ", " + team +  ", " + player["link"])
    
    # Check for pagination
    if has_pagination_next_button():
        return show_more_results()


# Go

init()

set_active_stat("Goals")
set_active_season("2022/23")
set_search_list()

extract_list()

# extract_list('All Nationalities')
# extract_list('All Positions')

shut_down()
