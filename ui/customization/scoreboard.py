import csv
from io import StringIO
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from domjudge_tool_cli.commands.general import general_state, get_or_ask_config
from domjudge_tool_cli.commands.scoreboard import titles, scores, summary

def export(
    cid: int,
    url: Optional[str] = None,
):
    if not url:
        client = get_or_ask_config(general_state["config"])
        url = f"{client.host}/public?static=1"

    cookies = None
    if cid:
        cookies = {"domjudge_cid": f"{cid}"}

    res = httpx.get(url, cookies=cookies).content
    soup = BeautifulSoup(res, "html.parser")

    data = []
    data.append(titles(soup.find("tr", class_="scoreheader").find_all("th")))

    elements = soup.find("table", class_="scoreboard").find("tbody").find_all("tr")
    for element in elements:
        if element.find("td", class_="scoresummary"):
            data.append(summary(element))
        else:
            data.append(scores(element))

    # 創建一個 StringIO 物件
    output = StringIO()
    writer = csv.writer(output)

    # 寫入資料
    for row in data:
        writer.writerow(row)

    # 獲取 CSV 格式的資料
    csv_data = output.getvalue()

    return csv_data