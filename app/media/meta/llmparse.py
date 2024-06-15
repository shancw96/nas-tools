import logging
from typing import Any

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = """You will now play an function to reformat video title. Your task is to extract metadata from 
unstructured text content and compose it as a new string with connector `-`. your output format is: {title}-{
season}-{episode}-{year}-{edition}-{videoFormat}-{videoCodec}.{filesuffix} If some metadata missed, just skip it, 
Dont fake something you dont know, dont reply useless word, follow output format carefully! \n the valid metadata 
list below : {title}：(the video title){season}：(if video is tv, it has season number, like S1/S2/S3){episode}：(if 
video is tv, it has episode number, like E1/E2/E3){year}： (the video published year){edition}：(Bluray/WEB-DL/...) {
videoFormat}：(1080p/4k/...){videoCodec}：(AV1/... ){filesuffix}: (mp4, mkv....) \n Example: input: "【喵萌奶茶屋】★04月新番★[
夏日重现/Summer Time Rendering][S01E11][1080p][繁日双语][招募翻译]-2023-Bluray" desc: valid information is:  title: 夏日重现， year: 
2023, edition: Bluray, season: 01, episode:11。the other part is ignored. output: 夏日重现-S01E11-2023-Bluray \n input: 
"汉尼拔.H265.1080P.SE03.13.2015.mkv" desc: valid information is: title: 汉尼拔 year: 2015, season: 03, episode: 13, 
videoFormat:1080P, filesuffix: mkv,  videocCodec: H265 the other part is ignored. output: 
汉尼拔-S03E13-2015-1080P-H265.mkv"""


class OpenAIParser:
    def __init__(
        self,
        api_key: str,
        api_base: str = "https://api.openai.com/v1",
        model: str = "gpt-3.5-turbo",
        **kwargs,
    ) -> None:
        """OpenAIParser is a class to parse text with openai

        Args:
            api_key (str): the OpenAI api key
            api_base (str):
                the OpenAI api base url, you can use custom url here. \
                Defaults to "https://api.openai.com/v1".
            model (str):
                the ChatGPT model parameter, you can get more details from \
                https://platform.openai.com/docs/api-reference/chat/create. \
                Defaults to "gpt-3.5-turbo".
            kwargs (dict):
                the OpenAI ChatGPT parameters, you can get more details from \
                https://platform.openai.com/docs/api-reference/chat/create.

        Raises:
            ValueError: if api_key is not provided.
        """
        if not api_key:
            raise ValueError("API key is required.")

        self._api_key = api_key
        self.api_base = api_base
        self.model = model
        self.openai_kwargs = kwargs

    def parse(
        self, text: str, prompt: str | None = None
    ) -> ChatCompletionMessage:
        """parse text with openai

        Args:
            text (str): the text to be parsed
            prompt (str | None, optional):
                the custom prompt. Built-in prompt will be used if no prompt is provided. \
                Defaults to None.
            asdict (bool, optional):
                whether to return the result as dict or not. \
                Defaults to True.

        Returns:
            dict | str: the parsed result.
        """
        if not prompt:
            prompt = DEFAULT_PROMPT

        params = self._prepare_params(text, prompt)

        client = OpenAI(
            api_key=self._api_key,
            base_url=self.api_base,
        )

        completion = client.chat.completions.create(**params)
        return completion.choices[0].message

    def _prepare_params(self, text: str, prompt: str) -> dict[str, Any]:
        """_prepare_params is a helper function to prepare params for openai library.
        There are some differences between openai and azure openai api, so we need to
        prepare params for them.

        Args:
            text (str): the text to be parsed
            prompt (str): the custom prompt

        Returns:
            dict[str, Any]: the prepared key value pairs.
        """
        params = dict(
            messages=[
                dict(role="system", content=prompt),
                dict(role="user", content=text),
            ],
            model=self.model,
            # set temperature to 0 to make results be more stable and reproducible.
            temperature=0,
        )
        return params