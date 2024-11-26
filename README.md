[日本語](./README_j.md)

# jp-stopword-filter

`jp-stopword-filter` is a lightweight Python library designed to filter stopwords from Japanese text based on customizable rules. It provides an efficient way to preprocess Japanese text for natural language processing (NLP) tasks, with support for common stopword removal techniques and user-defined customization.


## Features

- **Preloaded Stopwords**: Includes a comprehensive list of Japanese stopwords from SlothLib.
- **Customizable Rules**:
  - Remove tokens based on **length**.
  - Filter **dates** in common Japanese formats (e.g., `2024年11月`).
  - Exclude **numbers**, **symbols**, **spaces**, and **emojis**.
- **Custom Wordlist**: Add your own stopwords to the filter.
- **Custom Filters**: Define your own filtering logic with a `custom_filter` function.
- **Flexible Usage**: Use only the rules you need by enabling or disabling them during initialization.


## Installation

Install via PyPI:

```bash
pip install jp-stopword-filter
```

Alternatively, clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/ja-stopword-filter.git
cd ja-stopword-filter
pip install -r requirements.txt
```


## Usage

### Basic Usage (String Tokens Only)

In this example, we filter tokens represented as strings. A custom wordlist is provided for additional filtering.

```python
from ja_stopword_filter import JaStopwordFilter

# Define a token list
tokens = ["２０２４年１１月", "こんにちは", "１２３", "！", "😊", "スペース", "短い", "custom"]

# Custom wordlist
custom_wordlist = ["custom", "スペース"]

# Initialize the filter
filter = JaStopwordFilter(
    convert_full_to_half=True,  # Convert full-width characters to half-width
    use_slothlib=True,         # Include SlothLib stopwords
    filter_length=1,           # Filter tokens with length <= 1
    use_date=True,             # Remove tokens matching date patterns
    use_numbers=True,          # Remove numeric tokens
    use_symbols=True,          # Remove tokens with symbols
    use_spaces=True,           # Remove empty or whitespace-only tokens
    use_emojis=True,           # Remove emoji-containing tokens
    custom_wordlist=custom_wordlist  # Add custom stopwords
)

# Filter tokens
filtered_tokens = filter.remove(tokens)
print(filtered_tokens)  # Output: ['こんにちは', '短い']
```


### Advanced Usage (Using `Token` Class and `custom_filter`)

This example demonstrates how to use the `Token` class and a `custom_filter` function to define custom filtering logic. Additionally, you can extend the `Token` class to include custom attributes and design corresponding `custom_filter` functions to suit specific use cases.

#### Example with Basic `Token` Class

```python
from ja_stopword_filter import JaStopwordFilter, Token

# Define a list of Token objects
tokens = [
    Token("２０２４年１１月", "名詞"),
    Token("こんにちは", "動詞"),
    Token("１２３", "名詞"),
    Token("短い", "形容詞"),
    Token("custom", "名詞"),
]

# Define a custom filter function
def custom_filter(token: Token) -> bool:
    # Remove tokens where the part of speech (pos) is "名詞"
    return token.pos == "名詞"

# Initialize the filter
filter = JaStopwordFilter(
    convert_full_to_half=True,  # Convert full-width characters to half-width
    custom_filter=custom_filter,  # Apply custom filtering logic
    use_numbers=True,            # Remove numeric tokens
    use_emojis=True,             # Remove tokens with emojis
)

# Filter tokens
filtered_tokens = filter.remove(tokens)
filtered_surfaces = [t.surface for t in filtered_tokens]
print(filtered_surfaces)  # Output: ['こんにちは', '短い']
```

#### Example with Extended `Token` Class

You can extend the `Token` class to include additional attributes, such as `frequency`, `is_special`, or `context`. These attributes allow you to design more complex filtering logic.

```python
from ja_stopword_filter import JaStopwordFilter, Token

# Extend the Token class to include custom attributes
class ExtendedToken(Token):
    def __init__(self, surface: str, pos: str, frequency: int, is_special: bool) -> None:
        super().__init__(surface, pos)
        self.frequency = frequency  # Frequency of the token in the text
        self.is_special = is_special  # Whether the token is marked as special

# Define a list of ExtendedToken objects
tokens = [
    ExtendedToken("２０２４年１１月", "名詞", 10, False),
    ExtendedToken("こんにちは", "動詞", 5, True),
    ExtendedToken("１２３", "名詞", 2, False),
    ExtendedToken("短い", "形容詞", 15, False),
    ExtendedToken("custom", "名詞", 3, True),
]

