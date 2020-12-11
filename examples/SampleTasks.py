import gokart
from gokart_pipeliner import GokartPipeliner


class TaskA(gokart.TaskOnKart):
    def run(self):
        self.dump(['a'])


class TaskB(gokart.TaskOnKart):
    target = gokart.TaskInstanceParameter()

    def requires(self):
        return self.target

    def run(self):
        x = self.load()
        self.dump(x + ['b'])


class TaskC(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()

    def requires(self):
        return self.foo

    def run(self):
        x = self.load()
        self.dump(x + ['C'])


class TaskD(gokart.TaskOnKart):
    foo = gokart.TaskInstanceParameter()
    bar = gokart.TaskInstanceParameter()

    def requires(self):
        return {'foo': self.foo, 'bar': self.bar}

    def run(self):
        x = self.load('foo')
        y = self.load('bar')
        self.dump(x + y + ['D'])


if __name__ == '__main__':
    gp = GokartPipeliner()
    a = [TaskA]
    b = [a, {'foo': TaskB}, TaskC]
    gp.run([{'foo': a, 'bar': b}, TaskD])
