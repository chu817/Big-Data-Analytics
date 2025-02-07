import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
#This is written by Himani S Kumar 22MIA1092

#URL of the page i used is below

URL = "https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(URL)

wait = WebDriverWait(driver, 10)

from selenium.webdriver.common.action_chains import ActionChains

while True:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//span[contains(text(), "100 more")]]')))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more_button)
        time.sleep(1) 
        actions = ActionChains(driver)
        actions.move_to_element(load_more_button).click().perform()
        
        print("Clicked '100 more' button.")
        time.sleep(1)

    except Exception as e:
        print("No more '100 more' button found or all movies loaded.")
        break

page_source = driver.page_source
driver.quit()

soup = BeautifulSoup(page_source, "html.parser")

movie_containers = soup.find_all("div", class_="ipc-metadata-list-summary-item__c")

movies_list = []

for container in movie_containers:
    title_tag = container.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"
    index = title.split('.', 1)[0] if '.' in title else "N/A"
    title = title.split('.', 1)[1] if '.' in title else title

    metadata_tags = container.find_all("span", class_="sc-d5ea4b9d-7 URyjV dli-title-metadata-item")
    
    year = metadata_tags[0].text.strip() if len(metadata_tags) > 0 else "N/A"
    duration = metadata_tags[1].text.strip() if len(metadata_tags) > 1 else "N/A"
    age_rating = metadata_tags[2].text.strip() if len(metadata_tags) > 2 else "N/A"

    rating_tag = container.find("span", class_="ipc-rating-star--rating")
    rating = rating_tag.text.strip() if rating_tag else "N/A"

    vote_tag = container.find("span", class_="ipc-rating-star--voteCount")
    votes = vote_tag.text.strip().replace("(", "").replace(")", "") if vote_tag else "N/A"

    metacritic_tag = container.find("span", class_="sc-b0901df4-0 bXIOoL metacritic-score-box")
    metacritic_score = metacritic_tag.text.strip() if metacritic_tag else "N/A"

    movies_list.append({
        "Index": index,
        "Title": title,
        "Duration": duration,
        "Year": year,
        "Age Rating": age_rating,
        "IMDb Rating": rating,
        "Votes": votes,
        "Metacritic Score": metacritic_score
    })

df = pd.DataFrame(movies_list)
df.to_csv("movies.csv", index=False)

print(f"Scraping complete! {len(movies_list)} movies saved to 'movies.csv'.")
