from collections import namedtuple
from itertools import takewhile


def raw_documents(fileobject):

    stripped_lines = (l.rstrip() for l in fileobject)

    lines = (
        l for l in stripped_lines
        if not l.startswith('<text') and l != '<s>'
    )

    while True:
        raw_document = list(takewhile(lambda l: l != '</text>', lines))

        if not raw_document:
            break

        yield raw_document


def raw_sentences(document):
    document = iter(document)

    while True:
        sentence = list(takewhile(lambda l: l != '</s>', document))

        if not sentence:
            break

        yield sentence


Token = namedtuple('Token', 'word, lemma, tag, feats, head, rel')


def tokens(raw_sentence):
    for raw_token in raw_sentence:
        yield Token(*raw_token.split('\t'))._asdict()


def sentences(raw_document):
    for raw_sentence in raw_sentences(raw_document):
        yield list(tokens(raw_sentence))


def documents(raw_documents):
    for raw_document in raw_documents:
        yield {
            'document_id': '...',
            'sentences': list(sentences(raw_document)),
        }
