# -*- coding: utf-8 -*-
"""Compositions for classifiers."""
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["mloning", "fkiraly"]
__all__ = [
    "ClassifierPipeline",
    "ComposableTimeSeriesForestClassifier",
    "ColumnEnsembleClassifier",
    "SklearnClassifierPipeline",
    "WeightedEnsembleClassifier",
]

from sktime.classification.compose._column_ensemble import ColumnEnsembleClassifier
from sktime.classification.compose._pipeline import (
    ClassifierPipeline,
    SklearnClassifierPipeline,
)

# 0.20.0 - remove this import
from sktime.classification.ensemble import (
    ComposableTimeSeriesForestClassifier,
    WeightedEnsembleClassifier,
)
