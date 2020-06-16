import json
import pandas as pd


class TestMsg:

    def value(self):
        return {"x1": 1, "x2": 2, "x3": 3, "x4": 4}

    def error(self):
        return None


def preprocessing(in_json):
    return pd.DataFrame(data=in_json, index=[0])


def predict(df):
    return pd.DataFrame(data={"prediction": [2]})


def postprocessing(df):
    return df.to_dict('records')[0]


class TestModel:
    def predict(self, df):
        return pd.DataFrame(data={"prediction": [2]})


_preproc_func = preprocessing
_postproc_func = postprocessing
_model = TestModel()

while True:
    try:
        msg = TestMsg()

        if msg.error() or msg is None:
            print(f"Consumer error : {msg.value()}")
            continue

        # 1. get raw value
        # value = json.loads(msg.value())
        value = msg.value()
        print(value)
        # 2. apply preprocessing function
        # this should return a pd.Dataframe
        value_preprocessed = _preproc_func(value)
        print(value_preprocessed)
        # 3. apply model prediction
        value_predicted = _model.predict(value_preprocessed)
        print(value_predicted)
        # 4. apply postprocessing function
        value_postprocessed = _postproc_func(value_predicted)
        print(value_postprocessed)

        data_out = value
        data_out["output"] = value_postprocessed

        print(data_out)

    except KeyboardInterrupt:
        break
