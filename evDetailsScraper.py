import re
# pip install requests
import requests
# pip install numpy
import numpy as np
# pip install pandas
import pandas as pd
# pip install seaborn
import seaborn as sns
# pip install beautifulsoup4
# pip install lxml
from bs4 import BeautifulSoup
# pip install matplotlib
import matplotlib.pyplot as plt
# pip install sklearn
from sklearn.preprocessing import MinMaxScaler

main_url = "https://fame2.heavyindustry.gov.in/ModelUnderFame.aspx"
html_page = requests.get(main_url).text
soup = BeautifulSoup(html_page, 'lxml')
table_body = soup.find_all(name="a", id="btnShow")
ev_ids = []

ev_cat_e2w = {
    "range": [],
    "battery_capacity": [],
    "energy_consumption": []
}

ev_cat_e3w = {
    "range": [],
    "battery_capacity": [],
    "energy_consumption": []
}

ev_cat_e4w = {
    "range": [],
    "battery_capacity": [],
    "energy_consumption": []
}

for content in table_body:
    href = content['href']
    ev_details_url = f"https://fame2.heavyindustry.gov.in/{href}"
    details_page = requests.get(ev_details_url).text
    soup = BeautifulSoup(details_page, 'lxml')
    vehicle_cat_soup = soup.find(name="span", id="lblOEMname").text
    re_query = "\((.*)\)$"
    vehicle_cat = re.findall(re_query, vehicle_cat_soup)
    if vehicle_cat:
        details_table_body = soup.find_all(name="table", class_="table table-bordered custom_table")
        for details in details_table_body:
            if vehicle_cat[0] == "e-2W":
                ev_cat_e2w["range"].append(float(details.find(name="span", id="lblRange").text))
                ev_cat_e2w["battery_capacity"].append(float(details.find(name="span", id="lblBatteryCapacity").text))
                ev_cat_e2w["energy_consumption"].append(float(details.find(name="span", id="lblEnergyConsumption")
                                                              .text))
            elif vehicle_cat[0] == "e-3W":
                ev_cat_e3w["range"].append(float(details.find(name="span", id="lblRange").text))
                ev_cat_e3w["battery_capacity"].append(float(details.find(name="span", id="lblBatteryCapacity").text))
                ev_cat_e3w["energy_consumption"].append(float(details.find(name="span", id="lblEnergyConsumption")
                                                              .text))
            elif vehicle_cat[0] == "e-4W":
                ev_cat_e4w["range"].append(float(details.find(name="span", id="lblRange").text))
                ev_cat_e4w["battery_capacity"].append(float(details.find(name="span", id="lblBatteryCapacity").text))
                ev_cat_e4w["energy_consumption"].append(float(details.find(name="span", id="lblEnergyConsumption")
                                                              .text))

mean_e2w_range = np.mean(ev_cat_e2w['range'])
mean_e2w_battery_capacity = np.mean(ev_cat_e2w['battery_capacity'])
mean_e2w_energy_consumption = np.mean(ev_cat_e2w['energy_consumption'])

mean_e3w_range = np.mean(ev_cat_e3w['range'])
mean_e3w_battery_capacity = np.mean(ev_cat_e3w['battery_capacity'])
mean_e3w_energy_consumption = np.mean(ev_cat_e3w['energy_consumption'])

mean_e4w_range = np.mean(ev_cat_e4w['range'])
mean_e4w_battery_capacity = np.mean(ev_cat_e4w['battery_capacity'])
mean_e4w_energy_consumption = np.mean(ev_cat_e4w['energy_consumption'])

print(mean_e2w_range, mean_e2w_battery_capacity, mean_e2w_energy_consumption)
print(mean_e3w_range, mean_e3w_battery_capacity, mean_e3w_energy_consumption)
print(mean_e4w_range, mean_e4w_battery_capacity, mean_e4w_energy_consumption)

print(min(ev_cat_e2w['range']), min(ev_cat_e2w['battery_capacity']), min(ev_cat_e2w['energy_consumption']))
print(min(ev_cat_e3w['range']), min(ev_cat_e3w['battery_capacity']), min(ev_cat_e3w['energy_consumption']))
print(min(ev_cat_e4w['range']), min(ev_cat_e4w['battery_capacity']), min(ev_cat_e4w['energy_consumption']))

print(max(ev_cat_e2w['range']), max(ev_cat_e2w['battery_capacity']), max(ev_cat_e2w['energy_consumption']))
print(max(ev_cat_e3w['range']), max(ev_cat_e3w['battery_capacity']), max(ev_cat_e3w['energy_consumption']))
print(max(ev_cat_e4w['range']), max(ev_cat_e4w['battery_capacity']), max(ev_cat_e4w['energy_consumption']))

# scaler = MinMaxScaler()
#
# ev_cat_e2w['range'] = [data_point[0] for data_point in scaler.fit_transform(np.array(ev_cat_e2w['range'])
#                                                                             .reshape(-1, 1))]
# ev_cat_e2w['battery_capacity'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e2w['battery_capacity']).reshape(-1, 1))]
# ev_cat_e2w['energy_consumption'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e2w['energy_consumption']).reshape(-1, 1))]
#
# ev_cat_e3w['range'] = [data_point[0] for data_point in scaler.fit_transform(np.array(ev_cat_e3w['range'])
#                                                                             .reshape(-1, 1))]
# ev_cat_e3w['battery_capacity'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e3w['battery_capacity']).reshape(-1, 1))]
# ev_cat_e3w['energy_consumption'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e3w['energy_consumption']).reshape(-1, 1))]
#
# ev_cat_e4w['range'] = [data_point[0] for data_point in scaler.fit_transform(np.array(ev_cat_e4w['range'])
#                                                                             .reshape(-1, 1))]
# ev_cat_e4w['battery_capacity'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e4w['battery_capacity']).reshape(-1, 1))]
# ev_cat_e4w['energy_consumption'] = [data_point[0] for data_point in scaler.fit_transform(np.array(
#     ev_cat_e4w['energy_consumption']).reshape(-1, 1))]
#
# ev_cat_e2w_data = pd.DataFrame(data=ev_cat_e2w)
# ev_cat_e3w_data = pd.DataFrame(data=ev_cat_e3w)
# ev_cat_e4w_data = pd.DataFrame(data=ev_cat_e4w)
#
# sns.scatterplot(data=ev_cat_e2w_data)
# plt.show()
# sns.scatterplot(data=ev_cat_e3w_data)
# plt.show()
# sns.scatterplot(data=ev_cat_e4w_data)
# plt.show()
