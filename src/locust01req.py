import random
from locust import TaskSequence, HttpLocust, task, seq_task, between
import json

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

    @task  # 装饰器，说明下面是一个测试任务
    def regist_case(self):
        url = '/erp/regist'
        headers = {"Content-Type": "application/json"}
        user = "locust" + str(random.randint(100, 999))
        pwd = "1234567890"
        data = {"name": user, "pwd": pwd}
        # self.client 发起请求，相当于requests
        # catch_response 值为True 允许为失败 ， name 设置任务标签名称   -----可选参数
        rsp = self.client.post(url, data=json.dumps(data), headers=headers, catch_response=True, name='test_regist')
        if rsp.status_code == 200:
            rsp.success()
        else:
            rsp.failure("regist注册失败！")

    # def login_case(self):
    #     url = '/erp/login'
    #     headers = {"Content-Type": "application/json"}
    #     user = "locust" + str(random.randint(100, 999))
    #     pwd = "1234567890"
    #     data = {"name": user, "pwd": pwd}
    #     # self.client 发起请求，相当于requests
    #     # catch_response 值为True 允许为失败 ， name 设置任务标签名称   -----可选参数
    #     rsp = self.client.post(url, data=json.dumps(data), headers=headers, catch_response=True, name='test_regist')
    #     if rsp.status_code == 200:
    #         rsp.success()
    #     else:
    #         rsp.failure("regist注册失败！")

class RunCase(HttpLocust):
    """
    创建 压测类 继承 HttpLocust
    """
    # host = "http://127.17.0.1:8080"
    task_set = TestSuite  # 指定测试套件    task_set 固定
    wait_time = between(0.1, 3)  # 定义执行过程中随机等待时间区间，单位 秒
