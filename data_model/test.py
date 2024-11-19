from dataclasses import dataclass, field
from typing import List, Optional
import concurrent.futures
from test_status import Status
from test_case import Case


@dataclass
class Test:
    """
    测试类，包含多个测试用例实例，支持并行执行用例测试
    """
    cases: List[Case] = field(default_factory=list)
    params: Optional[dict] = None

    def add_case(self, case: Case) -> None:
        if self.params:
            case.params = self.params
        self.cases.append(case)

    def run_all_cases(self, parallel: bool = True) -> None:
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
            "success_count": sum(1 for case in self.cases if case.status == Status.AC),
            "total_count": len(self.cases),
            "cases": [
                {
                    "index": case.index,
                    "name": case.name,
                    "status": case.status.value,
                    "time": case.time
                } for case in self.cases
            ]
        }
