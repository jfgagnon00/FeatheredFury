from evidently import ColumnMapping
from evidently.metrics.data_drift.embedding_drift_methods import (
    model, 
    distance, 
    ratio, 
    mmd
)
from evidently.test_suite import TestSuite
from evidently.tests import TestEmbeddingsDrift
from evidently.ui.workspace.cloud import CloudWorkspace
from ffury.configs import EvidentlyConfig
from ffury.misc.logging import (
    create_logger,
    pretty_format
)
from pandas import DataFrame


def test_embeddings_drift(reference: DataFrame,
                          data: DataFrame,
                          config: EvidentlyConfig) -> bool:
    logger = create_logger(file=__file__)

    logger.info(f"Reference shape: {reference.shape}")
    logger.info(f"Data shape: {data.shape}")

    column_mapping = ColumnMapping(embeddings={
        "classification_embeddings": reference.columns
    })
    test_suite = TestSuite(tests=[
        TestEmbeddingsDrift(
            embeddings_name="classification_embeddings", 
            drift_method=model(threshold=config.threshold,
                               quantile_probability=config.quantile_probability,
                               pca_components=config.pca_components)
        )
    ])

    logger.info("Running test")
    test_suite.run(reference_data=reference, 
              current_data=data, 
              column_mapping=column_mapping)

    logger.info("Resultat")
    results = test_suite.as_dict()
    message = pretty_format(results)
    logger.info(message)

    logger.info(f"Log test sur Evidently")
    ws = CloudWorkspace(token=config.api_token, url=config.url)
    ws.add_test_suite(project_id=config.project_id, test_suite=test_suite)

    return results["tests"][0]["status"] != "FAIL"
