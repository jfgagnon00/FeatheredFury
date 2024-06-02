import neptune
import os

api_token = os.environ["NEPTUNE_API_TOKEN"]

if len(api_token) == 0:
    print("NEPTUNE_API_TOKEN non defini")
    exit(1)

run = neptune.init_run(
    project="FeatheredFury/FeatheredFury",
    api_token=api_token,
)

params = {
    "learning_rate": 0.001, 
    "optimizer": "Adam"
}

run["parameters"] = params

for epoch in range(10):
    run["train/loss"].append(0.9 ** epoch)

run["eval/f1_score"] = 0.66

run.stop()