import asyncio
from sys import implementation
from typing import List

from openai import AsyncOpenAI

from app.drivers.configs.config import Config
from app.interfaces.llm_wrapper import LlmClientWrapper
from app.schemas.GetCompletionReq import GetCompletionReq


class OpenAiLlmWrapper(LlmClientWrapper):
    """
    OpenAI LLM client wrapper for handling requests to OpenAI's API.
    This class manages concurrent requests and provides methods to get completions and execute multiple prompts in parallel.
    """

    client = None  # OpenAI client instance
    active_req = 0
    sem = asyncio.Semaphore(100)  # Limit to 100 concurrent requests

    @staticmethod
    def set_client(api_key: str):
        """
        Set the OpenAI client with the provided API key.
        :param api_key: The API key for OpenAI.
        """
        OpenAiLlmWrapper.client = AsyncOpenAI(api_key=api_key)


    async def get_completion(self, req: GetCompletionReq) -> str:
        if type(self).client is None:
            raise Exception("OpenAI client is not initialized. Please set the API key using set_client method.")

        if type(self).active_req >= 100:
            raise Exception("Too many concurrent requests, please try again later.")

        # print("for req", req.prompt, "active requests:", type(self).active_req)
        async with type(self).sem:
            type(self).active_req += 1
            try:
                response = await type(self).client.chat.completions.create(
                    model=req.model,
                    messages=[ {"role": "user", "content": req.prompt} ],
                    temperature=req.temperature,
                    max_tokens=req.max_tokens,
                )
                print("Completed")
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error in OpenAI request: {e}")
                raise e
            finally:
                type(self).active_req -= 1

    async def execute_multiple_prompts_parallel(self, reqs: List[GetCompletionReq]) -> List[str]:
        """
        Execute multiple prompts in parallel using asyncio.gather.
        :param reqs: List of GetCompletionReq objects.
        :return: List of responses from OpenAI.
        """
        tasks = [self.get_completion(req) for req in reqs]
        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    import asyncio
    from app.schemas.GetCompletionReq import GetCompletionReq

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
