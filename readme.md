# NetLabFramework

浙江大学2024-2025学年秋冬学期 计算机网络 编程实验测试框架

> [!NOTE]
> 
> 请注意，本框架用于辅助测试Lab7-8实现的正确性，不是编程实验的基础代码框架
> 
> 请按照实验要求，完成Lab7-8的代码编写

框架目前仍在调试改进中，测试中遇到问题欢迎提交issue/钉钉反馈，谢谢！

## 运行

### 在线测试框架

```bash
python online_test.py
```

### 本地测试框架

#### Lab7 测试
    
  测试需要指定Socket服务端地址`host`、端口`port`、测试线程数

  ```bash
  # 测试 1
  python local_test.py --lab 7 --test 1 --host 127.0.0.1 --port 6054
  # 测试 3
  python local_test.py --lab 7 --test 3 --host 127.0.0.1 --port 6054 --threads 20
  ```

#### Lab8 测试
    
  测试需要指定Web服务端地址`host`、端口`port`
  ```bash
  # 测试 2
  python local_test.py --lab 8 --test 2 --host 127.0.0.1 --port 6052
  # 测试 3
  python local_test.py --lab 8 --test 3 --host 127.0.0.1 --port 6053
  # 测试 4
  python local_test.py --lab 8 --test 4 --host 127.0.0.1 --port 6054
  # 测试 5
  python local_test.py --lab 8 --test 5 --host 127.0.0.1 --port 6055
  ```

### Q & A

* 我的电脑上，测试时无论如何都会超时，该如何解决？
  * 如果你的电脑性能受限，导致计算速度过慢，请尝试增加`utils/socket_client.py`、`data_model/test_case.py`中超时时间，观察是否解决
  * 如果不存在性能问题，请检查代码实现是否存在问题