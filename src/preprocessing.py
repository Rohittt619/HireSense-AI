import re


class TextCleaner:

    @staticmethod
    def clean(text):

        text = text.lower()

        text = re.sub(r"\n", " ", text)

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^a-zA-Z0-9+#./ ]", "", text)

        return text.strip()