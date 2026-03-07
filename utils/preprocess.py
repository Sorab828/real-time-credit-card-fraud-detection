import numpy as np

# expected number of features
EXPECTED_FEATURES = 30


def preprocess_features(features):
    """
    Prepare input features for prediction
    """

    # check length
    if len(features) != EXPECTED_FEATURES:
        raise ValueError(f"Expected {EXPECTED_FEATURES} features")

    # convert to float
    processed = [float(x) for x in features]

    # convert to numpy array
    processed = np.array(processed)

    return processed