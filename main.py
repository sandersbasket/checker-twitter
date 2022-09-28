from loguru import logger
import requests
import re
import threading
import glob, os


def response_check(session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    html = session.get("https://twitter.com/home?lang=ru", headers = headers).text
    if not 'screen_name' in html:
        logger.error("not screen")

    find_link = re.findall('screen_name":"([^"]*)"', html)
    logger.info("Name: {}".format(find_link))
    find_link = re.findall('"favourites_count":([0-9]*),', html)
    logger.info("Favourites count: {}".format(find_link))
    find_link = re.findall('"followers_count":([0-9]*),', html)
    logger.info("Subs: {}".format(find_link))
    find_link = re.findall('name":"([^"]*)"', html)
    logger.info("Name: {}".format(find_link))
    find_link = re.findall('"verified":([^"]*)', html)
    logger.info("Verify: {}".format(find_link))

    
def read_file(filename, session):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().split("\n"):
            vals = line.split("\t")
            if len(vals) == 7:
                _, _, _, _, _, name, value = vals
            elif len(vals) == 6:
                _, _, _, _, name, value = vals
            else:
                logger.debug(f"Неизвестный кук {vals}")
                continue
            session.cookies[name] = value
        response_check(session)

if __name__ == "__main__":
    session = requests.Session()
    os.chdir("./cookies")
    for file in glob.glob("*.txt"):
        th = threading.Thread(target=read_file, args=(file, session,)).start()
