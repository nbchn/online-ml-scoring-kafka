from generic_online_ml_scoring.builder import ConsumerTransformerProducerLoop
from generic_online_ml_scoring.builder import GenericModel
import math


class SquareAllIntPropsModel(GenericModel):
    def __init__(self):
        print("Initialization of model")

    def execute(self, data):
        for key in data:
            yield {
                "key": key,
                "value": math.pow(int(data[key]), 2)
            }


config_path = "../data/testconfig.conf"

loop = ConsumerTransformerProducerLoop(config_path)
loop.submit_model(SquareAllIntPropsModel())
loop.start()


