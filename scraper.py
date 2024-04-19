from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import time 

LEAGUE_URL = "https://www.fonbet.com.cy/sports/hockey/13283/?mode=1"

def scrape():
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    
        
    # option very important to scraping the entire odds of every match
    chr_options.add_argument("--start-maximized")
    chr_options.add_argument("--headless")

    # start the webdriver and get to the leagues url
    driver = webdriver.Chrome(options=chr_options)
    driver.get(LEAGUE_URL)

    try:
        # check if the web elements loaded 
        test = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sport-base-event--pDx9cf _compact--5fB1ok']")))
    except TimeoutException:
        print("The expected element was not found within the timeout period.")
        driver.quit()  # Close the browser
        return None  # Or any other appropriate action
    # scrape all the current matches and their respective data
    matches = driver.find_elements(By.XPATH,"//div[@class='sport-base-event--pDx9cf _compact--5fB1ok']")
    
    # load previous data
    file = open("bot_results.txt", 'r')
    old_data = file.read().split("\n")
    file.close()

    new_data = []
    bot_results = []

    # flag that tells wether or not new matches have been added to the list 
    change = False

    # scrape all the data from each game
    for match in matches:
        
        # scrape game teams names and clean it up
        teams_raw = match.find_element(By.XPATH, ".//a[@class='table-component-text--5BmeJU sport-event__name--HefZLq _clickable--G5cwQm _event-view--7J8rEd _compact--7BwYe1']").text
        teams_raw = teams_raw.split("—")
        teams = teams_raw[0] + "vs" + teams_raw[1]
        
        # scrape 1, x, 2, over and under odds
        odds = match.find_elements(By.XPATH, ".//div[@class='table-component-factor-value_single--6nfox5 _compact--7j5yEe cell-state-normal--iYJc0x value-state-normal--4JL4xN']")
        team1 = odds[0].text
        draw = odds[1].text
        team2 = odds[2].text
        over = odds[3].text
        under = odds[4].text

        # scrape total value 
        total_raw = match.find_element(By.XPATH, ".//div[@class='table-component-factor-value_param--5xDx2Q _compact--7j5yEe']")
        total = total_raw.find_element(By.TAG_NAME, "span").text
          

        # scrape asian handicap values
        ah_home_odds = []
        ah_raw = match.find_elements(By.XPATH, ".//div[@class='table-component-factor-value_complex--25G2ok _compact--7j5yEe cell-state-normal--iYJc0x']")
        ah_home = ah_raw[0].find_elements(By.TAG_NAME, "span")
        for a in ah_home:
            ah_home_odds.append(a.text)
        
        ah_away_odds = []
        ah_away = ah_raw[1].find_elements(By.TAG_NAME, "span") 
        for a in  ah_away:
            ah_away_odds.append(a.text)

        new_data.append((str(teams)+'\n'))
        new_data.append((team1 + " " + draw + " " + team2 + " " + ah_home_odds[1]+ " " + ah_away_odds[1] + " " + over + " " + under + " " + "\n"))

        # if the match already exists in bot_results.txt provide previous data
        if teams in old_data:
            match_old_data_index = old_data.index(teams)
            match_old_data = old_data[match_old_data_index + 1].split(" ")

            bot_results.append(
                f"**{teams}**\n"
                f"HOME: {team1} (was {match_old_data[0]})\n"
                f"DRAW: {draw} (was {match_old_data[1]})\n"
                f"AWAY: {team2} (was {match_old_data[2]})\n"
                f"AH HOME: {ah_home_odds[0]} {ah_home_odds[1]} (was {match_old_data[3]})\n" 
                f"AH AWAY:  {ah_away_odds[0]} {ah_away_odds[1]} (was {match_old_data[4]})\n" 
                f"OVER: {total} {over} (was {match_old_data[5]})\n"
                f"UNDER {total} {under} (was {match_old_data[6]})\n"   
            )

            # check if any odds have changed
            if team1 != match_old_data[0]:
                change = True  
            if draw != match_old_data[1]:
                change = True
            if team2 != match_old_data[2]:
                change= True               
            if ah_home_odds[1] != match_old_data[3]:
                change = True
            if ah_away_odds[1] != match_old_data[4]:
                change = True              
            if over != match_old_data[5]:
                change = True
            if under != match_old_data[6]:
                change = True        
                     
        else:
            bot_results.append(
                f"**{teams}**\n"
                f"HOME: {team1} (no old data)\n"
                f"DRAW: {draw} (no old data)\n"
                f"AWAY: {team2} (no old data)\n"
                f"AH HOME: {ah_home_odds[0]} {ah_home_odds[1]} (no old data)\n" 
                f"AH AWAY:  {ah_away_odds[0]} {ah_away_odds[1]} (no old data)\n" 
                f"OVER: {total} {over} (no old data)\n"
                f"UNDER {total} {under} (no old data)\n"
                
            )
            change = True

    # write the new data in bot_results.txt file           
    file = open("bot_results.txt", "w")
    for d in new_data:
        file.write(d)
    file.close()    

    # write the new data in the display_results.txt file and notify the user if any new matches have been added
    # the display_results.txt file is only to organize the data before sending it to the bata
    file = open('display_results.txt', 'w', encoding="utf-8")
    if change:
        file.write("new changes have been added \n")
    for bot_result in bot_results:
        file.write(bot_result)
        file.write("\n")
    file.close()    
    
    try:
        test = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sport-base-event--pDx9cf _compact--5fB1ok']")))
    except TimeoutException:
        print("The expected element was not found within the timeout period.")
        driver.quit()  # Close the browser
        return None  # Or any other appropriate action
    
    # close the driver when done
    driver.quit()
    return change


if __name__ == "__main__":
    scrape()