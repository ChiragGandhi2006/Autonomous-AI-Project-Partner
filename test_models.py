from models.intent_classifier import IntentClassifier
from models.project_type_detector import ProjectTypeDetector

intent_model = IntentClassifier()
project_model = ProjectTypeDetector()

print(intent_model.classify("Create a Flask API"))
print(project_model.detect("Build a machine learning model using Python"))
