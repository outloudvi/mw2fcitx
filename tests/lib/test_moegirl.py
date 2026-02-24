"""Unit tests for moegirl tweaks module."""
from mw2fcitx.tweaks.moegirl import (
    tweak_remove_word_includes,
    tweak_split_word_with,
    tweak_len_more_than,
    tweak_remove_char,
    tweak_trim_suffix,
    tweak_remove_regex,
    tweak_normalize,
)


class TestTweakRemoveWordIncludes:
    """Tests for tweak_remove_word_includes function."""

    def test_remove_words_with_specific_items(self):
        """Test removing words that include specific items."""
        tweak = tweak_remove_word_includes(["○", "〇"])
        result = tweak(["test○", "another", "test〇", "clean"])
        assert result == ["another", "clean"]

    def test_remove_words_with_single_item(self):
        """Test removing words with a single item."""
        tweak = tweak_remove_word_includes(["a", "b"])
        result = tweak(["abc", "acd", "bde", "def", "ghi"])
        assert result == ["def", "ghi"]


class TestTweakSplitWordWith:
    """Tests for tweak_split_word_with function."""

    def test_split_with_single_separator(self):
        """Test splitting words with a single separator."""
        tweak = tweak_split_word_with([":"])
        result = tweak(["test:case", "another:test"])
        assert set(result) == {"test", "case", "another"}

    def test_split_with_multiple_separators(self):
        """Test splitting words with multiple separators."""
        tweak = tweak_split_word_with([":", "/"])
        result = tweak(["test:case/name", "another/test"])
        assert set(result) == {"test", "case", "name", "another"}

    def test_split_with_wave_dash(self):
        """Test splitting with the full-width wave dash ～."""
        tweak = tweak_split_word_with(["～"])
        result = tweak(["test～case", "another～test"])
        assert set(result) == {"test", "case", "another"}


class TestTweakLenMoreThan:
    """Tests for tweak_len_more_than function."""

    def test_filter_by_length(self):
        """Test filtering words by minimum length."""
        tweak = tweak_len_more_than(1)
        result = tweak(["a", "ab", "abc", ""])
        assert result == ["ab", "abc"]

    def test_filter_length_zero(self):
        """Test filtering with minimum length 0."""
        tweak = tweak_len_more_than(0)
        result = tweak(["", "a", "ab"])
        assert result == ["a", "ab"]

    def test_filter_length_larger_than_all(self):
        """Test filtering with length larger than all words."""
        tweak = tweak_len_more_than(10)
        result = tweak(["test", "case"])
        assert result == []

    def test_filter_empty_input(self):
        """Test filtering with empty input."""
        tweak = tweak_len_more_than(1)
        result = tweak([])
        assert result == []


class TestTweakRemoveChar:
    """Tests for tweak_remove_char function."""

    def test_remove_single_character(self):
        """Test removing a single character from words."""
        tweak = tweak_remove_char("·")
        result = tweak(["test·case", "another"])
        assert result == ["testcase", "another"]

    def test_remove_character_not_present(self):
        """Test removing a character that's not present."""
        tweak = tweak_remove_char("·")
        result = tweak(["test", "case"])
        assert result == ["test", "case"]

    def test_remove_character_empty_input(self):
        """Test removing character with empty input."""
        tweak = tweak_remove_char("·")
        result = tweak([])
        assert result == []


class TestTweakTrimSuffix:
    """Tests for tweak_trim_suffix function."""

    def test_trim_single_suffix(self):
        """Test trimming a single suffix."""
        tweak = tweak_trim_suffix(["系列"])
        result = tweak(["test系列", "case系列", "another"])
        assert result == ["test", "case", "another"]

    def test_trim_multiple_suffixes(self):
        """Test trimming multiple suffixes."""
        tweak = tweak_trim_suffix(["系列", "列表"])
        result = tweak(["test系列", "case列表", "another"])
        assert result == ["test", "case", "another"]

    def test_trim_suffix_not_present(self):
        """Test trimming when suffix is not present."""
        tweak = tweak_trim_suffix(["系列"])
        result = tweak(["test", "case"])
        assert result == ["test", "case"]

    def test_trim_suffix_empty_input(self):
        """Test trimming suffix with empty input."""
        tweak = tweak_trim_suffix(["系列"])
        result = tweak([])
        assert result == []


class TestTweakRemoveRegex:
    """Tests for tweak_remove_regex function."""

    def test_remove_by_regex_pattern(self):
        """Test removing words that match a regex pattern."""
        tweak = tweak_remove_regex(["^第.*(次|话)$"])
        result = tweak(["第一次", "第二话", "normal", "第三章"])
        assert set(result) == {"normal", "第三章"}


class TestTweakNormalize:
    """Tests for tweak_normalize function."""

    def test_normalize_returns_list(self):
        """Test that normalize returns a list."""
        result = tweak_normalize(["test ", " case", "testcase"])
        assert set(result) == {"test", "case", "testcase"}
