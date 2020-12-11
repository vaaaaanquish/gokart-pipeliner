# gokart-pipeliner
gokart pipeline project


```python
from gokart_pipeliner import GokartPipeliner
from ExampleTasks import *

# make pipeline
preprocess = [TaskA, {'task_b': TaskB, 'task_c': TaskC}, TaskD]
modeling = [preprocess, TaskE, {'task_f': TaskF}, TaskF]
predict = [{'model': modeling, 'task_a': TaskA}, TaskG]

# instantiation (setting static params)
params = {'TaskA': {'param1':0.1, 'param2': 'sample'}, 'TaskD': {'param1': 'foo'}}
config_path_list = ['./conf/param.ini']
gp = GokartPipeliner(
    params=params,
    config_path_list=config_path_list)

# run (setting dynamic params)
running_params = {'TaskB': {'param1':'bar'}}
gp.run(predict, params=running_params)
```


```
pip install poetry
pip install poetry-dynamic-versioning

# poetry install
poetry build
# poetry lock
```
