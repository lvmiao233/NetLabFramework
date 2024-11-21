from dataclasses import dataclass, field
from typing import List, Optional
import concurrent.futures
from .test_status import Status
from .test_case import Case


@dataclass
class Test:
    """
    测试类，包含多个测试用例实例，支持并行执行用例测试
    """
    cases: List[Case] = field(default_factory=list)
    params: Optional[dict] = None
    timeout: Optional[float] = None  # 默认超时时间，单位：秒

    def add_case(self, case: Case) -> None:
        self.cases.append(case)

    def run_all_cases(self, parallel: bool = True) -> None:
        # 同步全局参数到每个用例
        if self.params:
            for case in self.cases:
                case.params = self.params
        if self.timeout:
            for case in self.cases:
                case.timeout = self.timeout
        if parallel:
            # 运行所有用例，并行执行各个用例
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(case.run) for case in self.cases]
                concurrent.futures.wait(futures)
        else:
            # 顺序运行所有用例
            for case in self.cases:
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
