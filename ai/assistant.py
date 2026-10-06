from .providers import AIProvider


class AIAssistant:

    def __init__(self):
        self.provider = AIProvider()

    def ask(self, message, history=None):

        return self.provider.ask(
            message,
            history
        )

    def voice_calculation(self, message):

        return self.provider.voice_calculation(
            message
        )
