
def get_file_parser():
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    return file_parser



def get_evaluator_engine():
    from app.repos.llm_wrapper.llm_openai_impl import OpenAiLlmWrapper
    from app.repos.hiring_processor.hiring_processor_impl import EvaluatorEngineImpl
    from app.repos.prompt_exec.prompt_processor import PromptProcessorImpl
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    prompt_processor = PromptProcessorImpl()
    llm_client = OpenAiLlmWrapper()
    evaluator = EvaluatorEngineImpl(file_parser, prompt_processor, llm_client)
    return evaluator

