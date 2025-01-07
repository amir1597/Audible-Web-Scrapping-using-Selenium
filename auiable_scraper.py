from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = Options()
#options.add_argument("-headless")

website = 'https://www.audible.com/adblbestsellers?ref_pageloadid=XtrrztZCpjK39KPS&pf_rd_p=1fd040d2-b1e2-469e-b3f9-f039ab573663&pf_rd_r=R7RNJCNZP09Y7EYHV15Q&plink=kBReJbhJSrd3rHw9&pageLoadId=FseyBkUPxyHgZ0E9&creativeId=c2e1091d-ff6b-4a30-a52d-c6db1a4d5245&ref=a_hp_t1_navTop_pl0cg1c0r0'
service = Service(executable_path='geckodriver.exe')
driver = webdriver.Firefox(service=service , options=options)
driver.get(website)

#last_page
pagination_bar = driver.find_element(By.XPATH, "//ul[contains(@class ,'pagingElements')]")
pages = pagination_bar.find_elements(By.XPATH, './li')
last_page = int(pages[-2].text)
print(last_page)

book_name =[]
book_rate =[]
book_rate_number =[]
book_author =[]
book_narrator =[]
book_time =[]

current_page = 1
while current_page<=last_page :

    container = WebDriverWait(driver , 5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container ')))
    book_list = WebDriverWait(container , 5).until(EC.presence_of_all_elements_located((By.XPATH,'//li[contains(@class , "productListItem")]')))
    next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH ,'//span[contains(@class , "nextButton")]')))

    for book in book_list:
        book_title = book.find_element(By.XPATH,'.//h3[contains(@class , "bc-heading")]').text
        book_name.append(book_title)
        try:
            book_rate.append(book.find_element(By.XPATH,'.//li[contains(@class , "ratingsLabel")]/span[contains(@class , "pub-offscreen")]').text)
        except:
            book_rate.append('not_rated_yet')
        book_rate_number.append(book.find_element(By.XPATH, './/li[contains(@class , "ratingsLabel")]/span[contains(@class , "bc-color-secondary")]').text)
        book_author.append(book.find_element(By.XPATH, './/li[contains(@class , "authorLabel")]').text)
        try:
            book_narrator.append(book.find_element(By.XPATH, './/li[contains(@class , "narratorLabel")]').text)
        except:
            book_narrator.append('no narrator')
        book_time.append(book.find_element(By.XPATH, './/li[contains(@class , "runtimeLabel")]').text)

    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

df = pd.DataFrame({'book_name':book_name ,'book_rate':book_rate,'book_rate_number':book_rate_number,'book_narrator':book_narrator,'book_time':book_time})
df.to_csv('best_seller_books.csv',index=False)

driver.quit()
