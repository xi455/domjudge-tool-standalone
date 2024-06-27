import csv
from io import StringIO
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from domjudge_tool_cli.commands.scoreboard import titles, scores, summary

from utils.web import get_config

def export(
    cid: str,
    url: Optional[str] = None,
):
    """
    Export the scoreboard data as a CSV file.

    Args:
        cid (str): The ID of the contest.
        url (str, optional): The URL of the scoreboard. If not provided, it will be obtained from the client configuration.

    Returns:
        str: The CSV data representing the scoreboard.

    """
    if not url:
        client = get_config()
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