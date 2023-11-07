import pandas as pd
import ast


class DataframeOperations:
    def add_data_to_df(self, df, data):
        df.loc[len(df)] = data

    def create_source_target_df(self, orig_df):
        st_df = pd.DataFrame(columns=["source", "target"])
        for id in orig_df["id"]:
            friends = ast.literal_eval(
                orig_df[orig_df["id"] == id]["friends"].values[0]
            )
            for friend in friends:
                if (
                    st_df[
                        ((st_df["source"] == id) & (st_df["target"] == friend[0]))
                        | ((st_df["target"] == id) & (st_df["source"] == friend[0]))
                    ].shape[0]
                    <= 0
                ):
                    self.add_data_to_df(st_df, [id, friend[0]])

        return st_df

    def create_attribute_df(self, orig_df):
        return orig_df.drop(columns=["friends"])
