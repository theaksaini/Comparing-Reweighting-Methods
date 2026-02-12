import numpy as np
import pandas as pd
import pytest


@pytest.mark.parametrize(
    "y_true,y_pred,expected",
    [
        (np.array([0, 0, 0]), np.array([0.2, 0.4, 0.6]), (0.2 + 0.4 + 0.6) / 3),
        (np.array([1, 1, 1]), np.array([0.0, 1.0, 0.5]), 0.0),
    ],
)
def test_fpr_basic(y_true, y_pred, expected):
    utils = pytest.importorskip("utils")
    assert utils.FPR(y_true, y_pred) == pytest.approx(expected)


@pytest.mark.parametrize(
    "y_true,y_pred,expected",
    [
        (np.array([1, 1, 1]), np.array([0.1, 0.0, 1.0]), (1 - 0.1 + 1 - 0.0 + 1 - 1.0) / 3),
        (np.array([0, 0, 0]), np.array([0.5, 0.4, 0.3]), 0.0),
    ],
)
def test_fnr_basic(y_true, y_pred, expected):
    utils = pytest.importorskip("utils")
    assert utils.FNR(y_true, y_pred) == pytest.approx(expected)


def test_binary_to_decimal():
    utils = pytest.importorskip("utils")
    assert utils.binary_to_decimal([1, 0, 1]) == 5
    assert utils.binary_to_decimal([0, 0, 0, 1]) == 1


def test_front_simple():
    utils = pytest.importorskip("utils")
    obj1 = [1, 2, 3]
    obj2 = [3, 2, 1]
    front = utils.front(obj1, obj2)

    # No point strictly dominates the others; all should be on front
    assert set(front) == {0, 1, 2}


def test_subgroup_FNR_loss_expected_value():
    utils = pytest.importorskip("utils")
    sample_df = pd.DataFrame(
        [
            {"a": 1, "b": 0, "c": 1, "y": 1},
            {"a": 1, "b": 1, "c": 1, "y": 1},
            {"a": 0, "b": 1, "c": 1, "y": 1},
            {"a": 0, "b": 0, "c": 0, "y": 1},
            {"a": 1, "b": 1, "c": 0, "y": 1},
            {"a": 1, "b": 0, "c": 1, "y": 1},
            {"a": 1, "b": 0, "c": 1, "y": 0},
            {"a": 0, "b": 1, "c": 1, "y": 0},
            {"a": 0, "b": 0, "c": 0, "y": 1},
            {"a": 1, "b": 1, "c": 1, "y": 0},
        ],
        columns=["a", "b", "c", "y"],
    )

    # First three columns as features, last as target
    X = sample_df.iloc[:, :-1]
    y = sample_df.iloc[:, -1]
    y_pred = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

    result = utils.subgroup_FNR_loss(X, y, y_pred, sens_features=["a", "b"])
    assert result == pytest.approx(0.042857142857142864, rel=1e-12)
