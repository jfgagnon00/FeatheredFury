import os
import pandas as pd

from datetime import datetime
from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.report import Report
from evidently.metric_preset import (
    DataDriftPreset,
    DataQualityPreset,
)
from evidently import metrics


from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

iris = load_iris()

data=pd.DataFrame({
    'sepal length':iris.data[:,0],
    'sepal width':iris.data[:,1],
    'petal length':iris.data[:,2],
    'petal width':iris.data[:,3],
    'species':iris.target
})

X=data[['sepal length', 'sepal width', 'petal length', 'petal width']]
y=data['species']

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

ws = CloudWorkspace(
    token=os.getenv("EVIDENTLY_API_TOKEN"),
    url="https://app.evidently.cloud")

project = ws.get_project(project_id=os.getenv("EVIDENTLY_PROJECT_ID"))
print(type(project))

if False:
    # snapshot est comme une collection de test suite et metrics
    # pas tout a fait ce que ke veux
    project.add_snapshot()

if False:
    # ca log un rapport tout seul qui ne semble pas lier a aucune donnee (autre que celle du rapport)
    # pas tout a fait ce qu'on cherche
    data_report = Report(
        metrics=[
            DataDriftPreset(stattest="psi", stattest_threshold="0.3"),
            DataQualityPreset(),
        ],
        timestamp=datetime.now()
    )
    data_report.run(reference_data=X_train, current_data=X_test)

    ws.add_report(project_id=os.getenv("EVIDENTLY_PROJECT_ID"),
                report=data_report)

