# tusbadmh

タートル工業の AD 変換器[TUSB-0216ADMH](https://www.turtle-ind.co.jp/products/ad-converters/tusb-0216admh/)を Python で扱うためのライブラリです。

## セットアップ

1. タートル工業の[ソフトウェアダウンロード](https://www.turtle-ind.co.jp/download/win7_8_10/)のサイトから TUSB-0216ADMH 用のソフトをダウンロード
2. `DRIVER`ディレクトリをプロジェクトのディレクトリに配置
3. `pip install git+https://github.com/Kohei-Asai/tusbadmh`を実行する
   - PyPI には登録していないです

## 使い方

- ディレクトリ構成

```
.
├── DRIVER/
│   ├── amd64/
│   └── x86/
├── main.py
```

- `main.py`
  - 詳しい API の呼び出し順などは[タートル工業のドキュメント](https://www.turtle-ind.co.jp/wp-content/uploads/TUSB0216ADMH_M2.pdf)を参照

```python
from tusbadmh import TUSBADMH, TUSBADMHImpl, TUSBADMHMockImpl, InputType

def main(tusbadmh: TUSBADMH) -> None:
    err = tusbadmh.device_open(id=0)
    if err.has_error():
        raise Exception(f"could not open device: {err.message()}")

    err = tusbadmh.input_type(id=0, type_1=InputType.BIPOLAR, type_2=InputType.BIPOLAR)
    if err.has_error():
        raise Exception(f"could not set input type: {err.message()}")
    ...


if __name__ == "__main__":
    use_mock = False
    if use_mock:
        # 機器そのものが手元になくてもコードを動かせるようにmockを実装してある
        # mockはかなり雑なので大した動きはしない
        tusbadmh_mock_impl = TUSBADMHMockImpl()
        main(tusbadmh=tusbadmh_impl)
    else:
        tusbadmh_impl = TUSBADMHImpl(dll_path="./DRIVER/amd64/TUSBADMH.dll")
        # PCのアーキテクチャによってはx86をインポートする
        main(tusbadmh=tusbadmh_impl)
```
