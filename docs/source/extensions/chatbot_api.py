from docutils import nodes
from docutils.parsers.rst import Directive


class ChatbotDirective(Directive):
    def run(self):
        iframe = '<iframe src="/chatbot" width="100%" height="500px"></iframe>'
        paragraph_node = nodes.raw('', iframe, format='html')
        return [paragraph_node]


def setup(app):
    app.add_directive("chatbot", ChatbotDirective)
