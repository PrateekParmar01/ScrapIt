from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import warnings
import csv


warnings.filterwarnings("ignore")
csv.register_dialect(
    "escaped", escapechar="\\", doublequote=True, quoting=csv.QUOTE_ALL
)

query = "web developer"
location = "India"


url = f"https://in.indeed.com/jobs?q={query.replace(' ','+')}&l={location}"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
stealth(
    driver,
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
    # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
driver.get(url)

script = """
window.scrollTo(0, document.body.scrollHeight);
"""
driver.execute_script(script)

job_cards = driver.find_elements(
    By.CSS_SELECTOR, "div.cardOutline.tapItem.fs-unmask.result"
)
job_links = []
jobs_page_source = []
# job_cards = job_cards[:4]
filename = filename = f"{query} jobs in {location} indeed.csv"
seen=set()
with open(filename, "w", newline='') as myfile:
    spamWriter = csv.writer(myfile, dialect='excel')
    spamWriter.writerow(["Job Title","Company","Salary","URL","Job type"])
    for card in job_cards:
        card.click()
        sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        job_links.append(driver.current_url)
        jobs_page_source.append(driver.page_source)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(1)

    driver.quit()
    entries = []

    for i in range(0, len(jobs_page_source)):
        page = jobs_page_source[i]
        url = job_links[i]
        soup = BeautifulSoup(page, "html.parser")
        try:
            details = soup.find("div", id="jobDetailsSection")
            details = details.children  # type: ignore
            details = [x for x in details][1:]
            entry = {}
            companyinfo = soup.find("div",class_="jobsearch-CompanyInfoContainer").text
            entry["Company"] = companyinfo
            entry["URL"] = url
            l=["WEB DEVELOPER","NA","NA","NA","NA"]
            l[1]=companyinfo
            l[3]=url
            for detail in details:
                field, value = [x for x in detail.children]  # type: ignore
                field = field.text
                value = value.text
                if(field=="Job type"):
                    l[4]=value
                else:
                    l[2]=value
                entry[field] = value
            entries.append(entry)
            spamWriter.writerow(l)
            seen.add(l[1])
        except Exception as e:
            print(e)
print(entries)