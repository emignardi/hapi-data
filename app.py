import requests
from bs4 import BeautifulSoup
import pandas as pd

columns = []
data = []

url = "https://www.hockey-reference.com/leagues/NHL_2024_skaters.html"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

attributes = ["Player", "Age", "Team", "Pos", "GP", "G", "A", "PTS", "+/-", "PIM"]
columns.extend([soup.find("th", attrs={"aria-label": attr}).text for attr in attributes])

rows = soup.find("tbody").find_all("tr")

for current_row in range(len(rows) - 1):
    print(f"Currently scraping row {current_row}")
    row = rows[current_row]
    player_obj = {}
    player_obj["Player"] = row.find("td", attrs={"data-stat": "name_display"}).text
    player_obj["Age"] = row.find("td", attrs={"data-stat": "age"}).text
    player_obj["Team"] = row.find("td", attrs={"data-stat": "team_name_abbr"}).text
    player_obj["Pos"] = row.find("td", attrs={"data-stat": "pos"}).text
    player_obj["GP"] = row.find("td", attrs={"data-stat": "games"}).text
    player_obj["G"] = row.find("td", attrs={"data-stat": "goals"}).text
    player_obj["A"] = row.find("td", attrs={"data-stat": "assists"}).text
    player_obj["PTS"] = row.find("td", attrs={"data-stat": "points"}).text
    player_obj["+/-"] = row.find("td", attrs={"data-stat": "plus_minus"}).text
    player_obj["PIM"] = row.find("td", attrs={"data-stat": "pen_min"}).text
    data.append(player_obj)

df = pd.DataFrame(columns=columns, data=data)
df.to_csv("./players.csv", index=False, encoding='ISO-8859-1')