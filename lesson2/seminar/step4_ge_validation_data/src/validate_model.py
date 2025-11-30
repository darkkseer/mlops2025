import json
import sys
import yaml


def validate_model():
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    
    accuracy_min = params["accuracy_min"]
    
    with open("metrics/metrics.json", "r") as f:
        metrics = json.load(f)
    
    accuracy = metrics["accuracy"]
    
    print(f"Model validation check:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Minimum required: {accuracy_min}")
    
    if accuracy < accuracy_min:
        print(f"Model validation FAILED: Accuracy {accuracy:.4f} < {accuracy_min}")
        sys.exit(1)
    else:
        print(f"Model validation PASSED: Accuracy {accuracy:.4f} >= {accuracy_min}")
        sys.exit(0)

if __name__ == "__main__":
    validate_model()