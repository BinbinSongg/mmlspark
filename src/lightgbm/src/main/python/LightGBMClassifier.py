# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.

import sys
from pyspark import SQLContext
from pyspark import SparkContext

if sys.version >= '3':
    basestring = str

from mmlspark._LightGBMClassifier import _LightGBMClassifier
from mmlspark._LightGBMClassifier import _LightGBMClassificationModel
from pyspark import SparkContext
from pyspark.ml.common import inherit_doc
from pyspark.ml.wrapper import JavaParams

@inherit_doc
class LightGBMClassifier(_LightGBMClassifier):
    def _create_model(self, java_model):
        model = LightGBMClassificationModel()
        model._java_obj = java_model
        model._transfer_params_from_java()
        return model

@inherit_doc
class LightGBMClassificationModel(_LightGBMClassificationModel):
    def saveNativeModel(self, filename, overwrite=True):
        """
        Save the booster as string format to a local or WASB remote location.
        """
        self._java_obj.saveNativeModel(filename, overwrite)

    @staticmethod
    def loadNativeModelFromFile(filename, labelColName="label",
                                featuresColName="features", predictionColName="prediction",
                                probColName="probability", rawPredictionColName="rawPrediction"):
        """
        Load the model from a native LightGBM text file.
        """
        ctx = SparkContext._active_spark_context
        loader = ctx._jvm.com.microsoft.ml.spark.LightGBMClassificationModel
        java_model = loader.loadNativeModelFromFile(filename, labelColName,
                                                    featuresColName, predictionColName,
                                                    probColName, rawPredictionColName)
        return JavaParams._from_java(java_model)

    @staticmethod
    def loadNativeModelFromString(model, labelColName="label",
                                  featuresColName="features", predictionColName="prediction",
                                  probColName="probability", rawPredictionColName="rawPrediction"):
        """
        Load the model from a native LightGBM model string.
        """
        ctx = SparkContext._active_spark_context
        loader = ctx._jvm.com.microsoft.ml.spark.LightGBMClassificationModel
        java_model = loader.loadNativeModelFromString(model, labelColName,
                                                      featuresColName, predictionColName,
                                                      probColName, rawPredictionColName)
        return JavaParams._from_java(java_model)

    def getFeatureImportances(self, importance_type="split"):
        """
        Get the feature importances.  The importance_type can be "split" or "gain".
        """
        return self._java_obj.getFeatureImportances(importance_type)
