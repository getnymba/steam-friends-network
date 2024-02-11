import pandas as pd


class Finder:
    def __init__(self, scraper, df_ops):
        self.scraper = scraper
        self.df_ops = df_ops
        self.df = pd.DataFrame(columns=["id", "friends"])

    async def find_st4ck(self, steam_url):
        friends = await self.scraper.crawl_friends_from_id(steam_url)
        visited = []
        queue = [steam_url]
        queue.extend(friends)

        # Convert friends list to pandas Series
        friends_series = pd.Series(friends)

        self.df_ops.add_data_to_df(
            self.df,
            [
                steam_url.split("/")[-1],
                friends_series.map(lambda x: x.split("/")[-1]).tolist(),
            ],
        )
        for friend in queue:
            if "https://steamcommunity.com/id/St4ck" in queue:
                print("St4ck found!")
                break
            # Limit the number of friends to 100
            if len(visited) > 100:
                print("St4ck not found!")
                break
            if friend not in visited:
                friend_of_friends = await self.scraper.crawl_friends_from_id(friend)
                friend_of_friends_series = pd.Series(friend_of_friends)
                queue.extend(friend_of_friends)
                visited.append(friend)
                self.df_ops.add_data_to_df(
                    self.df,
                    [
                        friend.split("/")[-1],
                        friend_of_friends_series.map(
                            lambda x: x.split("/")[-1]
                        ).tolist(),
                    ],
                )
                queue.pop(0)

        self.df.to_csv("./output/data.csv", index=False)
