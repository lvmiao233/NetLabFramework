from dataclasses import dataclass
from typing import Optional, Callable
import time
import threading
from test_status import Status


@dataclass
class Case:
    """
    用例类，包含用例的基本信息、调用参数、测试函数。
    """
    index: int
    status: Status = Status.WA
    time: Optional[float] = None
    name: Optional[str] = None
    run_function: Optional[Callable[..., Status]] = None
    params: Optional[dict] = None
    timeout: float = 5.0  # 默认超时时间，单位：秒

    def run(self) -> None:
        if self.run_function:
            start_time = time.time()
            thread = threading.Thread(target=self._run_function)
            thread.start()
            thread.join(timeout=self.timeout)
            if thread.is_alive():
                self.status = Status.TLE
            self.time = time.time() - start_time

    def _run_function(self) -> None:
        try:
            if self.params:
                self.status = self.run_function(**self.params)
            else:
                self.status = self.run_function()
        except Exception as e:
            self.status = Status.RE

    def update_status(self, status: Status, time: Optional[float] = None) -> None:
        self.status = status
        if time is not None:
            self.time = time
