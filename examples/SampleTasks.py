import luigi
import gokart

from gokart_pipeliner import GokartPipeliner


class TaskA(gokart.TaskOnKart):
    def run(self):
        self.dump(['a'])


class TaskB(gokart.TaskOnKart):
    target = gokart.TaskInstanceParameter()

    def run(self):
        x = self.load('target')
        self.dump(x + ['b'])


class TaskC(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()
    text = luigi.Parameter()

    def run(self):
        x = self.load('foo')
        self.dump(x + [self.text])


class TaskD(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()
    bar = gokart.TaskInstanceParameter()

    def run(self):
        x = self.load('foo')
        y = self.load('bar')
        self.dump(x + y + ['D'])


if __name__ == '__main__':
    a = [TaskA]
    b = [a, {'foo': TaskB}, TaskC]

    params = {'TaskC': {'text': 'c'}}

    gp = GokartPipeliner()
    gp.print_dependence_tree([{'foo': a, 'bar': b}, TaskD], params=params)
    gp.run([{'foo': a, 'bar': b}, TaskD], params=params)
