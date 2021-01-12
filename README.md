# gokart-pipeliner
gokart pipeline project


# Usage

Please show [SampleTask.py](https://github.com/vaaaaanquish/gokart-pipeliner/blob/main/examples/SampleTasks.py) or [Eaxmple.ipynb](https://github.com/vaaaaanquish/gokart-pipeliner/blob/main/examples/Example.ipynb)

```python
from gokart_pipeliner import GokartPipeliner
from ExampleTasks import *

# make pipeline
preprocess = [TaskA, {'task_b': TaskB, 'task_c': TaskC}, TaskD]
modeling = preprocess + [TaskE, {'task_f': TaskF}, TaskF]
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

task example
```python
class Task(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()

    def run(self):
        x = self.load('foo')
        self.dump(x)
```

## get task result

We can get result of latest pipeline tasks.
```python
task_b_result = gp.run([TaskA, TaskB], return_value=True)
```


## write requires

If you say "want to write requires" or "want to reuse existing tasks", we can use `override_requires` parameter.
```python
params = {'ExistingTask': {'override_requires': False}}
gp.run([ExistingTask], params=params)
```

## for jupyter notebook

### off logger
```python
gp.run([Task], params=params, verbose=False)
```

# Develop

```
pip install poetry
pip install poetry-dynamic-versioning

# poetry install
poetry build
# poetry lock
```
