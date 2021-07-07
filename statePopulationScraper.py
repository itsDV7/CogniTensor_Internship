# pip install xlrd
import xlrd
# pip install requests
import requests
import xlsxwriter
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


def modify_xls(quiet=True):
    """
    Modify .xls file to required format.
    :param quiet: (default: True) - Set verbosity of the function.
    :return years: (defualt: []) - A list of years extracted from the .xls file
    :return state_population_dict: (default: {}) - A dictionary of State Names (keys) and their population data (values)
    """
    book = xlrd.open_workbook("state_population_data.xls", on_demand=True)
    sh = book.sheet_by_index(0)
    state_population_dict = {}
    years = []
    for rows in range(sh.nrows):
        cell_values = [text.value for text in sh.row(rows)]
        useful_cell_values = []
        for value in cell_values:
            if value == '':
                continue
            useful_cell_values.append(str(value).strip())
        if len(useful_cell_values) == 0:
            continue
        if "State/" in useful_cell_values[0]:
            years = sorted([int(float(value)) for value in list(set(useful_cell_values[1:]))])
        if len(useful_cell_values) == 9:
            state_population_dict[useful_cell_values[0]] = [int(float(value)) for value in useful_cell_values[1:]]
    book.release_resources()
    del book
    if not quiet:
        print(f"Years: {years}")
        print(f"State Population Data: {state_population_dict}")
    return years, state_population_dict


def write_xlsx(year_list, population_dict):
    """
    Create a new .xlsx file to write required data in required format
    :param year_list: A list of years
    :param population_dict: A dictionary of "State_Name":[Yearly_Population_data_list] pair of key:value
    :return:
    """
    filename = "Yearly_State_Population.xlsx"
    book = xlsxwriter.Workbook(filename)
    sh = book.add_worksheet()
    row = 0
    col = 0
    for index, year in enumerate(year_list, start=1):
        sh.write(row, col + index, year)
    col = 0
    keys = population_dict.keys()
    for key in keys:
        row += 1
        sh.write(row, col, key)
        for index, item in enumerate(population_dict[key], start=1):
            sh.write(row, col + index, item)
    book.close()
    print(f"Sucessfully written file: {filename}")


if __name__ == "__main__":
    download_xls()
    year_list_data, population_data = modify_xls(quiet=True)
    write_xlsx(year_list=year_list_data, population_dict=population_data)
