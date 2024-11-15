import neptune
import os
import pickle
from pprint import pprint

api_token = os.environ["NEPTUNE_API_TOKEN"]

if len(api_token) == 0:
    print("NEPTUNE_API_TOKEN non defini")
    exit(1)

run = neptune.init_run(
    project="FeatheredFury/FeatheredFury",
    capture_hardware_metrics=False,
    api_token=api_token,
)

# afficher les membres de run
pprint( dir(run) )

# simuler data binaire
my_model = [0, 1, 2, 3, 4]
with open("model.pkl", "wb") as f:
    pickle.dump(my_model, f)

# envoyer le binaire du modele sur neptune.ai
run["model_checkpoints/my_model"].upload("model.pkl")

run.stop()