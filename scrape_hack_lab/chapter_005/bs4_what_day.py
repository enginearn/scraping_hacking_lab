#!/bin/bash/env python3

import csv

import requests
from bs4 import BeautifulSoup
import re

url = "https://ja.wikipedia.org/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# today = soup.find("div", attrs={"id": "on_this_day"}).text
# print(today)
today = soup.find("div", attrs={"id": "on_this_day"})
entries = today.find_all("li")

today_list = []
for i, entry in enumerate(entries):
    today_text = entry.get_text().replace("（", "(").replace("）", ")")
    match = re.search("\(([0-9]*?)年\)", today_text)
    if match:
        today_list.append([i + 1, entry.get_text(), match.group(1)])
    else:
        today_list.append([i + 1, entry.get_text()])

with open("what_day_today.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    for i, entry in enumerate(today_list):
        if "：" in today_list[i][1]:
            today_list[i][1] = today_list[i][1].replace("：", ":")
        writer.writerow(entry)

print(today_list)
