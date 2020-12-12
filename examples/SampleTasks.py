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

    def run(self):
        x = self.load('foo')
        self.dump(x + ['C'])


class TaskD(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()
    bar = gokart.TaskInstanceParameter()

    def run(self):
        x = self.load('foo')
        y = self.load('bar')
        self.dump(x + y + ['D'])


if __name__ == '__main__':
    gp = GokartPipeliner()
    a = [TaskA]
    b = [a, {'foo': TaskB}, TaskC]
    gp.run([{'foo': a, 'bar': b}, TaskD])
