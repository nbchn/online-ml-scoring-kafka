from .utils import load_properties
from confluent_kafka import Consumer
from confluent_kafka import Producer
import json
import sys


class ConfigException(Exception):
    pass


class GenericModel:

    def __init__(self):
        pass

    def execute(self, data):
        yield data


class ConsumerTransformerProducerLoop:

    def __init__(self, config_path):
        """
        :param config_path: path for config file containing consumer producer config and internal config
        """

        self._consumer_config, self._producer_config, self.builder_config = load_properties(config_path)

        if all(prop in self.builder_config for prop in ("topic.in", "topic.out")):
            self._inTopic = self.builder_config["topic.in"]
            self._outTopic = self.builder_config["topic.out"]
        else:
            print("Cannot create builder : topic.in / topic.out are mandatory properties", file=sys.stderr)
            raise ConfigException

        self._consumer = Consumer(self._consumer_config)
        self._producer = Producer(self._producer_config)
        self._consumer.subscribe([self._inTopic])

        self._model = None

    def submit_model(self, model):
        if issubclass(model, GenericModel):
            self._model = model
        else:
            print("Model should inherit from GenericModel", file=sys.stderr)
            raise ConfigException

    def start(self):

        print("Producer consumer loop started...")

        if self._model is None:
            print("You should submit a model before starting the consumer/producer loop", file=sys.stderr)
            raise ConfigException

        while True:
            try:
                msg = self._consumer.poll(1.0)

                if msg.error() or msg is None:
                    print(f"Consumer error : {msg.value()}")
                    continue

                # Get raw key/value
                # we assume key is kept unchanged
                key = msg.key()
                value = json.loads(msg.value())

                # Execute model and produce output to out.topic
                for model_output in self._model.execute(value):
                    self._producer.produce(self._outTopic, key, json.dumps(model_output))

            except KeyboardInterrupt:
                break

            finally:
                self._consumer.close()
                self._producer.flush()
