from contextlib import asynccontextmanager

@asynccontextmanager
async def get_file_parser():
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    try:
        yield file_parser
    finally:
        print("Cleaning up resources in get_file_parser")


@asynccontextmanager
async def get_hiring_manager():
    from app.repos.llm_wrapper.llm_openai_impl import OpenAiLlmWrapper
    from app.repos.hiring_processor.hiring_processor_impl import HiringProcessorImpl
    from app.repos.prompt_exec.prompt_processor import PromptProcessorImpl
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    prompt_processor = PromptProcessorImpl()
    llm_client = OpenAiLlmWrapper()
    hiring_processor = HiringProcessorImpl(file_parser, prompt_processor, llm_client)
    try:
        yield hiring_processor
    finally:
        print("Cleaning up resources in get_hiring_manager")


