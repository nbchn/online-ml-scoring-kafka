# Generic Online ML scoring for Kafka

## Usage: 

```
from generic_online_ml_scoring.builder import ConsumerTransformerProducerLoop

loop = ConsumerTransformerProducerLoop(config_path)
loop.submit_model(model)
loop.start()
```

### Parameters

```
config_path: 
    Path for config file. 
    Kafka-consumer properties should be prefixed by 'consumer.'.
    Kafka-producer properties should be prefixed by 'producer.'.
    Properties for both consumer and producer can be prefixed by 'all.'.
    Internal mandatory properties:
        - in.topic
        - out.topic
model:
    Instance of class that inherits from GenericModel. GenericModel has two methods: 
        - Contructor 
        - Execute function that takes raw data as input and returns an iterator over results.
```

## Example: 

Config file:
```
all.bootstrap.servers=host1:9092,host2:9092
consumer.auto.offset.reset=earliest
consumer.group.id=model1-consumer-group
producer.client.id=model1-output
in.topic=input-topic
out.topic=output-topic
```

Code:
```
from generic_online_ml_scoring.builder import ConsumerTransformerProducerLoop
from generic_online_ml_scoring.builder import GenericModel
import math


class SquareAllIntPropsModel(GenericModel):
    def __init__(self):
        print("Initialization of the model")

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

```

## Install:
```
pip install requirements.txt
python setup.py bdist_egg
easy_install dist/generic_online_ml_scoring_for_kafka-0.0.1-py[...].egg
```