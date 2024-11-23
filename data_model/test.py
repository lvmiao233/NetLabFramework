from dataclasses import dataclass, field
from typing import List, Optional
import concurrent.futures
from .test_status import Status
from .test_case import Case
import tabulate
from termcolor import colored

@dataclass
class Test:
    """
    测试类，包含多个测试用例实例，支持并行执行用例测试
    """
    cases: List[Case] = field(default_factory=list)
    params: Optional[dict] = None
    timeout: Optional[float] = None  # 默认超时时间，单位：秒
    duplicate: int = 1

    def add_case(self, case: Case) -> None:
        self.cases.append(case)

    def run_all_cases(self, parallel: bool = True) -> None:
        # 同步全局参数到每个用例，以 case 内的 params 为准
        if self.params:
            for case in self.cases:
                new_params = self.params.copy()
                if case.params:
                    new_params.update(case.params)
                case.params = new_params
        if self.timeout:
            for case in self.cases:
                case.timeout = self.timeout
        if parallel:
            # 运行所有用例，并行执行各个用例
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(self.duplicate):
                    futures = [executor.submit(case.run) for case in self.cases]
                    concurrent.futures.wait(futures)
        else:
            # 顺序运行所有用例
            for case in self.cases:
                for i in range(self.duplicate):
                    case.run()

    def to_dict(self) -> dict:
        return {
            "success_cnt": sum(1 for case in self.cases if case.status == Status.AC),
            "timeout_cnt": sum(1 for case in self.cases if case.status == Status.TLE),
            "error_cnt": sum(1 for case in self.cases if case.status == Status.RE),
            "total_cnt": len(self.cases),
            "cases": [
                {
                    "index": case.index,
                    "name": case.name,
                    "status": case.status.value,
                    "time": case.time
                } for case in self.cases
            ]
        }

    def print_results(self):
        status_colors = {
            Status.AC: "green",
            Status.RE: "red",
            Status.TLE: "yellow",
            Status.WA: "red"
        }
        status_desc = {
            Status.AC: "Pass",
            Status.RE: "Runtime Error",
            Status.TLE: "Time Limit Exceeded",
            Status.WA: "Wrong Response"
        }
        headers = ["Index", "Name", "Status", "Time (ms)"]
        data = []
        for case in self.cases:
            if case.time is None:
                time_str = "N/A"
            else:
                time_ms = case.time * 1000
                if time_ms >= 1000:
                    time_str = f"{int(time_ms)} ms"
                elif time_ms >= 100:
                    time_str = f"{time_ms:.1f} ms"
                elif time_ms >= 10:
                    time_str = f"{time_ms:.2f} ms"
                else:
                    time_str = f"{time_ms:.3f} ms"
            name = case.name if case.name is not None else ""
            status_color = status_colors.get(case.status, "white")
            status_str = colored(status_desc[case.status], status_color)
            data.append([case.index, name, status_str, time_str])
        table = tabulate.tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
