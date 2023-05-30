from typing import Tuple
import time
import csv
import math
import pkg_resources

from tusbadmh.error import Error
from tusbadmh.tusbadmh import TUSBADMH
from tusbadmh.enum import (
    Ch,
    ClkSel,
    InputType,
    Mode,
    OvfSt,
    Status,
    TrgSel,
)
from tusbadmh.result_class import (
    StatusResult,
    LengthResult,
    CheckInputTypeResult,
    DataResult,
)


def __get_mock_data_from_csv() -> list[int]:
    csv_path = pkg_resources.resource_filename("tusbadmh", "mock_data.csv")
    f = open(csv_path, "r")
    reader = csv.reader(f)
    data = [e for e in reader]
    f.close()
    return [int(e) for e in data[0]]


mock_data = __get_mock_data_from_csv()


# NOTE: ソフトウェアトリガの場合のみを想定している
# TODO: より柔軟なmockの実装
class TUSBADMHMockImpl(TUSBADMH):
    def __init__(self) -> None:
        self.idx_1 = 0
        self.idx_2 = 50000
        self.cyc_len = 0
        self.pre_len = 0
        self.trg_sel = TrgSel.SOFTWARE
        self.mode = Mode.REPEAT
        self.ch1_only = True
        self.data_1: list[int] = []
        self.data_2: list[int] = []
        self.input_type_1 = InputType.BIPOLAR
        self.input_type_2 = InputType.BIPOLAR
        self.status = Status.STOP
        self.clk_sel = ClkSel.IN_200MHz
        self.div = 0

    def device_open(self, id: int) -> Error:
        _ = id
        return Error(0)

    def device_close(self, id: int) -> None:
        _ = id

    def dio_read(self, id: int, data: int) -> Error:
        _ = id
        _ = data
        return Error(0)

    def dio_write(self, id: int, data: int) -> Error:
        _ = id
        _ = data
        return Error(0)

    def adc_start(
        self,
        id: int,
        cyc_len: int,
        pre_len: int,
        trg_sel: TrgSel,
        mode: Mode,
        ch1_only: bool,
    ) -> Error:
        _ = id
        self.cyc_len = cyc_len
        self.pre_len = pre_len
        self.trg_sel = trg_sel
        self.mode = mode
        self.ch1_only = ch1_only
        self.status = Status.WAITING
        return Error(0)

    def adc_stop(self, id: int) -> Error:
        _ = id
        self.status = Status.STOP
        return Error(0)

    def status_get(self, id: int) -> Tuple[StatusResult, Error]:
        _ = id
        return StatusResult(status=self.status, ovf_st=OvfSt.OK), Error(0)

    def length(self, id: int) -> Tuple[LengthResult, Error]:
        _ = id
        max = 1048576
        len_1 = len(self.data_1)
        len_2 = len(self.data_2)
        rate_1 = int(math.floor(len_1 * 100 / max))
        rate_2 = int(math.floor(len_2 * 100 / max))
        return (
            LengthResult(
                len_1=len_1,
                len_2=len_2,
                rate_1=rate_1,
                rate_2=rate_2,
            ),
            Error(0),
        )

    def data_get(self, id: int, ch: Ch, leng: int) -> Tuple[DataResult, Error]:
        _ = id
        if ch == Ch.CHANNEL_1:
            if leng < len(self.data_1):
                res = self.data_1[0:leng]
                self.data_1 = self.data_1[leng:]
            else:
                res = self.data_1
                self.data_1 = []
        else:
            if leng < len(self.data_2):
                res = self.data_2[0:leng]
                self.data_2 = self.data_2[leng:]
            else:
                res = self.data_2
                self.data_2 = []
        return DataResult(data=res, leng=len(res)), Error(0)

    def clock_select(self, id: int, clk_sel: ClkSel, div: int, ave: int) -> Error:
        _ = id
        self.clk_sel = clk_sel
        self.div = div
        _ = ave
        return Error(0)

    def thlevel_set(self, id: int, th_level: int, n_level: int) -> Error:
        _ = id
        _ = th_level
        _ = n_level
        return Error(0)

    def input_type(self, id: int, type_1: InputType, type_2: InputType) -> Error:
        _ = id
        self.input_type_1 = type_1
        self.input_type_2 = type_2
        return Error(0)

    def check_input_type(self, id: int) -> Tuple[CheckInputTypeResult, Error]:
        _ = id
        return (
            CheckInputTypeResult(type_1=self.input_type_1, type_2=self.input_type_2),
            Error(0),
        )

    def trigger(self, id: int) -> Error:
        _ = id
        self.status = Status.CONVERTING
        freq = self.clk_sel.freq() / (self.div + 1)
        dt = 1 / freq
        for _ in range(self.cyc_len):
            self.data_1.append(mock_data[self.idx_1])
            self.idx_1 = self.idx_1 + 1 if self.idx_1 < len(mock_data) - 1 else 0
            if not self.ch1_only:
                self.data_2.append(mock_data[self.idx_2])
                self.idx_2 = self.idx_2 + 1 if self.idx_2 < len(mock_data) - 1 else 0
            time.sleep(dt)
        return Error(0)

    def translimit(self, id: int, limit: int) -> Error:
        _ = id
        _ = limit
        return Error(0)
