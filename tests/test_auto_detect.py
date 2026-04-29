from __future__ import annotations

import pandas as pd
import pytest

from mmcs._quick_api import _auto_detect_columns, _resolve_frame

_X_NAMES = ["Group", "Treatment", "Condition", "Genotype", "Strain", "CellType", "Dose"]
_Y_NAMES = ["Value", "Expression", "Signal", "Score", "Intensity", "FoldChange"]


class TestAutoDetectColumns:
    def test_known_x_known_y(self):
        df = pd.DataFrame({"Group": ["A", "B"], "Expression": [1.0, 2.0]})
        x, y = _auto_detect_columns(df)
        assert x == "Group"
        assert y == "Expression"

    @pytest.mark.parametrize("col", _X_NAMES)
    def test_known_x_names(self, col):
        df = pd.DataFrame({col: ["A", "B"], "Value": [1.0, 2.0]})
        x, y = _auto_detect_columns(df)
        assert x == col, f"Expected x={col}, got {x}"
        assert y == "Value"

    @pytest.mark.parametrize("col", _Y_NAMES)
    def test_known_y_names(self, col):
        df = pd.DataFrame({"Group": ["A", "B"], col: [1, 2]})
        x, y = _auto_detect_columns(df)
        assert x == "Group"
        assert y == col, f"Expected y={col}, got {y}"

    def test_fallback_categorical_x(self):
        df = pd.DataFrame({"SampleID": ["S1", "S2"], "Measurement": [1.5, 2.5]})
        x, y = _auto_detect_columns(df)
        assert x == "SampleID"
        assert y == "Measurement"

    def test_no_categorical_cols(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0]})
        x, y = _auto_detect_columns(df)
        assert y is not None
        # x may be None since no cat cols exist

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        x, y = _auto_detect_columns(df)
        assert x is None
        assert y is None

    def test_mixed_case_matches(self):
        df = pd.DataFrame({"group": ["A", "B"], "VALUE": [1, 2]})
        x, y = _auto_detect_columns(df)
        assert x == "group"
        assert y == "VALUE"

    def test_fold_change_variants(self):
        df = pd.DataFrame({"Condition": ["X", "Y"], "FoldChange": [2.0, 0.5]})
        x, y = _auto_detect_columns(df)
        assert y == "FoldChange"

        df2 = pd.DataFrame({"Condition": ["X", "Y"], "fold_change": [2.0, 0.5]})
        x2, y2 = _auto_detect_columns(df2)
        assert y2 == "fold_change"

    def test_multiple_numeric_cols_picks_first_known(self):
        df = pd.DataFrame({"Group": ["A", "B"], "Expression": [1, 2], "Score": [3, 4]})
        x, y = _auto_detect_columns(df)
        assert y == "Expression"


class TestResolveFrame:
    def test_dataframe_auto_detect(self):
        df = pd.DataFrame({"Group": ["Con", "KO"], "Value": [100, 200]})
        vals, grps = _resolve_frame(df)
        assert list(vals) == [100, 200]
        assert list(grps) == ["Con", "KO"]

    def test_explicit_x_y(self):
        df = pd.DataFrame({"g": ["A", "B"], "v": [1, 2], "extra": [3, 4]})
        vals, grps = _resolve_frame(df, x_col="g", y_col="v")
        assert list(vals) == [1, 2]
        assert list(grps) == ["A", "B"]

    def test_non_dataframe_passthrough(self):
        vals, grps = _resolve_frame([10, 20])
        assert vals == [10, 20]
        assert grps is None

    def test_explicit_x_only(self):
        df = pd.DataFrame({"g": ["A", "B"], "v": [1, 2]})
        vals, grps = _resolve_frame(df, x_col="g")
        assert list(grps) == ["A", "B"]
        # values defaults to the full DataFrame when y is None

    def test_explicit_y_only(self):
        df = pd.DataFrame({"g": ["A", "B"], "v": [1, 2]})
        vals, grps = _resolve_frame(df, y_col="v")
        assert list(vals) == [1, 2]
