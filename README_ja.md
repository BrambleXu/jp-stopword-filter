[English](./README.md)

# jp-stopword-filter

`jp-stopword-filter` は、カスタマイズ可能なルールに基づいて日本語のストップワードをフィルタリングするための軽量なPythonライブラリです。自然言語処理（NLP）タスクのために日本語テキストを効率的に前処理する方法を提供し、一般的なストップワード削除技術とユーザー定義のカスタマイズをサポートします。


## 特徴

- **プリロードされたストップワード**: SlothLibからの日本語ストップワードリストを含みます。
- **カスタマイズ可能なルール**:
  - **文字数**に基づいてトークンを削除。
  - 日本語形式の日付（例: `2024年11月`）をフィルタリング。
  - **数字**、**記号**、**スペース**、**絵文字**を除外。
- **カスタムワードリスト**: 独自のストップワードをフィルタに追加可能。
- **カスタムフィルタ**: `custom_filter`関数を使用して独自のフィルタリングロジックを定義可能。
- **柔軟な利用**: 初期化時に必要なルールのみを有効または無効にできます。


## インストール

PyPI経由でインストール：

```bash
pip install jp-stopword-filter
```

または、リポジトリをクローンして依存関係をインストール：

```bash
git clone https://github.com/your-username/ja-stopword-filter.git
cd ja-stopword-filter
pip install -r requirements.txt
```


## 使用方法

### 基本的な使い方（文字列トークンのみ）

この例では、文字列として表現されたトークンをフィルタリングします。追加のフィルタリングのためにカスタムワードリストを提供しています。

```python
from ja_stopword_filter import JaStopwordFilter

# トークンリストの定義
tokens = ["２０２４年１１月", "こんにちは", "１２３", "！", "😊", "スペース", "短い", "custom"]

# カスタムワードリスト
custom_wordlist = ["custom", "スペース"]

# フィルタの初期化
filter = JaStopwordFilter(
    convert_full_to_half=True,  # 全角文字を半角文字に変換
    use_slothlib=True,         # SlothLibのストップワードを使用
    filter_length=1,           # 長さが1以下のトークンをフィルタリング
    use_date=True,             # 日付形式のトークンを削除
    use_numbers=True,          # 数字のトークンを削除
    use_symbols=True,          # 記号を含むトークンを削除
    use_spaces=True,           # 空白のみのトークンを削除
    use_emojis=True,           # 絵文字を含むトークンを削除
    custom_wordlist=custom_wordlist  # カスタムストップワードを追加
)

# トークンをフィルタリング
filtered_tokens = filter.remove(tokens)
print(filtered_tokens)  # 出力: ['こんにちは', '短い']
```


### 高度な使い方（`Token`クラスと`custom_filter`の使用）

この例では、`Token`クラスと`custom_filter`関数を使用してカスタムフィルタリングロジックを定義する方法を示します。また、`Token`クラスを拡張してカスタム属性を追加し、それに応じた`custom_filter`関数を設計することもできます。

#### 基本的な`Token`クラスの例

```python
from ja_stopword_filter import JaStopwordFilter, Token

# Tokenオブジェクトのリストを定義
tokens = [
    Token("２０２４年１１月", "名詞"),
    Token("こんにちは", "動詞"),
    Token("１２３", "名詞"),
    Token("短い", "形容詞"),
    Token("custom", "名詞"),
]

# カスタムフィルタ関数を定義
def custom_filter(token: Token) -> bool:
    # 品詞（pos）が"名詞"の場合、トークンを削除
    return token.pos == "名詞"

# フィルタを初期化
filter = JaStopwordFilter(
    convert_full_to_half=True,  # 全角文字を半角文字に変換
    custom_filter=custom_filter,  # カスタムフィルタリングロジックを適用
    use_numbers=True,            # 数字のトークンを削除
    use_emojis=True,             # 絵文字を含むトークンを削除
)

# トークンをフィルタリング
filtered_tokens = filter.remove(tokens)
filtered_surfaces = [t.surface for t in filtered_tokens]
print(filtered_surfaces)  # 出力: ['こんにちは', '短い']
```

#### 拡張された`Token`クラスの例

`Token`クラスを拡張して、`frequency`、`is_special`、`context`などの追加属性を含めることができます。これらの属性を使用して、より複雑なフィルタリングロジックを設計できます。

