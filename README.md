# JaStopwordFilter

`JaStopwordFilter` is a lightweight Python library designed to filter stopwords from Japanese text based on customizable rules. It provides an efficient way to preprocess Japanese text for natural language processing (NLP) tasks, with support for common stopword removal techniques and user-defined customization.


## Features

- **Preloaded Stopwords**: Includes a comprehensive list of Japanese stopwords from SlothLib.
- **Customizable Rules**:
  - Remove tokens based on **length**.
  - Filter **dates** in common Japanese formats (e.g., `2024年11月`).
  - Exclude **numbers**, **symbols**, **spaces**, and **emojis**.
- **Custom Wordlist**: Add your own stopwords to the filter.
- **Flexible Usage**: Use only the rules you need by enabling or disabling them during initialization.


## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/ja-stopword-filter.git
cd ja-stopword-filter
pip install -r requirements.txt
```


## Usage

### Example Code

```python
from ja_stopword_filter import JaStopwordFilter

# Example token list
tokens = ["2024年11月", "こんにちは", "123", "！", "😊", "スペース", "短い", "custom"]

# Custom wordlist
custom_wordlist = ["custom", "スペース"]

# Initialize the filter
filter = JaStopwordFilter(
    use_slothlib=True,      # Use SlothLib stopwords
    use_length=True,        # Filter tokens with length <= 1
    use_date=True,          # Filter Japanese date formats
    use_numbers=True,       # Filter numeric tokens
    use_symbols=True,       # Filter symbolic tokens
    use_spaces=True,        # Filter whitespace-only tokens
    use_emojis=True,        # Filter emoji tokens
    custom_wordlist=custom_wordlist  # Add custom stopwords
)

# Filter tokens
filtered_tokens = filter.remove(tokens)
print(filtered_tokens)  # Output: ['こんにちは', '短い']
```


## Parameters

The `JaStopwordFilter` class supports the following parameters during initialization:


| Parameter         | Type   | Default | Description                                             |
|--- |--- |--- |---|
| `use_slothlib`    | `bool` | `True`  | Whether to use the SlothLib stopword list.              |
| `use_length`      | `bool` | `False` | Remove tokens with a length of 1 character or less.     |
| `use_date`        | `bool` | `False` | Remove tokens that match Japanese date formats.         |
| `use_numbers`     | `bool` | `False` | Remove numeric tokens.                                  |
| `use_symbols`     | `bool` | `False` | Remove symbolic tokens (e.g., `!`, `@`).                |
| `use_spaces`      | `bool` | `False` | Remove tokens that are empty or consist only of spaces. |
| `use_emojis`      | `bool` | `False` | Remove tokens containing emojis.                        |
| `custom_wordlist` | `list` | `None`  | A list of user-defined stopwords to remove.             |


## Stopword Sources

### SlothLib Stopwords
If `use_slothlib` is set to `True`, the filter loads stopwords from a `slothlib.txt` file. Ensure this file is in the same directory as the script or adjust the file path in the `get_stopwords` function.

### Custom Wordlist
You can pass a list of custom stopwords using the `custom_wordlist` parameter. These will be merged with the SlothLib stopwords if enabled.


## Rules

The filter applies the following rules if they are enabled:

1. **Length Filtering**: Tokens with one or fewer characters are removed.
2. **Date Filtering**: Matches Japanese date patterns like:
   - `YYYY年MM月`
   - `MM月DD日`
   - `YYYY年MM月DD日`
3. **Number Filtering**: Removes numeric tokens (`123`, `2024`).
4. **Symbol Filtering**: Removes punctuation and special symbols.
5. **Space Filtering**: Removes tokens that are empty or consist only of spaces.
6. **Emoji Filtering**: Detects and removes tokens containing emojis.


## Contributing

Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.
