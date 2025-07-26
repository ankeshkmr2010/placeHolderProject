from app.interfaces.evaluator_engine import EvaluatorEngine
from app.interfaces.file_parser import Fileparser


def get_file_parser()-> Fileparser:
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    return file_parser



def get_evaluator_engine()-> EvaluatorEngine:
    from app.repos.llm_wrapper.llm_openai_impl import OpenAiLlmWrapper
    from app.repos.evaluator_engine.evaluator_engine import EvaluatorEngineImpl
    from app.repos.prompt_exec.prompt_processor import PromptProcessorImpl
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    prompt_processor = PromptProcessorImpl()
    llm_client = OpenAiLlmWrapper()
    evaluator = EvaluatorEngineImpl(file_parser, prompt_processor, llm_client)
    return evaluator

