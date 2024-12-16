from dataclasses import dataclass
from typing import Optional, Callable
import time as timer
import threading, traceback

from .test_status import Status


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
    timeout: float = 1  # 默认超时时间，单位：秒
    duplicate: int = 0

    def run(self) -> None:
        if self.run_function:
            if self.status != Status.AC and self.duplicate > 0:
                return
            thread = threading.Thread(target=self._run_function)
            start_time = timer.time()
            thread.start()
            thread.join(timeout=self.timeout)
            elapsed_time = timer.time() - start_time
            if thread.is_alive():
                self.status = Status.TLE
            else:
                self.duplicate += 1
                self.time = 0 if self.time is None else self.time
                self.time = (self.time * (self.duplicate - 1) + elapsed_time) / self.duplicate

    def _run_function(self) -> None:
        try:
            if self.params:
                self.status = self.run_function(**self.params)
            else:
                self.status = self.run_function()
        except Exception as e:
            self.status = Status.RE
            if self.name is not None and self.name != "":
                print(self.name)
            print(f" Exception occurred:\n{traceback.format_exc()}")

    def update_status(self, status: Status, run_time: Optional[float] = None) -> None:
        self.status = status
        if run_time is not None:
            self.time = run_time
