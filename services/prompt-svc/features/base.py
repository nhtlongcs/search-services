
import logging
from abc import ABC, abstractmethod
from typing import List

import openai
import tiktoken


class BaseAPI(ABC):
    """
    Base class for the OpenAI API
    """
    def __init__(self):
        self._model = None 
        self._max_tokens = 4096

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def _num_tokens_from_str(self, text: str):
        """
        Returns the number of tokens in the text
        """
        encoding = tiktoken.encoding_for_model(self._model)
        num_tokens = len(encoding.encode(text))
        return num_tokens

    def _num_tokens(self, messages):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(self._model)
        except KeyError:
            # print("Warning: model not found. Using cl100k_base encoding.")
            logging.warning("model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if self._model == "gpt-3.5-turbo":
            # print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            logging.warning("gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
            # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {self._model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

class InstructionBase(BaseAPI):
    """
    Base class for the OpenAI API Completion


    Creates a completion for the provided prompt and parameters
    """

    def __init__(self):
        super().__init__()
        self._model = "gpt-3.5-turbo"

    def execute(self, instruction: str, content: str, temperature: float = 0) -> str:
        messages = [
                {'role': 'system', 'content': instruction},
                {'role': 'user', 'content': content}
        ]
        assert self._num_tokens(messages) <= self._max_tokens, f"Number of tokens {self._num_tokens(messages)} exceeds maximum {self._max_tokens}"
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=messages,
            temperature=temperature, # deterministic
            stream=True  # faster with stream, for more info see https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
        )

        # create variables to collect the stream of chunks
        collected_chunks = []
        collected_messages = []
        # iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk['choices'][0]['delta']  # extract the message
            collected_messages.append(chunk_message)  # save the message

        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
        return full_reply_content
    