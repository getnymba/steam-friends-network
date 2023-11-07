import aiohttp
from bs4 import BeautifulSoup
import re


class Scraper:
    async def crawl_friends_from_id(self, id: int) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://steamcommunity.com/profiles/{id}/friends"
            ) as response:
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        friends = []

        elements = soup.find_all(attrs={"data-steamid": True, "data-search": True})

        for element in elements:
            friends.append((element["data-steamid"], element["data-search"]))

        return friends

    async def crawl_country_from_id(self, id: int) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://steamcommunity.com/profiles/{id}"
            ) as response:
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        profile_flag_element = soup.find("img", class_="profile_flag")

        if profile_flag_element:
            profile_flag_value = profile_flag_element.find_next_sibling(text=True)
            return profile_flag_value.strip() if profile_flag_value else None
        else:
            return None

    async def crawl_steamid_from_profile(self, profile_url) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as response:
                html = await response.text()

        pattern = r'"steamid":"(\d+)"'
        match = re.search(pattern, html)

        if match:
            steamid = match.group(1)
            return int(steamid)
        else:
            return None
