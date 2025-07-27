import asyncio
import hashlib
from typing import List, Text

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.drivers.cache.redis import RedisCache
from app.drivers.configs.config import Config
from app.interfaces.llm_wrapper import LlmClientWrapper
from app.schemas.get_completion_reqs import GetCompletionReq


class OpenAiLlmWrapper(LlmClientWrapper):
    """
    OpenAI LLM client wrapper for handling asynchronous requests to OpenAI's API.
    Supports concurrent prompt execution, response caching, and parallel processing of multiple prompts.
    Provides methods for retrieving completions and managing request limits.
    """
    client = None  # OpenAI client instance
    cl = None
    active_req = 0
    sem = asyncio.Semaphore(100)

    @staticmethod
    def set_client(api_key: str):
        OpenAiLlmWrapper.client = AsyncOpenAI(api_key=api_key)

    def __init__(self, rediscache:RedisCache):
        if OpenAiLlmWrapper.client is None:
            raise Exception("OpenAI client is not initialized. Please set the API key using set_client method.")
        self.rediscache = rediscache

    async def get_completion(self, req: GetCompletionReq, text_format:BaseModel) -> any:
        """
        Asynchronously retrieves a completion from OpenAI's API based on the provided request.
        Utilizes Redis for caching responses to reduce API calls and improve performance.
        Handles concurrent requests with a semaphore to limit the number of active requests.
        Raises exceptions for API errors, caching issues, or parsing errors.
        :param req:
        :param text_format:
        :return:
        """

        if type(self).client is None:
            raise Exception("OpenAI client is not initialized. Please set the API key using set_client method.")

        if type(self).active_req >= 100:
            raise Exception("Too many concurrent requests, please try again later.")

        # print("for req", req.prompt, "active requests:", type(self).active_req)
        cache_key = self._generate_redis_key(req.prompt, text_format)
        cached_response = await self.rediscache.get(cache_key)
        if cached_response:
            if isinstance(cached_response, Exception):
                print(f"Cached response is an error: {cached_response}")
                raise cached_response
            try:
                criteria = text_format.model_validate_json(cached_response)
            except Exception as e:
                print(f"Error parsing cached response: {e}")
                raise e
            return criteria

        async with type(self).sem:
            type(self).active_req += 1
            try:
                response = await type(self).client.responses.parse(
                    model=req.model,
                    input=[{"role": "user", "content": req.prompt}],
                    text_format =text_format
                )

                if isinstance(response, Exception):
                    print(f"Error in OpenAI response: {response}")
                    raise response

                criteria = response.output_parsed
                if not criteria:
                    raise ValueError("No criteria extracted from OpenAI response.")

                criteria_json = criteria.json() if hasattr(criteria, "json") else str(criteria)
                await self.rediscache.set(cache_key, criteria_json, 3600)  # Cache for 1 hour

                return criteria
            except Exception as e:
                print(f"Error in OpenAI request: {e}")
                raise e
            finally:
                type(self).active_req -= 1

    async def execute_multiple_prompts_parallel(self, reqs: List[GetCompletionReq], text_format:type = Text) -> List[any]:
        """
        Asynchronously executes multiple prompts in parallel using OpenAI's API.
        Each request is processed concurrently, and results are returned as a list.
        Utilizes a semaphore to limit the number of concurrent requests and manages caching for efficiency.
        :param reqs:
        :param text_format:
        :return:
        """

        tasks = [self.get_completion(req, text_format) for req in reqs]
        return await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    def _generate_redis_key(prompt:str, resp_format:BaseModel)->str:
        """
        Generates a unique Redis key for caching OpenAI responses based on the prompt and response format.
        The key is created by normalizing the prompt and response format, then hashing the resulting string
        :param prompt:
        :param resp_format:
        :return:
        """
        normalized_prompt = prompt.strip().lower()
        type_representation = repr(resp_format)
        key_string = f"openai:{normalized_prompt}:{type_representation}"
        hashed_key = hashlib.sha256(key_string.encode('utf-8')).hexdigest()
        return f"openai:{hashed_key}"


if __name__ == "__main__":
    import asyncio
    from app.schemas.get_completion_reqs import GetCompletionReq

    async def main():
        Config.init_config()  # Initialize configuration
        wrapper = OpenAiLlmWrapper()
        wrapper.set_client(Config.OPEN_AI_API_KEY)
        req = GetCompletionReq(model="gpt-3.5-turbo", prompt="Hello! Please tell me a joke", max_tokens=50)
        req2 = GetCompletionReq(model="gpt-3.5-turbo", prompt="Name a random country and its capital?", max_tokens=50)
        req3 = GetCompletionReq(model="gpt-3.5-turbo", prompt="what would you say is better a bmw 7 series or an audi a8", max_tokens=100)
        response = await wrapper.execute_multiple_prompts_parallel([req, req2, req3])
        print(response)

    asyncio.run(main())
