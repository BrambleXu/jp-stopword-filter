# jp-stopword-filter

`jp-stopword-filter` is a lightweight Python library designed to filter stopwords from Japanese text based on customizable rules. It provides an efficient way to preprocess Japanese text for natural language processing (NLP) tasks, with support for common stopword removal techniques and user-defined customization.


## Features

- **Preloaded Stopwords**: Includes a comprehensive list of Japanese stopwords from SlothLib.
- **Customizable Rules**:
  - Remove tokens based on **length**.
  - Filter **dates** in common Japanese formats (e.g., `2024年11月`).
  - Exclude **numbers**, **symbols**, **spaces**, and **emojis**.
- **Custom Wordlist**: Add your own stopwords to the filter.
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

### Example Code

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


## Parameters

`JaStopwordFilter` supports the following parameters for customization:

| Parameter              | Type        | Default | Description                                             |
| ---------------------- | ----------- | ------- | ------------------------------------------------------- |
| `convert_full_to_half` | `bool`      | `True`  | Convert full-width characters to half-width.            |
| `use_slothlib`         | `bool`      | `True`  | Use the SlothLib stopword list.                         |
| `filter_length`        | `int`       | `0`     | Remove tokens with length ≤ this value (0 disables it). |
| `use_date`             | `bool`      | `False` | Remove tokens matching Japanese date patterns.          |
| `use_numbers`          | `bool`      | `False` | Remove numeric tokens.                                  |
| `use_symbols`          | `bool`      | `False` | Remove tokens containing symbols.                       |
| `use_spaces`           | `bool`      | `False` | Remove tokens that are empty or consist only of spaces. |
| `use_emojis`           | `bool`      | `False` | Remove tokens containing emojis.                        |
| `custom_wordlist`      | `list[str]` | `None`  | Add custom stopwords.                                   |


## Filtering Rules

### Preloaded Stopwords
By default, `JaStopwordFilter` uses stopwords from a `slothlib.txt` file. Ensure the file is available in the `./src` directory or update the `get_stopwords` function's path.

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

## Future Improvements

- Support for additional token attributes (e.g., `part of speech`).


## Contributing

Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.
