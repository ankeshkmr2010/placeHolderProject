from contextlib import asynccontextmanager



@asynccontextmanager
async def get_file_parser():
    from app.repos.file_parser.file_parser_impl import FileParserImpl
    file_parser = FileParserImpl()
    try:
        yield file_parser
    finally:
        pass
