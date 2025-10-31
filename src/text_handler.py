import re

class TextHandler:

    def search_pattern(self,pattern: str, text: str) -> list:
        result = re.findall(pattern, text)
        if result:
            return result
        print('Pattern did not match any text In search')
        return []

    def replace_pattern(self, pattern: str, text: str) -> str:
        result = re.sub(pattern, '', text)
        if result:
            return result
        print('Pattern did not match any text in replace')
        return text


textHandler = TextHandler()