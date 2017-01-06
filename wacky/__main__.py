import codecs
import json
import sys

import click

from . import readers


@click.group()
def cli():
    pass


@cli.command()
@click.option('--token-template', default=None, help='The template to render tokens. Available fields are: {word}, {lemma}, {tag}, {feats}, {head} and {rel}.')
def tokens(token_template):
    for raw_document in readers.raw_documents(sys.stdin):
        for raw_sentence in readers.raw_sentences(raw_document):
            for token in readers.tokens(raw_sentence):
                if token_template is None:
                    print(json.dumps(token))
                else:
                    print(token_template.format(**token))


@cli.command()
@click.option('--token-template', default=None, help='The template to render tokens. Available fields are: word, lemma, tag, feats, head and rel.')
def sentences(token_template):
    for raw_document in readers.raw_documents(sys.stdin):
        for tokens in readers.sentences(raw_document):

            if token_template is None:
                print(json.dumps(tokens))
            else:
                print(' '.join(token_template.format(**t) for t in tokens))


@cli.command()
def documents():
    for document in readers.documents(readers.raw_documents(sys.stdin)):
        print(json.dumps(document))

@cli.command()
@click.option('--most-common', default=None, type=int)
def count(most_common):
    from collections import Counter

    counter = Counter()

    counter.update(w[:-1]for w in sys.stdin)

    for item, count in counter.most_common(most_common):
        print(item, count)
