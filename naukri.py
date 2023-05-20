from subprocess import Popen
import csv
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import warnings

warnings.filterwarnings("ignore")
csv.register_dialect(
    "escaped", escapechar="\\", doublequote=True, quoting=csv.QUOTE_ALL
)
sear = "web developer"
location = "India"

naukriurl = f'https://www.naukri.com/{sear.replace(" ", "-")}-jobs-in-{location.replace(" ", "+")}'
filename = f"{sear} jobs in {location} naukri.csv"
seen = set()
with open(filename, "w", newline="") as myfile:
    spamWriter = csv.writer(myfile, dialect="excel")
    spamWriter.writerow(["Job Title", "Company", "Location", "Salary", "Link"])
    naukriurls = [naukriurl, naukriurl + "-2", naukriurl + "-3"]
    for naukriurl in naukriurls:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-sh-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3"
        )
        driver = webdriver.Chrome(
            executable_path="chromedriver", options=chrome_options
        )

        driver.get(naukriurl)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        src = driver.page_source
        driver.close()
        page_soup = soup(src, "html.parser")
        print(naukriurl)

        containers = page_soup.findAll("div", {"class": "jobTupleHeader"})
        for container in containers:
            name_container1 = container.find("a", {"class": "title"})
            link = name_container1.get("href")
            jobtitle = name_container1.text
            cycontainer = container.find("div", {"class": "companyInfo"})
            cy = cycontainer.find("a")
            com = cy.text
            loc = container.find("li", {"class": "location"})
            locs = loc.find("span")
            loc = locs.text
            salary = container.find("li", {"class": "salary"})
            sal = salary.find("span")
            salary = sal.text
            l = [
                str(str(jobtitle).strip()),
                str(str(com.strip())),
                str(str(loc).strip()),
                str(str(salary).strip()),
                f'=HYPERLINK("{str(str(link).strip())}")',
            ]
            if l[1] not in seen:
                spamWriter.writerow(l)
                seen.add(l[1])
        myfile.flush()
p = Popen(filename, shell=True)