```python
from ja_stopword_filter import JaStopwordFilter, Token

# Tokenクラスを拡張し、カスタム属性を追加
class ExtendedToken(Token):
    def __init__(self, surface: str, pos: str, frequency: int, is_special: bool) -> None:
        super().__init__(surface, pos)
        self.frequency = frequency  # トークンの頻度
        self.is_special = is_special  # 特殊フラグ

# ExtendedTokenオブジェクトのリストを定義
tokens = [
    ExtendedToken("２０２４年１１月", "名詞", 10, False),
    ExtendedToken("こんにちは", "動詞", 5, True),
    ExtendedToken("１２３", "名詞", 2, False),
    ExtendedToken("短い", "形容詞", 15, False),
    ExtendedToken("custom", "名詞", 3, True),
]

# カスタムフィルタ関数を定義
def custom_filter(token: ExtendedToken) -> bool:
    # 品詞が"名詞"または頻度が5未満のトークンを削除
    return token.pos == "名詞" or token.frequency < 5

# フィルタを初期化
filter = JaStopwordFilter(
    custom_filter=custom_filter,  # カスタムフィルタリングロジックを適用
    use_numbers=True,            # 数字のトークンを削除
    use_symbols=True,            # 記号を含むトークンを削除
)

# トークンをフィルタリング
filtered_tokens = filter.remove(tokens)
filtered_surfaces = [t.surface for t in filtered_tokens]
print(filtered_surfaces)  # 出力: ['こんにちは', '短い']
```


## パラメータ

`JaStopwordFilter`は以下のパラメータをサポートしています：

| パラメータ             | 型                        | デフォルト | 説明                                                      |
|- |- |- |- |
| `convert_full_to_half` | `bool`                    | `True`     | 全角文字を半角文字に変換します。                          |
| `use_slothlib`         | `bool`                    | `True`     | SlothLibのストップワードリストを使用します。              |
| `filter_length`        | `int`                     | `0`        | 指定した文字数以下のトークンを削除します。                |
| `use_date`             | `bool`                    | `False`    | 日本語の日付形式に一致するトークンを削除します。          |
| `use_numbers`          | `bool`                    | `False`    | 数字のトークンを削除します。                              |
| `use_symbols`          | `bool`                    | `False`    | 記号を含むトークンを削除します。                          |
| `use_spaces`           | `bool`                    | `False`    | 空白のみのトークンを削除します。                          |
| `use_emojis`           | `bool`                    | `False`    | 絵文字を含むトークンを削除します。                        |
| `custom_wordlist`      | `list[str]`               | `None`     | カスタムストップワードを追加します。                      |
| `custom_filter`        | `Callable[[Token], bool]` | `None`     | `Token`オブジェクト用のカスタムフィルタ関数を適用します。 |


## フィルタリングルール

### プリロードされたストップワード

デフォルトでは、`JaStopwordFilter` は[SlothLib](http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt)のストップワードを使用します。これは、日本語の一般的なストップワードを網羅したリストです。

さらに、ユーザーは`custom_wordlist`パラメーターを通じて独自のカスタムワードリストを提供することもできます。これにより、特定の分野やタスクに合わせてストップワードのフィルタリングプロセスをさらにカスタマイズできます。

**例: カスタムワードリストを追加する**

```python
from ja_stopword_filter import JaStopwordFilter

# カスタムワードリストを定義
custom_wordlist = ["example", "特定単語", "custom_stopword"]

# カスタムワードリストを使用してフィルタを初期化
filter = JaStopwordFilter(
    use_slothlib=True,           # SlothLibのストップワードを含む
    custom_wordlist=custom_wordlist  # ユーザー定義のストップワードを追加
)

# トークンのリストを定義
tokens = ["こんにちは", "特定単語", "example", "custom_stopword", "一般単語"]

# トークンをフィルタリング
filtered_tokens = filter.remove(tokens)
print(filtered_tokens)  # 出力: ['こんにちは', '一般単語']
```

#### 主なポイント:
- **SlothLibストップワード**: `use_slothlib=True`（デフォルト設定）で自動的に含まれる。
- **カスタムワードリスト**: `custom_wordlist`パラメーターを使用して独自のストップワードを追加可能。
- **ストップワードの統合**: SlothLibのリストとカスタムワードリストがシームレスに連携し、ニーズに合わせた包括的なストップワードの除去を実現。

この機能により、特定の言語、分野、またはプロジェクトに応じた柔軟なフィルタリングプロセスを可能にします。


### ルールの説明
1. **長さによるフィルタリング**: 指定された値以下の長さのトークンを除去します。
2. **日付フィルタリング**: 以下のような日本語の日付パターンを一致させて除去します。
   - `YYYY年MM月`
   - `MM月DD日`
   - `YYYY年MM月DD日`
3. **数値フィルタリング**: `123`や`2024`のような数値のトークンを除去します。
4. **記号フィルタリング**: 句読点や特殊文字を除去します。
5. **スペースフィルタリング**: 空白またはスペースのみのトークンを除去します。
6. **絵文字フィルタリング**: 絵文字を含むトークンを検出して除去します。
7. **カスタムフィルタ**: ユーザー定義のルールに基づいてトークンをフィルタリングするロジックを適用します。


## コントリビューション

バグを見つけた場合や新機能のリクエストがある場合は、Issueを作成するか、Pull Requestを送信してください！