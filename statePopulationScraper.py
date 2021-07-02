# pip install requests
import requests
# pip install beautifulsoup4
# pip install lxml
from bs4 import BeautifulSoup


def download_xls():
    """
    Downlaods a .xls file containing data for State Population.
    :param: None
    :return: None
    """
    # URL
    url = "http://mospi.nic.in/statistical-year-book-india/2015/171"
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')
    # Get table content
    table_links = []
    page_table = soup.find_all(name="table", class_="views-table")
    for content in page_table:
        table_links = content.find_all(name="a")
    # Try: Check if required_doc exists in table
    try:
        required_doc = "Mid Year Population"
        state_population_href = [link['href'] for link in table_links if required_doc in link.text][0]
        response = requests.get(state_population_href)
        # Open file with filename and write bytes
        filename = "state_population_data.xls"
        with open(filename, 'wb') as xls:
            xls.write(response.content)
            xls.close()
        print("File Downloaded!")
    except Exception as e:
        print("No Data Found!", e)


if __name__ == "__main__":
    download_xls()
