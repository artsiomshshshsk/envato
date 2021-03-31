from selenium import webdriver
from time import sleep


driver = webdriver.Chrome(executable_path='/Users/artsiom/Music-Botting/envato/chromedriver')
driver.get('https://elements.envato.com/audio')


categories = {
    "house":"https://elements.envato.com/audio/genre-house/min-length-01:30/max-length-03:00/sort-by-latest",
    "jazz":"https://elements.envato.com/audio/genre-jazz/min-length-01:30/max-length-03:00/sort-by-latest",
    "lofi":"https://elements.envato.com/audio/genre-lofi/min-length-01:30/max-length-03:00/sort-by-latest",
    "lounge":"https://elements.envato.com/audio/genre-lounge/min-length-01:30/max-length-03:00/sort-by-latest",
    "metal":"https://elements.envato.com/audio/genre-metal/min-length-01:30/max-length-03:00/sort-by-latest",
    "rock":"https://elements.envato.com/audio/genre-ock/min-length-01:30/max-length-03:00/sort-by-latest",
    "blues":"https://elements.envato.com/audio/genre-blues/min-length-01:30/max-length-03:00/sort-by-latest"
}


sleep(5)

driver.quit()









