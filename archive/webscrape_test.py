from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scrape_site():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')  
    # options.add_argument('--disable-dev-shm-usage') # Not used 
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
    driver.get('https://medium.com/analytics-vidhya/python-webscraping-in-a-docker-container-aca2a386a3c0')
    time.sleep(15)
    src = driver.page_source
    parser = BeautifulSoup(src, "html.parser")
    driver.close()
    print(src) 
    print(parser)

default_args = {
    'owner': 'Kenny'
}

with DAG(
  "webscraper",
  start_date=days_ago(1),
  schedule_interval=None,
  default_args=default_args
) as dag:
    task_a = PythonOperator(
    task_id="scraper",
    python_callable=scrape_site
    )
   
    task_a 