import os
# pip install tabula-py
import tabula
# pip install requests
import requests
# pip install beautifulsoup4
# pip install lxml
from bs4 import BeautifulSoup


def download_pdf():
    """
    Downloads PDF file for Gross State Domestic Produce from the RBI website.
    :param: None
    :return pdf_href_list: A list of href/links to the .pdf files.
    """

    url = "https://m.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook+of+Statistics+on+Indian+States"
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')
    report_links = soup.find_all(name="a", class_="link2")
    pdf_href_list = []
    for report_link in report_links:
        if "Gross State Domestic Product" in report_link.text:
            report_href = f"https://m.rbi.org.in/Scripts/{report_link['href']}"
            report_html_page = requests.get(report_href).text
            report_soup = BeautifulSoup(report_html_page, 'lxml')
            pdf_url_soup = report_soup.find(name="td", class_="tableheader")
            pdf_href = pdf_url_soup.find_all(name="a")[1].get("href")
            pdf_name = report_link.text.split(":")[1].replace(" ", "")
            filename = f"/StateGDP/pdf_{pdf_name}.pdf"
            print(f"Downloading File: {pdf_name}")
            response = requests.get(pdf_href)
            pdf_href_list.append(pdf_href)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as pdf:
                pdf.write(response.content)
                pdf.close()
    print("All files Downloaded")
    return pdf_href_list


def convert_pdf():
    """
    Converts the downloaded .pdf files to .csv in batch.
    :param: None
    :return: None
    """

    tabula.convert_into_by_batch("/StateGDP", output_format="csv", pages="all")
    print("Converted all files to .csv")


def read_pdf(pdf_href_list):
    """
    Read .pdf files directly from the href/links and converts them into a Dataframe.
    :param pdf_href_list: A list of href/links to the .pdf files.
    :return df: A Dictionary of Dataframe read from the .pdf files.
    """

    df = {}
    for index, href in enumerate(pdf_href_list):
        df[index] = tabula.read_pdf(input_path=href, pages="all")
    return df


if __name__ == "__main__":
    href_list = download_pdf()
    dataframe = read_pdf(pdf_href_list=href_list)
    print(dataframe)
    convert_pdf()
