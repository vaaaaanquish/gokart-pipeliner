# gokart-pipeliner
gokart pipeline project


```python
import gokart_pipliner

# make pipeline
preprocess = [TaskA, {'task_b': TaskB, 'task_c': TaskC}, TaskD]
modeling = [preprocess, TaskE, {'task_f': TaskF}, TaskF]
predict = [{'model': modeling, 'task_a': TaskA}, TaskG]

# setting params
params = {'TaskA': {'param1':0.1, 'param2': 'sample'}, 'TaskD': {'param1': 'foo'}}
gokart_pipliner.add_config_path('./conf/param.ini')

# run
gokart_pipliner.run(predict, params=params)
```
