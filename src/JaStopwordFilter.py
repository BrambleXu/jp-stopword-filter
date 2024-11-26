import re
import unicodedata
from typing import Callable, List, Optional, Set, Union


def get_stopwords() -> List[str]:
    """Reads the SlothLib stopwords from a file and returns them as a list.

    Returns:
        List[str]: A list of stopwords.
    """
    file_path = "./src/slothlib.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content.splitlines()


def convert_to_halfwidth(text: str) -> str:
    """Converts full-width characters to half-width characters.

    Args:
        text (str): The input string.

    Returns:
        str: The string with full-width characters converted to half-width.
    """
    return unicodedata.normalize("NFKC", text)


class Token:
    """Represents a token with attributes like surface text and part of speech.

    Attributes:
        surface (str): The plain text representation of the token.
        pos (str): The part of speech of the token (e.g., '名詞', '動詞').
    """

    def __init__(self, surface: str, pos: str) -> None:
        """Initializes a Token object.

        Args:
            surface (str): The surface form of the token.
            pos (str): The part of speech of the token.
        """
        self.surface = surface
        self.pos = pos


class JaStopwordFilter:
    """A filter class to remove Japanese stopwords and other undesired tokens based on customizable rules."""

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
        custom_filter: Optional[Callable[[Token], bool]] = None,
    ) -> None:
        """Initializes the JaStopwordFilter with the specified filtering rules.

        Args:
            convert_full_to_half (bool): Whether to convert full-width characters to half-width. Defaults to True.
            use_slothlib (bool): Whether to use the SlothLib stopword list. Defaults to True.
            filter_length (int): Remove tokens with a length less than or equal to this value. Defaults to 0.
            use_date (bool): Whether to remove tokens that match date patterns. Defaults to False.
            use_numbers (bool): Whether to remove numeric tokens. Defaults to False.
            use_symbols (bool): Whether to remove tokens consisting of symbols. Defaults to False.
            use_spaces (bool): Whether to remove tokens that are empty or contain only spaces. Defaults to False.
            use_emojis (bool): Whether to remove tokens containing emojis. Defaults to False.
            custom_wordlist (Optional[List[str]]): A list of user-defined stopwords to remove. Defaults to None.
            custom_filter (Optional[Callable[[Token], bool]]): A custom filter function for Token objects.
                                                               Defaults to None.
        """
        self.stopwords: Set[str] = set()
        self.filter_length = filter_length
        self.use_date = use_date
        self.use_numbers = use_numbers
        self.use_symbols = use_symbols
        self.use_spaces = use_spaces
        self.use_emojis = use_emojis
        self.convert_full_to_half = convert_full_to_half
        self.custom_filter = custom_filter

        if use_slothlib:
            self.stopwords.update(
                convert_to_halfwidth(word) if self.convert_full_to_half else word for word in get_stopwords()
            )

        if custom_wordlist:
            self.stopwords.update(
                convert_to_halfwidth(word) if self.convert_full_to_half else word for word in custom_wordlist
            )

    def remove(self, tokens: List[Union[str, Token]]) -> List[Union[str, Token]]:
        """Removes tokens based on the configured filtering rules.

        Args:
            tokens (List[Union[str, Token]]): A list of tokens to filter.
                                              Tokens can be either strings or Token objects.

        Returns:
            List[Union[str, Token]]: A list of filtered tokens.
        """
        filtered_tokens: List[Union[str, Token]] = []

        for token in tokens:
            if isinstance(token, str):
                content = convert_to_halfwidth(token) if self.convert_full_to_half else token

                if self.custom_filter and self.custom_filter(content):
                    continue
                if self._should_remove(content):
                    continue
                filtered_tokens.append(token)
            elif isinstance(token, Token):
                content = convert_to_halfwidth(token.surface) if self.convert_full_to_half else token.surface

                if self.custom_filter and self.custom_filter(token):
                    continue
                if self._should_remove(content):
                    continue
                filtered_tokens.append(token)

        return filtered_tokens

    def _should_remove(self, content: str) -> bool:
        """Checks if a token should be removed based on various rules.

        Args:
            content (str): The token content to check.

        Returns:
            bool: True if the token should be removed, False otherwise.
        """
        if content in self.stopwords:
            return True
        if self.filter_length > 0 and len(content) <= self.filter_length:
            return True
        if self.use_date and self._is_date(content):
            return True
        if self.use_numbers and self._is_number(content):
            return True
        if self.use_symbols and self._is_symbol(content):
            return True
        if self.use_spaces and content.strip() == "":
            return True
        if self.use_emojis and self._is_emoji(content):
            return True
        return False

    def _is_date(self, content: str) -> bool:
        """Checks if a token matches common Japanese date patterns.

        Args:
            content (str): The token content to check.

        Returns:
            bool: True if the token matches a date pattern, False otherwise.
        """
        date_patterns = [
            r"\d{4}年\d{1,2}月",  # YYYY年MM月
            r"\d{1,2}月\d{1,2}日",  # MM月DD日
            r"\d{4}年\d{1,2}月\d{1,2}日",  # YYYY年MM月DD日
        ]
        return any(re.match(pattern, content) for pattern in date_patterns)

    def _is_number(self, content: str) -> bool:
        """Checks if a token is numeric.

        Args:
            content (str): The token content to check.

        Returns:
            bool: True if the token is numeric, False otherwise.
        """
        return content.isdigit()

    def _is_symbol(self, content: str) -> bool:
        """Checks if a token consists entirely of symbols.

        Args:
            content (str): The token content to check.

        Returns:
            bool: True if the token is a symbol, False otherwise.
        """
        return re.fullmatch(r"[!-/:-@[-`{-~]", content) is not None

    def _is_emoji(self, content: str) -> bool:
        """Checks if a token contains emojis.

        Args:
            content (str): The token content to check.

        Returns:
            bool: True if the token contains emojis, False otherwise.
        """
        return any(
            "\U0001f600" <= char <= "\U0001f64f"
            or "\U0001f300" <= char <= "\U0001f5ff"
            or "\U0001f680" <= char <= "\U0001f6ff"
            or "\U0001f1e0" <= char <= "\U0001f1ff"
            for char in content
        )
