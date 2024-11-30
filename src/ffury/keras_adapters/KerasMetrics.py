from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score
)

from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasMetrics:
    def __init__(self) -> None:
        self.f1_average = "macro"

    def __call__(self, y_true, y_pred):
        print()
        print()
        print( y_true.shape )
        print( y_pred.shape )
        print()
        print()

        return f1_score(y_true, 
                        y_pred, 
                        average=self.f1_average)
