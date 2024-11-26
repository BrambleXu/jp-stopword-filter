import pytest

from src.JaStopwordFilter import JaStopwordFilter, Token, convert_to_halfwidth, get_stopwords


@pytest.fixture
def tokens_str_list() -> list[str]:
    """Provides a sample list of string tokens for testing.

    Returns:
        list[str]: A list of string tokens.
    """
    return [
        "２０２４年１１月",  # Full-width date
        "2024年11月",  # Half-width date
        "１２３",  # Full-width number
        "123",  # Half-width number
        "！",  # Full-width symbol
        "!",  # Half-width symbol
        "😊",  # Emoji
        "短",  # Short token
        "長い単語",  # Long token
        "custom",  # Custom word
    ]


@pytest.fixture
def tokens_class_list() -> list[Token]:
    """Provides a sample list of Token objects for testing.

    Returns:
        list[Token]: A list of Token objects.
    """
    return [
        Token("２０２４年１１月", "名詞"),
        Token("2024年11月", "名詞"),
        Token("１２３", "名詞"),
        Token("123", "名詞"),
        Token("！", "記号"),
        Token("!", "記号"),
        Token("😊", "記号"),
        Token("短", "形容詞"),
        Token("長い単語", "名詞"),
        Token("custom", "名詞"),
    ]


def test_get_stopwords() -> None:
    """Tests if stopwords are correctly loaded and returned as a list."""
    stopwords = get_stopwords()
    assert isinstance(stopwords, list), "Stopwords should be returned as a list."
    assert len(stopwords) > 0, "Stopwords list should not be empty."


def test_convert_to_halfwidth() -> None:
    """Tests the conversion of full-width characters to half-width."""
    assert convert_to_halfwidth("１２３") == "123", "Full-width numbers should convert to half-width."
    assert convert_to_halfwidth("ＡＢＣ") == "ABC", "Full-width letters should convert to half-width."
    assert convert_to_halfwidth("！＠＃") == "!@#", "Full-width symbols should convert to half-width."


def test_token_class() -> None:
    """Tests the initialization of the Token class."""
    token = Token("テスト", "名詞")
    assert token.surface == "テスト", "The surface attribute should match the given value."
    assert token.pos == "名詞", "The pos attribute should match the given value."


def test_filter_init() -> None:
    """Tests the initialization of the JaStopwordFilter class."""
    filter = JaStopwordFilter(convert_full_to_half=True)
    assert filter.convert_full_to_half, "convert_full_to_half should be True."


def test_remove_with_str_list(tokens_str_list: list[str]) -> None:
    """Tests filtering a list of string tokens."""
    filter = JaStopwordFilter(
        convert_full_to_half=True,
        use_date=True,
        use_numbers=True,
        use_symbols=True,
        use_emojis=True,
        custom_wordlist=["custom"],
    )
    filtered = filter.remove(tokens_str_list)
    assert "２０２４年１１月" not in filtered, "Full-width date should be removed."
    assert "123" not in filtered, "Numbers should be removed."
    assert "!" not in filtered, "Symbols should be removed."
    assert "😊" not in filtered, "Emojis should be removed."
    assert "長い単語" in filtered, "Long tokens should be retained."


def test_remove_with_class_list(tokens_class_list: list[Token]) -> None:
    """Tests filtering a list of Token objects."""
    filter = JaStopwordFilter(
        convert_full_to_half=True,
        use_date=True,
        use_numbers=True,
        use_symbols=True,
        use_emojis=True,
        custom_wordlist=["custom"],
    )
    filtered = filter.remove(tokens_class_list)
    filtered_surfaces = [t.surface for t in filtered]
    assert "２０２４年１１月" not in filtered_surfaces, "Full-width date should be removed."
    assert "123" not in filtered_surfaces, "Numbers should be removed."
    assert "!" not in filtered_surfaces, "Symbols should be removed."
    assert "😊" not in filtered_surfaces, "Emojis should be removed."
    assert "長い単語" in filtered_surfaces, "Long tokens should be retained."


