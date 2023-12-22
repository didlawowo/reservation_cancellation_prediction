# ML Pipeline using AWS and Airflow: https://aws.amazon.com/fr/blogs/machine-learning/build-end-to-end-machine-learning-workflows-with-amazon-sagemaker-and-apache-airflow/
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from steps.preprocess_step import PreprocessStep
from steps.train_step import TrainStep
from steps.condition_step import ConditionStep
from steps.feature_engineering_step import FeatureEngineeringStep
from steps.utils.data_classes import PreprocessingData, FeaturesEngineeringEData
from steps.config import (
    TRAINING_DATA_PATH,
    TrainerConfig,
    ConditionConfig,
    PreprocessConfig,
    FeatureEngineeringConfig,
)

# Preparation
inference_mode = False
preprocessing_data = PreprocessingData(
    train_path=PreprocessConfig.train_path,
    test_path=PreprocessConfig.test_path
)
feature_engineering_data = FeaturesEngineeringEData(
    train_path=FeatureEngineeringConfig.train_path,
    test_path=FeatureEngineeringConfig.test_path,
    encoders_path=FeatureEngineeringConfig.encoders_path,
)
target = FeatureEngineeringConfig.target

# Steps
preprocess_step = PreprocessStep(
    inference_mode=inference_mode, 
    preprocessing_data=preprocessing_data
)
feature_engineering_step = FeatureEngineeringStep(
    inference_mode=inference_mode,
    feature_engineering_data=feature_engineering_data
)
train_step = TrainStep(
    params=TrainerConfig.params
)
condition_step = ConditionStep(
    criteria=ConditionConfig.criteria, 
    metric=ConditionConfig.metric
)

default_args = {
    "owner": "user",
    "depends_on_past": False,
    "retries": 0,
    "catchup": False,
}

with DAG(
    "training-pipeline",
    default_args=default_args,
    start_date=datetime(2023, 12, 19),
    tags=["training"],
    schedule=None,
) as dag:
    preprocessing_task = PythonOperator(
        task_id="preprocessing",
        python_callable=preprocess_step,
        op_kwargs={"data_path": TRAINING_DATA_PATH},
    )
    feature_engineering_task = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering_step,
        op_kwargs={
            "train_path": preprocessing_data.train_path,
            "test_path": preprocessing_data.test_path,
        },
    )
    training_task = PythonOperator(
        task_id="training",
        python_callable=train_step,
        op_kwargs={
            "train_path": feature_engineering_data.train_path,
            "test_path": feature_engineering_data.test_path,
            "target": target
        },
    )
    validation_task = PythonOperator(
        task_id="validation",
        python_callable=condition_step,
        op_kwargs=training_task.output,
    )

    preprocessing_task >> feature_engineering_task >> training_task >> validation_task
