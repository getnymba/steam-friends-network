import aiohttp
from bs4 import BeautifulSoup


class Scraper:
    async def crawl_friends_from_id(self, url) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        friends = []

        elements = soup.find_all("div", class_="friendBlock")
        for element in elements:
            user_id = element.find("a", class_="friendBlockLinkOverlay")["href"]
            friends.append(user_id)

        return friends


if __name__ == "__main__":
    import asyncio

    scraper = Scraper()
    result = asyncio.run(scraper.crawl_friends_from_id(76561198023455525))
    print(result)
