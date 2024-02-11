class DataframeOperations:
    def add_data_to_df(self, df, data):
        if data[0] not in df["id"].values:
            df.loc[len(df)] = data

    def create_source_target_df(self, df):
        df["friends"] = df["friends"].apply(eval)

        # Use explode to transform the lists into separate rows
        result_df = df.explode("friends")

        # Rename columns to match your desired output
        result_df.columns = ["source", "target"]
        return result_df

    def create_attribute_df(self, orig_df):
        return orig_df.drop(columns=["friends"])
