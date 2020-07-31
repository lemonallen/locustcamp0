import random
from locust import TaskSequence, HttpLocust, task, seq_task, between


class TestSuite(TaskSequence):
    """
    创建一个测试用例管理类，继承 带有顺序的类TaskSequence
    """

    def on_start(self):
        """
        初始化方法，相当于 __init__ 函数，或setup
        每次测试执行时，都会首先执行的  函数
        不需要 装饰器 定义
        :return:
        """
        pass

    def on_stop(self):
        """
        测试执行结束后，执行的方法， 相当于teardown
        不需要用  装饰器 定义
        :return:
        """
        pass


class RunCase(HttpLocust):
    """
    创建 压测类 继承 HttpLocust
    """
    task_set = TestSuite    # 指定测试套件    task_set 固定
    wait_time = between(0.1, 3) # 定义执行过程中随机等待时间区间，单位 秒
