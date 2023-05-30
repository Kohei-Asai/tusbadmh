from tusbadmh.enum import InputType, OvfSt, Status


class StatusResult:
    def __init__(self, status: Status, ovf_st: OvfSt) -> None:
        self.status = status
        self.ovf_st = ovf_st

    def __str__(self) -> str:
        return f"status: {self.status}, ovf_st: {self.ovf_st}"


class LengthResult:
    def __init__(self, len_1: int, len_2: int, rate_1: int, rate_2: int) -> None:
        self.len_1 = len_1
        self.len_2 = len_2
        self.rate_1 = rate_1
        self.rate_2 = rate_2

    def __str__(self) -> str:
        return f"len_1: {self.len_1}, len_2: {self.len_2}, rate_1: {self.rate_1}%, rate_2: {self.rate_2}%"


class CheckInputTypeResult:
    def __init__(self, type_1: InputType, type_2: InputType) -> None:
        self.type_1 = type_1
        self.type_2 = type_2

    def __str__(self) -> str:
        return f"type_1: {self.type_1}, type_2: {self.type_2}"


class DataResult:
    def __init__(self, data: list[int], leng: int) -> None:
        self.data = data
        self.leng = leng

    def __str__(self) -> str:
        return f"data: {self.data}, leng: {self.leng}"
