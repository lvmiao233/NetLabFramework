# NetLabFramework

浙江大学2024-2025学年秋冬学期 计算机网络 编程实验测试框架

> [!NOTE]
> 
> 请注意，本框架用于测试Lab7-8实现的正确性，不是编程实验的基础代码框架
> 
> 请按照实验要求，完成Lab7-8的代码编写

框架目前仍处于开发状态，可能无法确保测试的正确性，测试中遇到问题请提交issue/钉钉反馈，谢谢！

## 运行

* 在线测试框架

```bash
python online_test.py
```

* 本地测试框架

  * Lab7 测试
    
    测试需要指定Socket服务端地址`host`、端口`port`、测试线程数

    ```bash
    # 测试 1
    python local_test.py --lab 7 --test 1 --host 127.0.0.1 --port 6054
    # 测试 3
    python local_test.py --lab 7 --test 3 --host 127.0.0.1 --port 6054 --threads 20
    ```