from services.code_generation_service import CodeGenerationService
from services.evaluation_service import EvaluationService
from services.error_analysis_service import ErrorAnalysisService


def main():
    code_service = CodeGenerationService()
    print(code_service.generate_code("Create a REST API using Flask"))

    evaluation_service = EvaluationService()
    print(evaluation_service.evaluate("Sample Python code output"))

    error_service = ErrorAnalysisService()
    print(error_service.analyze_error("IndexError: list index out of range"))


if __name__ == "__main__":
    main()
