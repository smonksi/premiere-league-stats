import time
from selenium import webdriver
from selenium.webdriver.common.by import By

 
# -- Functions --

# Carry out all set up requirements
def init():
    global f, driver

    filename = "Player appearances.csv"

    f = open(filename, "w", encoding="utf-8")

    headers = "Rank, Player, Country, Appearances, Club, Profile, \n"

    f.write(headers)


    driver = webdriver.Chrome()
    
    driver.maximize_window()

    driver.get("https://www.premierleague.com/stats/top/players/appearances")  



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



# Iterate through a dropdown list...
def extract_list(first_item = "All Clubs"):

    drop_down_button = get_drop_list_button(first_item)

    show_drop_list(drop_down_button)

    item_list = get_drop_list_elements(first_item)
        

    for item in item_list:

        current_item = item.text

        print(current_item)

        time.sleep(2)
        
        if current_item != first_item:

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

        country = get_element_by_class(record,'playerCountry').text


        playerCol = get_element_by_class(record, 'playerName')

        player = playerCol.text
        href = ""

        if player != "'playerName' not found":
            href = playerCol.get_attribute('href')


        stat = get_element_by_class(record, 'mainStat').text

        team = get_element_by_class(record, 'statNameSecondary').text

        print_row(str(x) + ", " + player + ", " + country + ", " + stat + ", " + team +  ", " + href)



 

# Go


init()

crap_cutter()

extract_list()

# extract_list('All Nationalities')

# extract_list('2022/23')

# extract_list('All Positions')