from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
import joblib

from sklearn.preprocessing import OrdinalEncoder, TargetEncoder


@dataclass
class PreprocessingData:
    """Data paths generated by PreprocessingStep.
    Regarding if it's the training or inference pipeline, the correct paths need to be implemented
    (respectively train_path, test_path / batch_path)
    """

    train_path: Optional[Path] = None
    test_path: Optional[Path] = None
    batch_path: Optional[Path] = None


@dataclass
class FeaturesEngineeringEData:
    """Data and encoders paths generated by FeatureEngineeringStep.
    Regarding if it's the training or inference pipeline, the correct paths need to be implemented
    (respectively train_path, test_path / batch_path)"""

    encoders_path: Path
    train_path: Optional[Path] = None
    test_path: Optional[Path] = None
    batch_path: Optional[Path] = None


@dataclass
class FeaturesEncoder:
    """Encoders artifact dumped and loaded during the feature_engineering step."""

    ordinal_encoder: OrdinalEncoder
    target_encoder: TargetEncoder
    base_features: Iterable[str]
    ordinal_features: Iterable[str]
    target_features: Iterable[str]
    target: str

    def to_joblib(self, path: Path) -> None:
        """Dump artifact as a joblib file.

        Args:
            path (Path): Encoders path
        """
        joblib.dump(self, path)
