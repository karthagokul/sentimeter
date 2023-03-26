import text2emotion as te
import json
import openai


class Basebackend:
    def __init__(self, backend_name) -> None:
        self.backend_name = backend_name

    def process(self, text):
        return {}


class LocalBackend(Basebackend):
    def __init__(self) -> None:
        super().__init__("Local")

    def process(self, text):
        data = {}
        data = te.get_emotion(text)
        return data


class AIRemoteBackend(Basebackend):
    def __init__(self, OPENAI_KEY) -> None:
        super().__init__("ChatGPT")
        self.openai = openai
        self.openai.api_key = OPENAI_KEY
        # Set up the model and prompt
        self.model_engine = "text-davinci-003"
        self.prompt = """
        can you identify the levels of Happy, Sad , Fear, Angry and Surprise in the
         following test and share the result as json format?
        """

    def extract_valid_json(self, output):
        res = output[output.index("{") : output.index("}") + 1]
        return res

    def process(self, text):
        data = {}
        prompt_with_input = self.prompt + text
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt_with_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # print("chat GPT Results")
        result = completion.choices[0].text
        result = result.replace("\n", " ")
        # print(result)
        json_string = self.extract_valid_json(result)
        try:
            data = json.loads(json_string)
        except ValueError:
            data = {}
        return data
