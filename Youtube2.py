# program that takes in data from a youtube search and saves to an excel
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
search = input("What would you want to look up on youtube.com?: ")

url = f"https://www.youtube.com/results?search_query={search}"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
# scroll func to scroll down in order to load in more videos
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)

scroll_count = 4
for i in range(scroll_count):
    scroll_down(driver)

videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-video-renderer')
video_list = []

videoNum = 0
for video in videos:
    # initialize items incase not available
    author = "N/A"
    title = "N/A"
    views = "N/A"
    date = "N/A"
    description = "N/A"
    videoLink = "N/A"
    if videoNum == 100:
      break
    videoNum += 1
    try:
        author = video.find_element(By.XPATH, './/*[@id="channel-info"]').text
    except:
        pass
    try:
        title = video.find_element(By.XPATH, './/*[@id="video-title"]/yt-formatted-string').text
    except:
        pass
    try:
        views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    except:
        pass
    try:
        date = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
    except:
        pass
    try:
        description = video.find_element(By.XPATH, './/*[@id="dismissible"]/div/div[3]/yt-formatted-string').text
    except:
        pass
    try:
        videoLink = video.find_element(By.XPATH, './/a[contains(@href, "/watch?v=")]').get_attribute("href")
    except:
        pass
    vid_item = {
        'author': author,
        'title': title,
        'views': views,
        'date': date,
        'description' : description,
        'link' : videoLink,
    }
    video_list.append(vid_item)
    print("Successfully copied video #" + str(videoNum))
# stores into an excel
df = pd.DataFrame(video_list)
df.to_excel('youtube_video_data.xlsx', index=False)

driver.quit()