def test_filter_length(tokens_str_list: list[str]) -> None:
    """Tests filtering tokens based on length."""
    filter = JaStopwordFilter(filter_length=2, convert_full_to_half=True)
    filtered = filter.remove(tokens_str_list)
    assert "短" not in filtered, "Tokens with length <= 2 should be removed."
    assert "長い単語" in filtered, "Tokens with length > 2 should be retained."


def test_filter_combined_rules(tokens_class_list: list[Token]) -> None:
    """Tests filtering with a combination of rules."""
    filter = JaStopwordFilter(
        filter_length=2,
        use_date=True,
        use_numbers=True,
        use_symbols=True,
        use_emojis=True,
        convert_full_to_half=True,
        custom_wordlist=["custom"],
    )
    filtered = filter.remove(tokens_class_list)
    filtered_surfaces = [t.surface for t in filtered]
    assert "２０２４年１１月" not in filtered_surfaces, "Full-width date should be removed."
    assert "123" not in filtered_surfaces, "Numbers should be removed."
    assert "!" not in filtered_surfaces, "Symbols should be removed."
    assert "😊" not in filtered_surfaces, "Emojis should be removed."
    assert "長い単語" in filtered_surfaces, "Long tokens should be retained."
    assert "短" not in filtered_surfaces, "Short tokens should be removed."
    assert "custom" not in filtered_surfaces, "Custom stopwords should be removed."


def test_no_rules(tokens_str_list: list[str]) -> None:
    """Tests filtering with no rules enabled."""
    filter = JaStopwordFilter(
        convert_full_to_half=False,
        use_slothlib=False,
    )
    filtered = filter.remove(tokens_str_list)
    assert filtered == tokens_str_list, "All tokens should be retained when no rules are enabled."


def test_custom_filter_with_str_list(tokens_str_list: list[str]) -> None:
    """Tests filtering with a custom filter applied to a string token list."""

    def custom_filter(token: str) -> bool:
        return "長" in token

    filter = JaStopwordFilter(
        convert_full_to_half=False,
        custom_filter=custom_filter,
    )
    filtered = filter.remove(tokens_str_list)
    assert "長い単語" not in filtered, "Tokens containing '長' should be removed by the custom filter."
    assert "短" in filtered, "Tokens not matching the custom filter should be retained."


def test_custom_filter_with_class_list(tokens_class_list: list[Token]) -> None:
    """Tests filtering with a custom filter applied to a Token class list."""

    def custom_filter(token: Token) -> bool:
        return token.pos == "名詞"

    filter = JaStopwordFilter(
        convert_full_to_half=False,
        custom_filter=custom_filter,
    )
    filtered = filter.remove(tokens_class_list)
    filtered_surfaces = [t.surface for t in filtered]
    assert "２０２４年１１月" not in filtered_surfaces, "Tokens with pos '名詞' should be removed."
    assert "短" in filtered_surfaces, "Tokens with pos other than '名詞' should be retained."


def test_custom_filter_combined_rules(tokens_class_list: list[Token]) -> None:
    """Tests filtering with a custom filter and combined rules."""

    def custom_filter(token: Token) -> bool:
        return "custom" in token.surface

    filter = JaStopwordFilter(
        convert_full_to_half=True,
        use_numbers=True,
        use_symbols=True,
        custom_filter=custom_filter,
    )
    filtered = filter.remove(tokens_class_list)
    filtered_surfaces = [t.surface for t in filtered]
    assert "custom" not in filtered_surfaces, "Tokens matching the custom filter should be removed."
    assert "123" not in filtered_surfaces, "Numbers should be removed by rules."
    assert "!" not in filtered_surfaces, "Symbols should be removed by rules."
    assert "長い単語" in filtered_surfaces, "Tokens not matching any rules should be retained."
