import gokart


class InstantiationTask:
    @classmethod
    def run(cls, tasks, before_task=None, params=dict()) -> gokart.TaskOnKart:
        if isinstance(tasks, list):
            before_task = cls.instantiation_list_task(tasks, before_task,
                                                      params)
        elif isinstance(tasks, dict):
            before_task = cls.instantiation_dict_task(tasks, before_task,
                                                      params)
        else:
            before_task = cls.instantiation_task(tasks, before_task, params)

        return before_task

    @classmethod
    def instantiation_list_task(cls, task_list, before_task, params=dict()):
        for task in task_list:
            if isinstance(task, dict):
                before_task = cls.instantiation_dict_task(
                    task, before_task, params)
            elif isinstance(task, list):
                before_task = cls.run(task, before_task, params)
            else:
                before_task = cls.instantiation_task(task, before_task, params)
        return before_task

    @classmethod
    def instantiation_dict_task(cls, task_dict, before_task, params=dict()):
        return {
            k: cls.run(v, before_task, params)
            for k, v in task_dict.items()
        }

    @classmethod
    def instantiation_task(cls, task, before_task, params=dict()):
        task_parameters = [
            var for var, object_name in vars(task).items()
            if isinstance(object_name, gokart.parameter.TaskInstanceParameter)
        ]

        specification_params = params.get(task.__name__, {})
        if specification_params.pop('override_requires', True):
            task = cls.override_requires(task, task_parameters)

        if isinstance(before_task, dict):
            return task(**specification_params,
                        **{t: before_task[t]
                           for t in task_parameters})
        if before_task is None:
            return task(**specification_params)
        return task(**specification_params,
                    **{task_parameters[0]: before_task})

    @staticmethod
    def override_requires(task, task_parameters):
        """
        class Task(gokart.TaskOnKart):
            foo = gokart.TaskInstanceParameter()
            bar = gokart.TaskInstanceParameter()

            def requires(self):
                return {'foo': self.foo, 'bar': self.bar}
        """
        def requires(cls):
            return {t: getattr(cls, t) for t in task_parameters}

        def _get_input_targets(cls, target):
            """For task name may not be specified."""
            if target is None:
                return cls.input()[list(cls.input().keys())[0]]
            if isinstance(target, str):
                return cls.input()[target]
            return target

        task.requires = requires
        task._get_input_targets = _get_input_targets
        return task
