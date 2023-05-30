err: dict[int, str] = {
    0: "正常終了しました",
    1: "ID番号が不正です",
    2: "ドライバがインストールされていません",
    3: "すでにデバイスはオープンされています",
    4: "接続されている台数が多すぎます",
    5: "オープンできませんでした",
    6: "デバイスがみつかりません",
    7: "オープンされていません",
    8: "パラメータエラー",
    9: "USB通信エラーです",
    10: "メモリ領域が確保できません",
    11: "連続取込動作中です",
    12: "連続取り込みデータはありません",
    13: "開始されていません",
    14: "メモリオーバーフロー",
    15: "データ並びエラー",
    99: "不明なエラーです",
}


class Error:
    def __init__(self, err_code: int) -> None:
        if err_code not in err:
            raise Exception(f"invalid error code: {err_code}")
        self.err_code = err_code

    def __str__(self) -> str:
        return f"err_code: {self.err_code}, message: {self.message()}"

    def message(self) -> str:
        return err[self.err_code]

    def has_error(self) -> bool:
        return self.err_code != 0
