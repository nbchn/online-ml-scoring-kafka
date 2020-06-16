from generic_online_ml_scoring.builder import Builder
import pandas as pd


def preprocessing(json):
    return pd.DataFrame(data=json, index=[0])


def predict(df):
    return pd.DataFrame(data={"prediction": [2]})


def postprocessing(df):
    return df.to_dict('records')[0]


class TestModel:
    def predict(self, df):
        return pd.DataFrame(data={"prediction": [2]})


config_path = "../data/testconfig.conf"

builder = Builder(config_path, TestModel(), preprocessing, postprocessing)
builder.start()
