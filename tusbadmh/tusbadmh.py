from abc import ABC, abstractmethod
from typing import Tuple
from tusbadmh.result_class import (
    StatusResult,
    LengthResult,
    CheckInputTypeResult,
    DataResult,
)
from tusbadmh.enum import (
    Ch,
    ClkSel,
    InputType,
    Mode,
    TrgSel,
)
from tusbadmh.error import Error


# タートル工業の公式ドキュメント：https://www.turtle-ind.co.jp/wp-content/uploads/TUSB0216ADMH_M2.pdf
class TUSBADMH(ABC):
    @abstractmethod
    def device_open(self, id: int) -> Error:
        """
        指定ID(ユニット番号選択スイッチの値)のデバイスをオープンします。
        このデバイスに関する各種関数を使用する前に必ず呼び出す必要が有ります。

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def device_close(self, id: int) -> None:
        """
        指定ID(ユニット番号選択スイッチの値)のデバイスをクローズします。

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）

        """
        pass

    @abstractmethod
    def dio_read(self, id: int, data: int) -> Error:
        """
        指定ID(ユニット番号選択スイッチの値)のデバイスのディジタル入力ポートの入力値および現在の出力ポートの出力値を読み込みます。
        下位4ビットが入力値、上位4ビットが出力値です。
        取得した数値は2進数にした時の0,1のパターンでLow,Highが示されます。（詳しい対応表はドキュメント）

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）
            data(int): データを格納するバッファのアドレス

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def dio_write(self, id: int, data: int) -> Error:
        """
        指定ID(ユニット番号選択スイッチの値)のデバイスのディジタル出力ポートの出力値を書き込みます。
        書き込みは下位4ビットで、数値とHigh,Lowレベルの関係はTusbadmh_Dio_Readと同じです。

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）
            data(int): 書き込むデータ

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def adc_start(
        self,
        id: int,
        cyc_len: int,
        pre_len: int,
        trg_sel: TrgSel,
        mode: Mode,
        ch1_only: bool,
    ) -> Error:
        """
        連続取り込みを開始します。
        サンプリングクロックの設定など連続取り込みに必要な設定はこの関数を呼ぶ前に行ってください。

        Args:
            id(int): ユニット番号選択スイッチの番号
            cyc_len(int): 繰り返しモードで使用する場合の１トリガ当たりの取り込みデータ数（1~1048576）
            pre_len(int): プレトリガ長（0~1048576）
            trg_sel(enum): 0:外部トリガ 1:立ち上がりトリガ 2:立下りトリガ 3:ソフトトリガ
            mode(enum): 0:トリガ後連続取り込みモードで動作　1:繰り返しトリガモードで動作
            ch1_only(bool): False(0):ch1とch2両方取り込み True(1):ch1のみ取り込み

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def adc_stop(self, id: int) -> Error:
        """
        連続取り込みを停止します。

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def status_get(self, id: int) -> Tuple[StatusResult, Error]:
        """
        連続取り込み状態を確認する。

        Args:
            id(int): ユニット番号選択スイッチの番号（0-15）

        Returns:
            StatusResult.status(enum): 0:停止中 1:トリガ待ち 2:トリガ後変換中
            StatusResult.ovf_st(enum): オーバーフロー状態 0:異常なし 1: ch1オーバーフロー 2: ch2オーバーフロー 3: ch1 とch2 オーバーフロー
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def length(self, id: int) -> Tuple[LengthResult, Error]:
        """
        取り込み完了データ数を取得します。データバッファはデバイス内とPC内にあります。
        デバイスからPCへのデータ転送はドライバで自動的に行います。この関数ではPC内のバッファに取り込まれたデータ長を返します。
        Rateは装置内バッファの使用率で、100%になると自動的に取り込みを停止します。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)

        Returns:
            LengthResult.len_1(int): Ch1 取り込み済み長
            LengthResult.len_2(int): Ch2 取り込み済み長
            LengthResult.rate_1(int): Ch1 装置内バッファ使用率(%)
            LengthResult.rate_2(int): Ch2 装置内バッファ使用率(%)
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def data_get(self, id: int, ch: Ch, leng: int) -> Tuple[DataResult, Error]:
        """
        取り込み済みデータを取得します。取得したデータはバッファ内から消去されます。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)
            ch(enum): チャンネル 0:ch1 1:Ch2
            leng(int): 取り込み要求長。呼び出し時は要求データ数を設定します。

        Returns:
            DataResult.data(list[int]): 取得データ
            DataResult.leng(int): 戻る時は実際に取得できた数が入っています。
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def clock_select(self, id: int, clk_sel: ClkSel, div: int, ave: int) -> Error:
        """
        連続サンプリングのクロックの設定を行います。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)
            clk_sel(enum): クロックソース選択 0: 200MHz   1:20.48MHz   2:16.384MHz   3:12.8MHz 4:1.92MHz   5:Ext ※ 0～4は内部クロックソースです
            div(int): クロックの分周比 0～199 clk_selで選択したクロックををDiv+1で割った値が内部クロックの周波数になります。
                例ClkSel = 0 (200MHz)   Div = 7の場合 200MHz / (7+1) -> 25MHz
                ※ 必ず1MHz～25MHzとなる様に設定してください。
                ※ 外部クロックの時はDivは最大24です。
            ave(int): 平均化設定 0～8 取り込んだデータの平均化機能を設定します。平均化回数は2のAve乗となります。(サンプリング個数は平均回数分の1になります)
                例) Ave = 4の時  2^4 = 16となり16回平均

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def thlevel_set(self, id: int, th_level: int, n_level: int) -> Error:
        """
        連続サンプリング時のアナログトリガ基準レベルの設定を行います。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)
            th_level(int): アナログ信号立ち上がりおよび立下りトリガの時の基準レベル設定 1～65534(変換値単位)
            n_level(int): ノイズ除去レベル アナログ信号トリガのときの誤動作防止レベルの設定値 0～3277(変換値単位)
                ※ ノイズレベルよりも十分大きく、信号振幅よりも十分小さい値が適切ですが、不明な場合は800程度を設定してください。

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def input_type(self, id: int, type_1: InputType, type_2: InputType) -> Error:
        """
        入力レンジの設定を行います。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)
            type_1(enum): Ch1 入力タイプ 0->バイポーラ(-1V～1V)  1->ユニポーラ(0V～2V)
            type_2(enum): Ch2 入力タイプ 0->バイポーラ(-1V～1V)  1->ユニポーラ(0V～2V)

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def check_input_type(self, id: int) -> Tuple[CheckInputTypeResult, Error]:
        """
        現在設定されている入力レンジの確認を行います。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)

        Returns:
            CheckInputTypeResult.type_1(int): Ch1 入力タイプ 0->バイポーラ(-1V～1V)  1->ユニポーラ(0V～2V)
            CheckInputTypeResult.type_2(int): Ch2 入力タイプ 0->バイポーラ(-1V～1V)  1->ユニポーラ(0V～2V)
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def trigger(self, id: int) -> Error:
        """
        ソフトウェアトリガをかけます。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass

    @abstractmethod
    def translimit(self, id: int, limit: int) -> Error:
        """
        転送サイズ制限を設定します。USB通信における転送データブロックのサイズを設定します。
        高速サンプリングかつ1回あたりの必要データ数が少ない場合にこの値を小さくすると応答性が良くなる場合があります。
        大量にデータを取得する時にこの値を小さくしすぎると転送効率が低下します。通常使用ではデフォルト値の50000データのままで設定不要です。
        設定目安としては(スタート~ストップ間の)必要なデータ長より少し大きい値に設定してみて下さい。

        Args:
            id(int): ユニット番号選択スイッチの番号(0-15)
            limit(int): 転送サイズ制限(100~100000)

        Returns:
            Error.code(int): エラーコード
            Error.message(str): エラーメッセージ

        """
        pass
