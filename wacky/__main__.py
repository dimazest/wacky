import codecs
import json
import sys
import gzip

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
@click.option('--index', default=None, type=click.Path(exists=True))
@click.option('--min-count', default=None, type=int)
def sentences(token_template, index, min_count):
    token_index = dict()
    with gzip.open(index, mode='rt') as f:
        for i, line in enumerate(f, start=1):
            item, count = line.rsplit(' ', maxsplit=1)
            count = int(count)

            if min_count is not None and count < min_count:
                i = -i

            token_index[item] = str(i)

    for raw_document in readers.raw_documents(sys.stdin):
        for tokens in readers.sentences(raw_document):
            if index:
                print(' '.join(token_index[token_template.format(**t)] for t in tokens))
            elif token_template is None:
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

    counter.update(w[:-1] for w in sys.stdin)

    for item, count in counter.most_common(most_common):
        print(item, count)


def read_counts(input_):
    from collections import Counter
    counter = Counter()

    for line in sys.stdin:
        item, count = line.rsplit(' ', maxsplit=1)
        count = int(count.strip())

        counter[item] += count

    return counter


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--most-common', default=None, type=int)
def merge(files, most_common):
    counter = read_counts(sys.stdin)

    for item, count in counter.most_common(most_common):
        print(item, count)