# Define a custom filter function
def custom_filter(token: ExtendedToken) -> bool:
    # Remove tokens if they are "名詞" or their frequency is less than 5
    return token.pos == "名詞" or token.frequency < 5

# Initialize the filter
filter = JaStopwordFilter(
    custom_filter=custom_filter,  # Apply custom filtering logic
    use_numbers=True,            # Remove numeric tokens
    use_symbols=True,            # Remove tokens with symbols
)

# Filter tokens
filtered_tokens = filter.remove(tokens)
filtered_surfaces = [t.surface for t in filtered_tokens]
print(filtered_surfaces)  # Output: ['こんにちは', '短い']
```

Key Points:
- **Custom Attributes**: Add attributes like `frequency`, `is_special`, or others depending on your requirements.
- **Flexible Filtering**: Use the `custom_filter` parameter to define logic based on the extended attributes.
- **Use Cases**:
  - Filter tokens by their frequency in the text.
  - Exclude special or flagged tokens.
  - Combine part of speech filtering with additional attribute-based rules.

This flexibility allows `jp-stopword-filter` to adapt to a wide variety of text preprocessing tasks beyond stopword removal.



## Parameters

`JaStopwordFilter` supports the following parameters for customization:

| Parameter              | Type                      | Default | Description                                             |
|- |- |- |- |
| `convert_full_to_half` | `bool`                    | `True`  | Convert full-width characters to half-width.            |
| `use_slothlib`         | `bool`                    | `True`  | Use the SlothLib stopword list.                         |
| `filter_length`        | `int`                     | `0`     | Remove tokens with length ≤ this value (0 disables it). |
| `use_date`             | `bool`                    | `False` | Remove tokens matching Japanese date patterns.          |
| `use_numbers`          | `bool`                    | `False` | Remove numeric tokens.                                  |
| `use_symbols`          | `bool`                    | `False` | Remove tokens containing symbols.                       |
| `use_spaces`           | `bool`                    | `False` | Remove tokens that are empty or consist only of spaces. |
| `use_emojis`           | `bool`                    | `False` | Remove tokens containing emojis.                        |
| `custom_wordlist`      | `list[str]`               | `None`  | Add custom stopwords.                                   |
| `custom_filter`        | `Callable[[Token], bool]` | `None`  | Apply a custom filter function for Token objects.       |


## Filtering Rules

### Preloaded Stopwords

By default, `JaStopwordFilter` uses stopwords from [SlothLib](http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt), a comprehensive list of commonly used Japanese stopwords. 

In addition to the SlothLib stopwords, users can provide their own custom wordlist through the `custom_wordlist` parameter. This allows for further customization of the filtering process by adding domain-specific or task-specific stopwords.

**Example: Adding a Custom Wordlist**

```python
from ja_stopword_filter import JaStopwordFilter

# Define a custom wordlist
custom_wordlist = ["example", "特定単語", "custom_stopword"]

# Initialize the filter with a custom wordlist
filter = JaStopwordFilter(
    use_slothlib=True,           # Include SlothLib stopwords
    custom_wordlist=custom_wordlist  # Add user-defined stopwords
)

# Define a list of tokens
tokens = ["こんにちは", "特定単語", "example", "custom_stopword", "一般単語"]

# Filter tokens
filtered_tokens = filter.remove(tokens)
print(filtered_tokens)  # Output: ['こんにちは', '一般単語']
```

#### Key Points:
- **SlothLib Stopwords**: Automatically included when `use_slothlib=True` (default setting).
- **Custom Wordlist**: Use the `custom_wordlist` parameter to add your own stopwords.
- **Combining Stopwords**: SlothLib and custom wordlists work together seamlessly, ensuring comprehensive stopword removal tailored to your needs.

This feature ensures flexibility, allowing users to adapt the filtering process to specific languages, domains, or projects.


### Rule Descriptions
1. **Length Filtering**: Removes tokens with length ≤ the specified value.
2. **Date Filtering**: Matches and removes Japanese date patterns such as:
   - `YYYY年MM月`
   - `MM月DD日`
   - `YYYY年MM月DD日`
3. **Number Filtering**: Removes numeric tokens like `123` or `2024`.
4. **Symbol Filtering**: Removes punctuation and special characters.
5. **Space Filtering**: Removes empty or whitespace-only tokens.
6. **Emoji Filtering**: Detects and removes tokens containing emojis.
7. **Custom Filter**: Apply custom logic to filter tokens based on user-defined rules.


## Contributing

Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.
