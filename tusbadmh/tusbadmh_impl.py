from ctypes import (
    cdll,
    c_short,
    c_int,
    c_ubyte,
    byref,
)
import os
from typing import Tuple
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


class TUSBADMHImpl(TUSBADMH):
    def __init__(self, archtecture: str):
        if archtecture == "x86":
            driver_path = os.path.join(
                os.path.dirname(__file__), "./DRIVER/x86/TUSBADMH.dll"
            )
            self.dll = cdll.LoadLibrary(driver_path)
        elif archtecture == "amd64":
            driver_path = os.path.join(
                os.path.dirname(__file__), "./DRIVER/amd64/TUSBADMH.dll"
            )
            self.dll = cdll.LoadLibrary(driver_path)
        else:
            raise ValueError("archtecture must be x86 or amd64")

    def device_open(self, id: int) -> Error:
        err_code = self.dll.Tusbadmh_Device_Open(c_short(id))
        return Error(int(err_code))

    def device_close(self, id: int) -> None:
        self.dll.Tusbadmh_Device_Close(c_short(id))

    def dio_read(self, id: int, data: int) -> Error:
        err_code = self.dll.Tusbadmh_Dio_Read(c_short(id), c_ubyte(data))
        return Error(int(err_code))

    def dio_write(self, id: int, data: int) -> Error:
        err_code = self.dll.Tusbadmh_Dio_Write(c_short(id), c_ubyte(data))
        return Error(int(err_code))

    def adc_start(
        self,
        id: int,
        cyc_len: int,
        pre_len: int,
        trg_sel: TrgSel,
        mode: Mode,
        ch1_only: bool,
    ) -> Error:
        err_code = self.dll.Tusbadmh_Adc_Start(
            c_short(id),
            c_int(cyc_len),
            c_int(pre_len),
            c_ubyte(trg_sel.value),
            c_ubyte(mode.value),
            c_ubyte(int(ch1_only)),
        )
        return Error(int(err_code))

    def adc_stop(self, id: int) -> Error:
        err_code = self.dll.Tusbadmh_Adc_Stop(c_short(id))
        return Error(int(err_code))

    def status_get(self, id: int) -> Tuple[StatusResult, Error]:
        ret_status = c_ubyte()
        ret_ovf_st = c_ubyte()
        err_code = self.dll.Tusbadmh_Status_Get(
            c_short(id), byref(ret_status), byref(ret_ovf_st)
        )
        return (
            StatusResult(
                status=Status(ret_status.value),
                ovf_st=OvfSt(ret_ovf_st.value),
            ),
            Error(int(err_code)),
        )

    def length(self, id: int) -> Tuple[LengthResult, Error]:
        ret_len_1 = c_int()
        ret_len_2 = c_int()
        ret_rate_1 = c_int()
        ret_rate_2 = c_int()
        err_code = self.dll.Tusbadmh_Length(
            c_short(id),
            byref(ret_len_1),
            byref(ret_len_2),
            byref(ret_rate_1),
            byref(ret_rate_2),
        )
        return (
            LengthResult(
                len_1=ret_len_1.value,
                len_2=ret_len_2.value,
                rate_1=ret_rate_1.value,
                rate_2=ret_rate_2.value,
            ),
            Error(int(err_code)),
        )

    def data_get(self, id: int, ch: Ch, leng: int) -> Tuple[DataResult, Error]:
        ret_data = (c_int * leng)()
        ret_leng = c_int(leng)
        err_code = self.dll.Tusbadmh_Data_Get(
            c_short(id), c_ubyte(ch.value), ret_data, byref(ret_leng)
        )
        return (
            DataResult(data=list(ret_data[: ret_leng.value]), leng=ret_leng.value),
            Error(int(err_code)),
        )

    def clock_select(self, id: int, clk_sel: ClkSel, div: int, ave: int) -> Error:
        err_code = self.dll.Tusbadmh_Clock_Select(
            c_short(id), c_ubyte(clk_sel.value), c_ubyte(div), c_ubyte(ave)
        )
        return Error(int(err_code))

    def thlevel_set(self, id: int, th_level: int, n_level: int) -> Error:
        err_code = self.dll.Tusbadmh_ThLevel_Set(
            c_short(id), c_int(th_level), c_int(n_level)
        )
        return Error(int(err_code))

    def input_type(self, id: int, type_1: InputType, type_2: InputType) -> Error:
        err_code = self.dll.Tusbadmh_InputType(
            c_short(id), c_ubyte(type_1.value), c_ubyte(type_2.value)
        )
        return Error(int(err_code))

    def check_input_type(self, id: int) -> Tuple[CheckInputTypeResult, Error]:
        ret_type_1 = c_ubyte()
        ret_type_2 = c_ubyte()
        err_code = self.dll.Tusbadmh_CheckInputType(
            c_short(id), byref(ret_type_1), byref(ret_type_2)
        )
        return (
            CheckInputTypeResult(
                type_1=InputType(ret_type_1.value), type_2=InputType(ret_type_2.value)
            ),
            Error(int(err_code)),
        )

    def trigger(self, id: int) -> Error:
        err_code = self.dll.Tusbadmh_Trigger(c_short(id))
        return Error(int(err_code))

    def translimit(self, id: int, limit: int) -> Error:
        err_code = self.dll.Tusbadmh_TransLimit(c_short(id), c_int(limit))
        return Error(int(err_code))
