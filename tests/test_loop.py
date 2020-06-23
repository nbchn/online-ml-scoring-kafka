import json
from generic_online_ml_scoring.builder import GenericModel


class TestMsg:

    def key(self):
        return "test"

    def value(self):
        return json.dumps({"x1": 1, "x2": 2, "x3": 3, "x4": 4})

    def error(self):
        return None


class TestModel(GenericModel):
    pass


_model = TestModel()

while True:
    try:
        msg = TestMsg()

        if msg.error() or msg is None:
            print(f"Consumer error : {msg.value()}")
            continue

        # Get raw key/value
        # we assume key is kept unchanged
        key = msg.key()
        value = json.loads(msg.value())

        for model_output in _model.execute(value):
            print(model_output)

    except KeyboardInterrupt:
        break

