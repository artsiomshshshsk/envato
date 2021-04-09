import traceback
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
from getpass import getuser
from selenium.webdriver.chrome.options import Options
import subprocess
import names
import pyautogui
import os
import sys
from zipfile import ZipFile
import wave
import contextlib
import shutil
import random
import sqlite3



def detect_and_solve_captcha():
    global driver
    try:
        status = driver.find_element_by_class_name('status')
    except:

        breakpoint()


def add_url_to_db(url):
    curs.execute('insert into songs values (?)', [url])
    conn.commit()


def if_url_already_in_db(url):
   curs.execute('select * from songs')
   urls = [x[0] for x in curs.fetchall()]
   if url in urls:
       return True


def get_wav_duration(path):
    with contextlib.closing( wave.open( path, 'r' ) ) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float( rate )
        return duration

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))




def wait_element(x_path):
    global driver
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, f"{x_path}"))
        )
        return element
    except:
        return 0

def get_name():
    return names.get_full_name( gender='male')

def remove_all_files_in_directory(path):
    for root, dirs, files in os.walk(r"C:\Users\PC1\Documents\EnvatoDownloader\envato\downloads", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
           shutil.rmtree(os.path.join(root, name))



categories = {
    "house":"https://elements.envato.com/audio/genre-house/min-length-01:30/max-length-02:30/sort-by-latest",
    "jazz":"https://elements.envato.com/audio/genre-jazz/min-length-01:30/max-length-02:30/sort-by-latest",
    "lofi":"https://elements.envato.com/audio/genre-lofi/min-length-01:30/max-length-02:30/sort-by-latest",
    "lounge":"https://elements.envato.com/audio/genre-lounge/min-length-01:30/max-length-02:30/sort-by-latest",
    "metal":"https://elements.envato.com/audio/genre-metal/min-length-01:30/max-length-02:30/sort-by-latest",
    "rock":"https://elements.envato.com/audio/genre-ock/min-length-01:30/max-length-02:30/sort-by-latest",
    "blues":"https://elements.envato.com/audio/genre-blues/min-length-01:30/max-length-02:30/sort-by-latest"
}
os_info = platform.system()
print(os_info)
DB_PATH = 'songs.db'
created = DB_PATH in os.listdir()
conn = sqlite3.connect(DB_PATH)
curs = conn.cursor()
if not created:
    curs.execute('create table songs (url varchar(255));')



downloads_dir = os.path.join(get_script_path(),'downloads')
if not os.path.isdir(downloads_dir):
    os.mkdir(downloads_dir)
    print('Downloads folder is created.')


songs = os.path.join(get_script_path(), 'songs')

if not os.path.isdir(songs):
    os.mkdir(songs)
    print('Songs folder is created.')


if os_info == 'Windows':
    ex_path = 'chromedriver.exe'
    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
    user_data_dir = r"user-data-dir=C:\Users\%s\AppData\Local\Google\Chrome\User Data" % getuser()
    print(user_data_dir)
else:
    pth = get_script_path()
    ex_path = os.path.join(pth,'chromedriver')
    print(ex_path)

    user_data_dir = r"user-data-dir=/Users/%s/Library/Application Support/Google/Chrome/Default" % getuser()
    print(user_data_dir)



chrome_options = Options()
chrome_options.add_argument(user_data_dir)
prefs = {'download.default_directory' : downloads_dir}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=ex_path,chrome_options=chrome_options)


all_genres = [[each, categories[each]] for each in categories]
print(all_genres)
random.shuffle(all_genres)

for each in all_genres:
    category = each[0]

    category_dir = os.path.join(songs, category)
    if not os.path.isdir( category_dir ):
        os.mkdir( category_dir )
        print( f'{category_dir} is created' )

    driver.get(each[1])
    ntfctn = wait_element('//*[@id="app"]/div[1]/main/div/div/section/div/div[3]/div[2]/div[2]/div/select').text
    sleep(2)
    
    next_but_is_not_found = False
    link_number = 2
    while not next_but_is_not_found:
        for i in range(1, 25):       # 24 songs on the page
            element = wait_element(f'/html/body/div[2]/div[1]/main/div/div/section/div/div[3]/div[3]/div[1]/ul/li[{i}]/div/a')
            element.location_once_scrolled_into_view
            href = element.get_attribute('href')

            #href = url of song to check 

            if if_url_already_in_db(href):
                print(f'{href} IS ALREADY DOWNLOADED')
                continue

            driver.execute_script( "window.open('');" )
            driver.switch_to.window(driver.window_handles[1] )
            driver.get(href)

            print(href)

            project_name = get_name()
            download_button = wait_element('/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[2]/div[2]/div[2]/button')
            download_button.location_once_scrolled_into_view
            while True:
                try:
                    pyautogui.press('pageup')
                    sleep(1)
                    download_button.click()
                    sleep(2)
                    create_new_project = wait_element('/html/body/div[8]/div/div/div/div/div/form/div[1]/div[2]/div/div[3]/div[2]')
                    create_new_project.click()
                    project_name_input = wait_element('/html/body/div[8]/div/div/div/div/div/form/div[1]/div[2]/div/div[1]/div/div[2]/input')
                    sleep(2)

                    project_name_input.send_keys(project_name)
                    submit = wait_element('/html/body/div[8]/div/div/div/div/div/form/div[2]/button')
                    remove_all_files_in_directory(downloads_dir)
                    submit.click()
                    break
                except Exception:
                    traceback.print_exc()
            # waiting for file to be downloaded
           
            file_is_downloaded = False
            while not file_is_downloaded:
                for file in os.listdir(downloads_dir):
                    file = os.path.join(downloads_dir,file)
                    if file.endswith('.zip'):
                        file_is_downloaded = True
                        print(f'{file} is downloaded')
                        downloaded_zip = file
                        break

            with ZipFile(downloaded_zip, 'r') as zipObj:
                zipObj.extractall(downloads_dir)
            os.remove(downloaded_zip)

            for file in os.listdir(downloads_dir):
                file = os.path.join(downloads_dir, file)
                if file.endswith('.wav'):
                    dur = int(get_wav_duration(file))
                    if 90 <= dur <= 150:
                        shutil.copy(file, category_dir)
                        break
            remove_all_files_in_directory(downloads_dir)

            add_url_to_db(href)

            driver.close()
            driver.switch_to.window( driver.window_handles[0] )
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









