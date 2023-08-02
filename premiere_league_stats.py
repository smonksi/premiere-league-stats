import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathvalidate import sanitize_filename
import argparse
from termcolor import colored



 
# ------------ Init & Shutdown ------------

# Carry out set up requirements
def init():
    global driver, current_season, default_stat

    define_arguments()
    if has_arguments():
        show_arguments()
        # print(get_argument())
    
    # exit()

    current_season = "2022/23"
    default_stat = "Goals"

    driver = webdriver.Chrome()
    
    # if platform.system() == 'Windows':
    #     driver.maximize_window()

    driver.get("https://www.premierleague.com/stats/top/players/appearances")  

    crap_cutter()


# Shut down the web browser etc
def shut_down():
    global driver
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



# ------------ Command Line Arguments ------------

# Define command line arguments
def define_arguments():
    global parser
    parser = argparse.ArgumentParser(description='Please enter stat type --stat -s e.g. Appearances, Goals, Assists etc...')
    parser.add_argument('-s', '--statistic', type=str) #, default="Appearances")
    parser.add_argument('-y','--season', type=str)
    parser.add_argument('-c','--club', action='store_true')
    parser.add_argument('-n','--nationality', action='store_true')
    parser.add_argument('-p','--position', action='store_true')


# Show all command line arguments
def has_arguments():

    return get_argument("statistic") != None


# Show all command line arguments
def show_arguments():
    global parser

    str =colored("Search request ", 'dark_grey')  #\n"

    args = parser.parse_args()

    for arg, value in vars(args).items():
        if type(value) != bool:
            str += arg.capitalize() + ' is ' + colored(value, 'green') + ", "
        elif value:
            str += "grouped by " + colored(arg.capitalize(), 'green')

    print(str)


# Retrieve a command line argument
def get_argument(arg="statistic"):
    global parser

    args = parser.parse_args()

    return getattr(args,arg)


# Get search filter
def get_search_filter():
    global parser

    args = parser.parse_args()

    # if getattr(args,'club'):
    #     return "All Clubs"
    
    if getattr(args,'nationality'):
        return "All Nationalities"
    
    if getattr(args,'position'):
        return "All Positions"
    
    return "All Clubs"



# ------------ File Handling ------------

# Open file and name it based on current search
def open_file(filename):
    global f, active_season, active_stat

    filename = "Player " + active_stat.lower() + " " + filename.lower() + " " + active_season + ".csv"

    filename = sanitize_filename(filename,"-")

    f = open(filename, "w", encoding="utf-8")

    headers = "Rank, Player, Country, " + active_stat + ", Club, Profile, \n"

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

# Find an element by tag & text
def get_element_by_text(element, text, tag="div"):

    class result:
        text = ''

    try:
        result = element.find_element(By.XPATH,".//" + tag + "[text()='" + text + "']")
    
    except:
        result.text = "'" + text + "' not found"

    return result


# Find an element by a link text
def get_element_by_link_text(element, text):

    class result:
        text = ''

    try:
        result = element.find_element(By.LINK_TEXT,text)
    
    except:
        result.text = "'" + text + "' not found"

    return result


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


# Find the element (div) that opens the drop-down list when clicked
def get_filter_button(text = "   Filter by Season  "):
    global driver

    filter_name_div = get_element_by_text(driver, text)

    return get_next_element(filter_name_div)


# Find the parent of the supplied element
def get_parent_element(element):

    return element.find_element(By.XPATH,"..")


# Find the next sibling of the supplied element
def get_next_element(element, tag="div"):

    return element.find_element(By.XPATH,"following-sibling::" + tag)


# Find one element in a ul in order to find all its li elements
def get_drop_list_elements(text, tag='li'):
    global driver
    
    # li = driver.find_element(By.XPATH,".//" + tag + "[text()='" + text + "']")
    li = get_element_by_text(driver,text, tag)

    ul = get_parent_element(li)

    return ul.find_elements(By.TAG_NAME,"li")


# Get rows in a table
def get_table_rows(table):

    if no_content(table):
        return []

    return table.find_elements(By.TAG_NAME,"tr")


# Find out if we have more rows in this record set
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

    # drop_down_button = get_drop_list_button(default_stat)

    drop_down_button = get_filter_button("Filter by Stat Type")

    show_drop_list(drop_down_button)

    drop_list = get_next_element(drop_down_button)

    item = get_element_by_link_text(drop_list,target_stat)
    
    if item.text.find("not found") > -1:

        print("ERROR: The target statistic (" + target_stat + ") was not found, defaulting to " + default_stat)
        show_drop_list(drop_down_button) # close drop down list
        set_active_stat(default_stat)

    else:
        item.click()

        advertClose()

        active_stat = target_stat


    time.sleep(2)


# Set the active season
def set_active_season(target_season="2022/23"):
    global current_season, active_season

    # drop_down_button = get_drop_list_button(current_season)

    # This method, get_filter_button, should always work regardless 
    # of the current season and as long as the filter name remains the same...
    drop_down_button = get_filter_button()

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(current_season)

    for item in item_list:
        
       if item.text == target_season:
            
            active_season = target_season
            current_season = target_season
            
            item.click()

            time.sleep(2)

            return True

    # If the target season is not found, default to current_season
    print("ERROR: The target season (" + target_season + ") was not found, defaulting to season: " + current_season )
    show_drop_list(drop_down_button) # this closes the button...
    set_active_season(current_season)
    return False


# Find the required drop-down list...
def set_search_list(find_list = "All Clubs"):
    global first_list_item, drop_down_button

    first_list_item = find_list

    drop_down_button = get_drop_list_button(find_list)


# Iterate through a dropdown list...
def extract_list(save = True):
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

            if save:
                while print_result_page(table):
                    print("More records found...")

            show_drop_list(drop_down_button)

    close_file()


# Print a page of results
def print_result_page(table): 
    global record_index

    time.sleep(1.5)

    results = get_table_rows(table)

    if results == []:
        return False

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

if has_arguments():
    set_active_stat(get_argument("statistic"))
    set_active_season(get_argument("season"))
    set_search_list(get_search_filter())
else:
    set_active_stat("Goals")
    set_active_season("2002/03")
    set_search_list("All Positions")

extract_list()

shut_down()
