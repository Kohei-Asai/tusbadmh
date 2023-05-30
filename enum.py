from enum import Enum


class TrgSel(Enum):
    EXTERNAL = 0
    UP_EDGE = 1
    DOWN_EDGE = 2
    SOFTWARE = 3


class Mode(Enum):
    CONTINUATION = 0
    REPEAT = 1

    def label(self) -> str:
        if self == Mode.CONTINUATION:
            return "continuation"
        else:
            return "repeat for each trigger"


class Ch(Enum):
    CHANNEL_1 = 0
    CHANNEL_2 = 1


class ClkSel(Enum):
    IN_200MHz = 0
    IN_20p48MHz = 1
    IN_16p384MHz = 2
    IN_12p8MHz = 3
    IN_1p92MHz = 4
    EX = 5

    def freq(self) -> float:
        if self == ClkSel.IN_200MHz:
            return 200e6
        elif self == ClkSel.IN_20p48MHz:
            return 20.48e6
        elif self == ClkSel.IN_16p384MHz:
            return 16.384e6
        elif self == ClkSel.IN_12p8MHz:
            return 12.8e6
        elif self == ClkSel.IN_1p92MHz:
            return 1.92e6
        else:
            return 1  # EXはどうせ使わないので適当に設定（0でなければよい）

    def label(self) -> str:
        if self == ClkSel.IN_200MHz:
            return "200MHz"
        elif self == ClkSel.IN_20p48MHz:
            return "20.48MHz"
        elif self == ClkSel.IN_16p384MHz:
            return "16.384MHz"
        elif self == ClkSel.IN_12p8MHz:
            return "12.8MHz"
        elif self == ClkSel.IN_1p92MHz:
            return "1.92MHz"
        else:
            return "外部トリガ（未対応）"


class InputType(Enum):
    BIPOLAR = 0
    UNIPOLAR = 1

    def label(self) -> str:
        if self == InputType.BIPOLAR:
            return "bipolar(-1V~1V)"
        else:
            return "unipolar(0V~2V)"


class Status(Enum):
    STOP = 0
    WAITING = 1
    CONVERTING = 2


class OvfSt(Enum):
    OK = 0
    OVERFLOW_CH1 = 1
    OVERFLOW_CH2 = 2
    OVERFLOW_CH1_CH2 = 3
