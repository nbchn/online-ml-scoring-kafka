# Generic Online ML scoring for Kafka

## Usage: 

```
from generic_online_ml_scoring.builder import Builder
builder = Builder(config_path, model, preprocessing, postprocessing)
builder.start()
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
    Python object that implements a '.predict(pd.Dataframe)' method.
preprocessing:
    Function executed before applying prediction function. 
    Takes raw data from topic as input and should return a pd.Dataframe.
postprocessing:
    Function executed after applying prediction function. 
    Takes output of prediction function as input and should return proper object to be published to out.topic.
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
from generic_online_ml_scoring.builder import Builder
import pandas as pd
import pickle

def preprocessing(json):
    return pd.DataFrame(data=json, index=[0])


def postprocessing(df):
    return df.to_dict('records')[0]

fh = open(data/model1.pkl, 'rb')
model1 = pickle.load(fh)

builder = Builder(
    'data/model1.conf', 
    model1, 
    preproc_func, 
    postproc_func
)

builder.start()

```

## Install:
```
pip install requirements.txt
python setup.py bdist_egg
easy_install dist/generic_online_ml_scoring_for_kafka-0.0.1-py[...].egg
```