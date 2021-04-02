from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_element(x_path):
    global driver
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, f"{x_path}"))
        )
        return element
    except:
        return 0

categories = {
    "house":"https://elements.envato.com/audio/genre-house/min-length-01:30/max-length-03:00/sort-by-latest",
    "jazz":"https://elements.envato.com/audio/genre-jazz/min-length-01:30/max-length-03:00/sort-by-latest",
    "lofi":"https://elements.envato.com/audio/genre-lofi/min-length-01:30/max-length-03:00/sort-by-latest",
    "lounge":"https://elements.envato.com/audio/genre-lounge/min-length-01:30/max-length-03:00/sort-by-latest",
    "metal":"https://elements.envato.com/audio/genre-metal/min-length-01:30/max-length-03:00/sort-by-latest",
    "rock":"https://elements.envato.com/audio/genre-ock/min-length-01:30/max-length-03:00/sort-by-latest",
    "blues":"https://elements.envato.com/audio/genre-blues/min-length-01:30/max-length-03:00/sort-by-latest"
}

driver = webdriver.Chrome(executable_path='/Users/artsiom/Music-Botting/envato/chromedriver')

#/html/body/div[2]/div[1]/main/div/div/section/div/div[3]/div[3]/div[1]/ul/li[1]/div/a
#/html/body/div[2]/div[1]/main/div/div/section/div/div[3]/div[3]/div[1]/ul/li[2]/div/a
#/html/body/div[2]/div[1]/main/div/div/section/div/div[3]/div[3]/div[1]/ul/li[24]/div/a





for each in categories:
    driver.get(categories[each])
    ntfctn = wait_element('//*[@id="app"]/div[1]/main/div/div/section/div/div[3]/div[2]/div[2]/div/select').text

    #print(ntfctn)

    sleep(2)
    
    next_but_is_not_found = False
    link_number = 2
    while not next_but_is_not_found:
        for i in range(1,25):           # 24 songs on the page
            element = wait_element(f'/html/body/div[2]/div[1]/main/div/div/section/div/div[3]/div[3]/div[1]/ul/li[{i}]/div/a')
            element.location_once_scrolled_into_view
            href = element.get_attribute('href')
            sleep(0.5)
            print(href)

        try:
            next_but = driver.find_element_by_link_text(f'{link_number}')
                                                    
            next_but.click()
            ntfctn = wait_element('//*[@id="app"]/div[1]/main/div/div/section/div/div[3]/div[2]/div[2]/div/select').text
            link_number += 1
        except:
            next_but_is_not_found = True
            print('Next page is not found')
            break


sleep(5)

driver.quit()









