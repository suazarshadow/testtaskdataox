import asyncio
from scraper import Scraper
from parser import Parser
from orm import ORM 
import datetime
import sys
import workers 

STATE_FILE = "state.txt"
START_URL = "https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page={0}&limit=100"


def write_state(last_page=None, last_url=None, status="RUNNING", reason="NORMAL"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    state = {
        "LAST_PAGE": last_page,
        "LAST_CHECK": now,
        "STATUS": status,
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        for k, v in state.items():
            if v is not None:
                f.write(f"{k}={v}\n")

def read_state():
    state = {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    state[k] = v
    except FileNotFoundError:
        pass
    return state



def main():
    scraper = Scraper()
    parser = Parser()
    orm = ORM()
    #numberOfPages = scraper.get_umber_of_pages(url=START_URL)
    state = read_state()
    number_of_pages = 1
    number_of_start_page = 1
    current_page = 0
    next_url = START_URL

    try: 
        workers.worker(orm, parser, scraper, number_of_start_page, number_of_pages)
        
    
    except Exception as e:
        write_state(
            last_page=current_page,
            status="REQUEST ERROR",
        )
        print(f"{e}")
        sys.exit(1)
            

    


if __name__ == '__main__':
    main()