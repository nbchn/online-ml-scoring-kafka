from generic_online_ml_scoring.builder import ConsumerTransformerProducerLoop
from generic_online_ml_scoring.builder import GenericModel


class EmptyModel(GenericModel):
    pass


config_path = "../data/testconfig.conf"

loop = ConsumerTransformerProducerLoop(config_path)
loop.submit_model(EmptyModel())
loop.start()


