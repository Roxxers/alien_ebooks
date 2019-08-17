from markovify import Text


class ListText(Text):
    """
    """
    def sentence_split(self, text):
        return list(text)