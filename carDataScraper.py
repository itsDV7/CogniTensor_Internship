import os
import csv
# pip install requests
import requests
# pip install beautifulsoup4
# pip install lxml
from bs4 import BeautifulSoup


def scrape(quiet=True):
    """
    Scrapes car sales data and writes it into csv_car_sales.csv in directory CarSalesData.
    :param quiet: (Default: True) Set verbosity of the output.
    :return data: Returns a list of Category, Sales and Grand Total of the scraped data.
    """
    url = "https://www.siam.in/statistics.aspx?mpgid=8&pgidtrail=14"
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, "lxml")
    vehicle_type = ["Passenger Vehicles", "Commercial Vehicles", "Three Wheelers", "Two Wheelers"]
    table_data = soup.find_all(name="tr")
    header = table_data[0].text.strip().split("\n")
    sales_data_list = []
    for data in table_data[1:]:
        if data.find(name="td").text in vehicle_type:
            sales_data_list.append([text_.text for text_ in data.find_all(name="td")])
        elif data.find(name="td").text == "Quadricycle":
            quadricycle_data = [text_.text for text_ in data.find_all(name="td")]
        elif data.find(name="td").text == "Grand Total":
            grand_total_data = [text_.text for text_ in data.find_all(name="td")]
    for index, total in enumerate(grand_total_data[1:], start=1):
        grand_total_data[index] = int(grand_total_data[index].replace(",", "")) \
                                  - int(quadricycle_data[index].replace(",", ""))
    data = [header, *sales_data_list, grand_total_data]
    try:
        filename = "/CarSalesData/csv_car_sales.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except Exception as e:
        print(e)
    if not quiet:
        print(data)
    return data


if __name__ == "__main__":
    scrape(quiet=True)
