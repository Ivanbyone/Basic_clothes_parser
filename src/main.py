""" Creating basic parser """

import time
import json
from typing import Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

befree_lst_titles: list[str, Any] = []
befree_lst_prices: list[str, Any] = []
befree_lst_discount: list[str, Any] = []
result = {}
parsing_page: int = 1
counter_iter: int = 0

ua_basic = UserAgent(
    browsers=["safari", "chrome", "firefox"],
    os=["macos", "windows"]
)


def befree_parse_titles(ua: UserAgent, lst: list[str, Any], counter: int) -> list[str, Any]:
    """
    Function for parsing titles
    :param ua: Useragent (from global scope 'ua_basic')
    :param lst: list[str, Any] (from global scope 'befree_list_titles')
    :param counter: int (from global scope 'counter_iter')
    :return: list[str, Any] (from global scope 'befree_list_titles')
    """

    for i in range(1, 100):

        if i == 1:
            request = requests.get(
                url="https://befree.ru/muzhskaya/muz-sale?sort_id=3",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            time.sleep(3)

            parser: BeautifulSoup = BeautifulSoup(request.text, "html.parser")
            parse_title = parser.find_all("div", class_="sc-129dae51-0 cfAPXo product-title")

            for data in parse_title:
                lst.append(data.text)
                counter += 1
            counter = 0

        else:
            req = requests.get(
                url=f"https://befree.ru/muzhskaya/muz-sale?sort_id=3&page={i}",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            time.sleep(3)

            parser: BeautifulSoup = BeautifulSoup(req.text, "html.parser")
            parse_title = parser.find_all("div", class_="sc-129dae51-0 cfAPXo product-title")

            for data in parse_title:
                lst.append(data.text)
                counter += 1
            if counter < 36:
                break
            counter = 0
    return lst


def befree_parse_prices(ua: UserAgent, lst: list[str, Any], counter: int) -> list[str, Any]:
    """
    Parsing function for prices
    :param ua:
    :param lst:
    :param counter:
    :return:
    """

    for i in range(1, 100):

        if i == 1:
            request = requests.get(
                url="https://befree.ru/muzhskaya/muz-sale?sort_id=3",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            time.sleep(3)

            parser: BeautifulSoup = BeautifulSoup(request.text, "html.parser")
            parse_price = parser.find_all("div", class_="sc-guDLey jrGgwZ sc-eDLKkx jQvHvV")

            for data in parse_price:
                lst.append(f"{data.text} руб.")
                counter += 1
            counter = 0

        else:
            req = requests.get(
                url=f"https://befree.ru/muzhskaya/muz-sale?sort_id=3&page={i}",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            time.sleep(3)

            parser: BeautifulSoup = BeautifulSoup(req.text, "html.parser")
            parse_price = parser.find_all("div", class_="sc-guDLey jrGgwZ sc-eDLKkx jQvHvV")

            for data in parse_price:
                lst.append(f"{data.text} руб.")
                counter += 1
            if counter < 36:
                break
            counter = 0
    return lst


def befree_parse_discount(ua: UserAgent, lst: list[str, Any], counter: int) -> list[str, Any]:
    """
    Parsing function for prices
    :param ua:
    :param lst:
    :param counter:
    :return:
    """

    for i in range(1, 100):

        if i == 1:
            request = requests.get(
                url="https://befree.ru/muzhskaya/muz-sale?sort_id=3",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            parser: BeautifulSoup = BeautifulSoup(request.text, "html.parser")
            parse_price = parser.find_all("div", class_="sc-guDLey nrKVf")

            for data in parse_price:
                lst.append(f"{data.text}")
                counter += 1
            counter = 0

        else:
            req = requests.get(
                url=f"https://befree.ru/muzhskaya/muz-sale?sort_id=3&page={i}",
                headers={"user-agent": f"{ua.random}"},
                timeout=5
            )

            time.sleep(3)

            parser: BeautifulSoup = BeautifulSoup(req.text, "html.parser")
            parse_price = parser.find_all("div", class_="sc-guDLey nrKVf")

            for data in parse_price:
                lst.append(f"{data.text}")
                counter += 1
            if counter < 36:
                break
            counter = 0
    return lst


def befree_main(ua: UserAgent, result_dict: dict) -> dict:
    """
    Entry point for parser
    :param ua:
    :param result_dict:
    :return:
    """

    req = requests.get(
        url="https://befree.ru/muzhskaya/muz-sale?sort_id=3",
        headers={"user-agent": f"{ua.random}"},
        timeout=5
    )

    if req.status_code == 200:
        befree_parse_titles(ua_basic, befree_lst_titles, counter_iter)
        befree_parse_prices(ua_basic, befree_lst_prices, counter_iter)
        befree_parse_discount(ua_basic, befree_lst_discount, counter_iter)
    else:
        print(f"Ошибка с кодом {req.status_code}")

    for index, data_ in enumerate(befree_lst_titles):
        result_dict[index] = {
            "title": data_,
            "price": befree_lst_prices[index],
            "discount": befree_lst_discount[index]
        }

    return result_dict


if __name__ == "__main__":
    befree_main(ua_basic, result)
    with open("result.json", mode="w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
