import pytest

from src.JaStopwordFilter import JaStopwordFilter, convert_to_halfwidth, get_stopwords


@pytest.fixture
def tokens():
    """
    A sample token list for testing.
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


def test_get_stopwords():
    """
    Test if get_stopwords correctly loads stopwords from a file.
    """
    stopwords = get_stopwords()
    assert isinstance(stopwords, list), "Stopwords should be returned as a list."
    assert len(stopwords) > 0, "Stopwords list should not be empty."


def test_convert_to_halfwidth():
    """
    Test if convert_to_halfwidth correctly converts full-width characters to half-width.
    """
    assert convert_to_halfwidth("１２３") == "123", "Full-width numbers should convert to half-width."
    assert convert_to_halfwidth("ＡＢＣ") == "ABC", "Full-width letters should convert to half-width."
    assert convert_to_halfwidth("！＠＃") == "!@#", "Full-width symbols should convert to half-width."


def test_init_with_full_to_half(tokens):
    """
    Test if the JaStopwordFilter correctly handles full-to-half conversion during initialization.
    """
    filter = JaStopwordFilter(convert_full_to_half=True)
    assert filter.convert_full_to_half, "convert_full_to_half should be True when enabled."


def test_remove_with_full_to_half(tokens):
    """
    Test if tokens are correctly filtered after converting full-width to half-width.
    """
    custom_wordlist = ["123", "custom"]
    filter = JaStopwordFilter(convert_full_to_half=True, custom_wordlist=custom_wordlist)
    filtered = filter.remove(tokens)
    assert "１２３" not in filtered, "Full-width '１２３' should be converted and removed."
    assert "custom" not in filtered, "'custom' should be removed."
    assert "２０２４年１１月" not in filtered, "Full-width date should be converted and removed."


def test_remove_without_full_to_half(tokens):
    """
    Test if tokens are filtered without converting full-width to half-width.
    """
    custom_wordlist = ["１２３", "custom"]
    filter = JaStopwordFilter(convert_full_to_half=False, custom_wordlist=custom_wordlist)
    filtered = filter.remove(tokens)
    assert "１２３" not in filtered, "Full-width '１２３' should be removed."
    assert "123" in filtered, "Half-width '123' should not be removed."
    assert "custom" not in filtered, "'custom' should be removed."


def test_filter_length(tokens):
    """
    Test if tokens with length less than or equal to filter_length are correctly removed.
    """
    filter = JaStopwordFilter(filter_length=2, convert_full_to_half=True)
    filtered = filter.remove(tokens)
    assert "短" not in filtered, "'短' should be removed because its length is <= 2."
    assert "長い単語" in filtered, "'長い単語' should remain because its length is > 2."


def test_remove_with_date(tokens):
    """
    Test if tokens matching date patterns are correctly removed.
    """
    filter = JaStopwordFilter(use_date=True, convert_full_to_half=True)
    filtered = filter.remove(tokens)
    assert "２０２４年１１月" not in filtered, "Full-width date should be converted and removed."
    assert "2024年11月" not in filtered, "Half-width date should be removed."


def test_remove_with_numbers(tokens):
    """
    Test if numeric tokens are correctly removed.
    """
    filter = JaStopwordFilter(use_numbers=True, convert_full_to_half=True)
    filtered = filter.remove(tokens)
    assert "１２３" not in filtered, "Full-width number should be converted and removed."
    assert "123" not in filtered, "Half-width number should be removed."


def test_remove_with_symbols(tokens):
    """
    Test if symbolic tokens are correctly removed.
    """
    filter = JaStopwordFilter(use_symbols=True, convert_full_to_half=True)
    filtered = filter.remove(tokens)
    assert "！" not in filtered, "Full-width symbol should be converted and removed."
    assert "!" not in filtered, "Half-width symbol should be removed."


def test_remove_with_spaces():
    """
    Test if empty or whitespace-only tokens are correctly removed.
    """
    tokens_with_spaces = [" ", "　", "custom"]
    filter = JaStopwordFilter(use_spaces=True, convert_full_to_half=True)
    filtered = filter.remove(tokens_with_spaces)
    assert " " not in filtered, "Half-width space should be removed."
    assert "　" not in filtered, "Full-width space should be removed."
    assert "custom" in filtered, "'custom' should remain."


def test_remove_with_emojis(tokens):
    """
    Test if tokens containing emojis are correctly removed.
    """
    filter = JaStopwordFilter(use_emojis=True, convert_full_to_half=True)
    filtered = filter.remove(tokens)
    assert "😊" not in filtered, "Emoji '😊' should be removed."


def test_combined_rules(tokens):
    """
    Test if the filter works correctly with combined rules and full-to-half conversion.
    """
    custom_wordlist = ["123", "custom"]
    filter = JaStopwordFilter(
        filter_length=2,
        use_date=True,
        use_numbers=True,
        use_symbols=True,
        use_emojis=True,
        convert_full_to_half=True,
        custom_wordlist=custom_wordlist,
    )
    filtered = filter.remove(tokens)
    assert "２０２４年１１月" not in filtered, "Full-width date should be converted and removed."
    assert "123" not in filtered, "Half-width number should be removed."
    assert "１２３" not in filtered, "Full-width number should be converted and removed."
    assert "！" not in filtered, "Full-width symbol should be converted and removed."
    assert "😊" not in filtered, "Emoji '😊' should be removed."
    assert "短" not in filtered, "Tokens with length <= 2 should be removed."
    assert "長い単語" in filtered, "'長い単語' should remain in the filtered list."


def test_no_rules(tokens):
    """
    Test if all tokens are retained when no rules are enabled.
    """
    filter = JaStopwordFilter(convert_full_to_half=False, use_slothlib=False)
    filtered = filter.remove(tokens)
    assert filtered == [
        "２０２４年１１月",
        "2024年11月",
        "１２３",
        "123",
        "！",
        "!",
        "😊",
        "短",
        "長い単語",
        "custom",
    ], "All tokens should remain when no rules are enabled."
