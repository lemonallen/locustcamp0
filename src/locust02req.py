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
        self.headers = {"Content-Type": "application/json"}
        self.user = "locust" + str(random.randint(100, 999))
        self.pwd = "1234567890"

    def on_stop(self):
        """
        测试执行结束后，执行的方法， 相当于teardown
        不需要用  装饰器 定义
        :return:
        """
        pass

    @task  # 装饰器，说明下面是一个测试任务
    @seq_task(1)  # 装饰器 说明任务的执行顺序
    def regist_case(self):
        url = '/erp/regist'
        data = {"name": self.user, "pwd": self.pwd, "age": self.user[-2:]}
        # self.client 发起请求，相当于requests
        # catch_response 值为True 允许为失败 ， name 设置任务标签名称   -----可选参数
        rsp = self.client.post(url, json=data, headers=self.headers, catch_response=True, name='test_0')
        # 进行结果断言
        if rsp.status_code == 200:
            rsp.success()
        else:
            rsp.failure("regist注册失败！")
        # 结果断言的方式还可以： rsp.ok 返回True则说明响应状态小于400

    @task
    @seq_task(2)
    def login_case(self):
        url = '/erp/loginIn'
        data = {"name": self.user, "pwd": self.pwd}
        rsp = self.client.post(url, json=data, headers=self.headers, catch_response=True, name='test_1')
        self.token = rsp.json()['token']  # 提取响应信息中的 token
        print(self.token)
        if rsp.status_code == 200:
            rsp.success()
        else:
            rsp.failure("login登录失败")

    @task
    @seq_task(3)
    def getuser_case(self):
        url = '/erp/user'
        headers = {"Token": self.token}
        rsp = self.client.get(url, headers=headers, catch_response=True, name='test_2')
        if rsp.status_code == 200:
            rsp.success()
        else:
            rsp.failure("getuser获取用户失败")


class RunCase(HttpLocust):
    """
    创建 压测类 继承 HttpLocust
    """
    task_set = TestSuite  # 指定测试套件    task_set 固定
    wait_time = between(0, 1)  # 定义执行过程中随机等待时间区间，单位 秒
