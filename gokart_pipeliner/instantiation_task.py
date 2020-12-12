import gokart


class InstantiationTask:
    @classmethod
    def run(cls, tasks, before_task=None) -> gokart.TaskOnKart:
        if isinstance(tasks, list):
            before_task = cls.instantiation_list_task(tasks, before_task)
        elif isinstance(tasks, dict):
            before_task = cls.instantiation_dict_task(tasks, before_task)
        else:
            before_task = cls.instantiation_task(tasks, before_task)

        return before_task

    @classmethod
    def instantiation_list_task(cls, task_list, before_task):
        for task in task_list:
            if isinstance(task, dict):
                before_task = cls.instantiation_dict_task(task, before_task)
            elif isinstance(task, list):
                before_task = cls.run(task, before_task)
            else:
                before_task = cls.instantiation_task(task, before_task)
        return before_task

    @classmethod
    def instantiation_dict_task(cls, task_dict, before_task):
        return {k: cls.run(v, before_task) for k, v in task_dict.items()}

    @staticmethod
    def instantiation_task(task, before_task):
        task_parameters = [
            var for var, object_name in vars(task).items()
            if isinstance(object_name, gokart.parameter.TaskInstanceParameter)
        ]

        if isinstance(before_task, dict):
            return task(**{t: before_task[t] for t in task_parameters})
        if before_task is None:
            return task()
        return task(**{task_parameters[0]: before_task})
