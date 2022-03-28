# stdlib
from typing import Callable

# third party
import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_diabetes, load_iris

# synthcity absolute
from synthcity.metrics.performance import (
    evaluate_test_performance_linear,
    evaluate_test_performance_mlp,
    evaluate_test_performance_xgb,
)
from synthcity.plugins import Plugin, Plugins


@pytest.mark.parametrize("test_plugin", [Plugins().get("marginal_distributions")])
@pytest.mark.parametrize(
    "evaluator",
    [
        evaluate_test_performance_xgb,
        evaluate_test_performance_linear,
        evaluate_test_performance_mlp,
    ],
)
def test_evaluate_performance_classifier(
    test_plugin: Plugin, evaluator: Callable
) -> None:
    X, y = load_iris(return_X_y=True, as_frame=True)
    X["target"] = y

    test_plugin.fit(X)
    X_gen = test_plugin.generate(100)

    good_score = evaluator(
        X,
        X_gen,
    )

    assert np.abs(good_score) < 1

    sz = 100
    X_rnd = pd.DataFrame(np.random.randn(sz, len(X.columns)), columns=X.columns)
    score = evaluator(
        X,
        X_rnd,
    )

    assert np.abs(good_score) < 1
    assert score > good_score


@pytest.mark.parametrize("test_plugin", [Plugins().get("marginal_distributions")])
@pytest.mark.parametrize(
    "evaluator",
    [
        evaluate_test_performance_xgb,
        evaluate_test_performance_linear,
        evaluate_test_performance_mlp,
    ],
)
def test_evaluate_performance_regression(
    test_plugin: Plugin, evaluator: Callable
) -> None:
    X, y = load_diabetes(return_X_y=True, as_frame=True)
    X["target"] = y

    test_plugin.fit(X)
    X_gen = test_plugin.generate(100)

    good_score = evaluator(
        X,
        X_gen,
    )

    assert np.abs(good_score) < 1

    sz = 100
    X_rnd = pd.DataFrame(np.random.randn(sz, len(X.columns)), columns=X.columns)
    score = evaluator(
        X,
        X_rnd,
    )

    assert np.abs(good_score) < 1
    assert score > good_score
