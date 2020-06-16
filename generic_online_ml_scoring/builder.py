from .utils import load_properties
from confluent_kafka import Consumer
from confluent_kafka import Producer
import json


class ConfigException(Exception):
    pass


class Builder:

    def __init__(self, config_path, model, preproc_func, postproc_func):
        """
        :param config: path for config file containing consumer producer config and internal config
        :param model: generic object having a .predict(df=pd.Dataframe) function
        :param preproc_func: function to call on incoming object for preprocessing
        :param postproc_func: function to call on outcoming object for postprocessing
        """

        self._model = model
        self._consumer_config, self._producer_config, self.builder_config = load_properties(config_path)

        if callable(preproc_func) and callable(postproc_func):
            self._preproc_func = preproc_func
            self._posproc_func = postproc_func
        else:
            print("Cannot create builder : preprocessing / postprocessing should be functions")
            raise ConfigException

        if all(prop in self.builder_config for prop in ("topic.in", "topic.out")):
            self._inTopic = self.builder_config["topic.in"]
            self._outTopic = self.builder_config["topic.out"]
        else:
            print("Cannot create builder : topic.in / topic.out are mandatory properties")
            raise ConfigException

        self._consumer = Consumer(self._consumer_config)
        self._producer = Producer(self._producer_config)
        self._consumer.subscribe([self._inTopic])
        self._running = False

    def start(self):

        print("Producer consumer loop started...")
        self._running = True

        # TODO : for now lets assume input is JSON

        while self._running:
            try:
                msg = self._consumer.poll(1.0)

                if msg.error() or msg is None:
                    print(f"Consumer error : {msg.value()}")
                    continue

                # 1. get raw key/value
                # we assume key is kept unchanged
                key = msg.key()
                value = json.loads(msg.value())

                # 2. apply preprocessing function
                # this should return a pd.Dataframe
                if self._preproc_func:
                    value = self._preproc_func(value)

                # 3. apply model prediction
                value_predicted = self._model.predict(value)

                # 4. apply postprocessing function
                if self._posproc_func:
                    value_predicted = self._posproc_func(value_predicted)

                # 5. merge original value with predicted value
                data_out = value
                data_out["output"] = value_predicted

                # 6. produce output in out.topic
                self._producer.produce(self._outTopic, key, json.dumps(data_out))

            finally:
                self._consumer.close()
                self._producer.flush()

    def stop(self):
        self._running = False
