import re
import unicodedata
from typing import List, Optional, Set


def get_stopwords() -> List[str]:
    """
    Reads the SlothLib stopwords from a file and returns them as a list.

    Returns:
        List[str]: A list of Japanese stopwords from SlothLib.
    """
    file_path = "./src/slothlib.txt"

    # Reading the file content and converting it into a list
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Splitting the content by lines to get a list of stop words
    japanese_stop_words_list = content.splitlines()

    return japanese_stop_words_list


def convert_to_halfwidth(text: str) -> str:
    """
    Converts a string from full-width to half-width characters.

    Args:
        text (str): The input string.

    Returns:
        str: The converted string with half-width characters.
    """
    return unicodedata.normalize("NFKC", text)


class JaStopwordFilter:
    """
    A filter class to remove Japanese stopwords and other undesired tokens
    based on customizable rules.
    """

    def __init__(
        self,
        convert_full_to_half: bool = True,
        use_slothlib: bool = True,
        filter_length: int = 0,
        use_date: bool = False,
        use_numbers: bool = False,
        use_symbols: bool = False,
        use_spaces: bool = False,
        use_emojis: bool = False,
        custom_wordlist: Optional[List[str]] = None,
    ) -> None:
        """
        Initializes the JaStopwordFilter with the specified filtering rules.

        Args:
            convert_full_to_half (bool): Whether to convert full-width characters to half-width. Defaults to True.
            use_slothlib (bool): Whether to use the SlothLib stopword list. Defaults to True.
            filter_length (int): Remove tokens with a length less than or equal to this value.
                                 Defaults to 0 (no filtering).
            use_date (bool): Whether to remove tokens that match Japanese date patterns. Defaults to False.
            use_numbers (bool): Whether to remove numeric tokens. Defaults to False.
            use_symbols (bool): Whether to remove tokens consisting of symbols. Defaults to False.
            use_spaces (bool): Whether to remove tokens that are empty or contain only spaces. Defaults to False.
            use_emojis (bool): Whether to remove tokens containing emojis. Defaults to False.
            custom_wordlist (Optional[List[str]]): A list of user-defined stopwords to remove. Defaults to None.
        """
        self.stopwords: Set[str] = set()
        self.filter_length = filter_length
        self.use_date = use_date
        self.use_numbers = use_numbers
        self.use_symbols = use_symbols
        self.use_spaces = use_spaces
        self.use_emojis = use_emojis
        self.convert_full_to_half = convert_full_to_half

        # Load SlothLib stopwords
        if use_slothlib:
            self.stopwords.update(
                convert_to_halfwidth(word) if self.convert_full_to_half else word for word in get_stopwords()
            )

        # Add custom wordlist to stopwords
        if custom_wordlist:
            self.stopwords.update(
                convert_to_halfwidth(word) if self.convert_full_to_half else word for word in custom_wordlist
            )

    def remove(self, tokens: List[str]) -> List[str]:
        """
        Removes tokens based on the filtering rules.

        Args:
            tokens (List[str]): A list of input tokens to filter.

        Returns:
            List[str]: A list of filtered tokens.
        """
        # Convert tokens to half-width if the option is enabled
        if self.convert_full_to_half:
            tokens = [convert_to_halfwidth(token) for token in tokens]

        filtered_tokens: List[str] = []
        for token in tokens:
            if token in self.stopwords:
                continue
            if self.filter_length > 0 and len(token) <= self.filter_length:
                continue
            if self.use_date and self._is_date(token):
                continue
            if self.use_numbers and self._is_number(token):
                continue
            if self.use_symbols and self._is_symbol(token):
                continue
            if self.use_spaces and token.strip() == "":
                continue
            if self.use_emojis and self._is_emoji(token):
                continue
            filtered_tokens.append(token)
        return filtered_tokens

    def _is_date(self, token: str) -> bool:
        """
        Checks if a token matches common Japanese date patterns.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token matches a date pattern, otherwise False.
        """
        date_patterns = [
            r"\d{4}年\d{1,2}月",  # YYYY年MM月
            r"\d{1,2}月\d{1,2}日",  # MM月DD日
            r"\d{4}年\d{1,2}月\d{1,2}日",  # YYYY年MM月DD日
        ]
        return any(re.match(pattern, token) for pattern in date_patterns)

    def _is_number(self, token: str) -> bool:
        """
        Checks if a token is numeric.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is numeric, otherwise False.
        """
        return token.isdigit()

    def _is_symbol(self, token: str) -> bool:
        """
        Checks if a token is a symbol.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a symbol, otherwise False.
        """
        return re.fullmatch(r"[!-/:-@[-`{-~]", token) is not None

    def _is_emoji(self, token: str) -> bool:
        """
        Checks if a token contains emojis.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token contains emojis, otherwise False.
        """
        return any(
            "\U0001f600" <= char <= "\U0001f64f"  # Emoticons
            or "\U0001f300" <= char <= "\U0001f5ff"  # Symbols & Pictographs
            or "\U0001f680" <= char <= "\U0001f6ff"  # Transport & Map Symbols
            or "\U0001f1e0" <= char <= "\U0001f1ff"  # Flags
            for char in token
        )
