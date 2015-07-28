from pathlib import Path

import click

from . import pyhistory, __description__

global_options = {}

line_length = click.option(
    '--line-length',
    help='Formatted line length.',
    default=79,
    show_default=True,
)


@click.group(help=__description__)
@click.pass_context
@click.version_option()
@click.help_option('-h')
@click.option(
    '--history-dir',
    help='History directory location.',
    default='history',
    show_default=True,
)
@click.option(
    '--history-file',
    help='History file name.',
    default='HISTORY.rst',
    show_default=True,
)
def main(context, history_dir, history_file):
    history_file = _find_across_path(Path.cwd(),  history_file)
    history_dir = history_file.parent / history_dir
    context.obj = {
        'history_dir': history_dir,
        'history_file': history_file,
    }


@main.command()
@click.pass_context
@click.argument('message')
def add(context, message):
    pyhistory.add(message, context.obj['history_dir'])


@main.command()
@click.pass_context
@line_length
def list(context, line_length):
    pyhistory.list_history(context.obj['history_dir'], line_length)


@main.command()
@click.pass_context
@click.argument('version')
@line_length
@click.option(
    '--at-line',
    help='Update file at line. (By default after first headline.)',
)
@click.option('--date', help='Date of update.')
def update(context, version, at_line, date, line_length):
    pyhistory.update(
        context.obj['history_dir'],
        context.obj['history_file'],
        version,
        at_line,
        date,
        line_length,
    )


@main.command()
@click.pass_context
@click.confirmation_option(prompt="Do you really want to remove all entries?")
def clear(context):
    pyhistory.clear(context.obj['history_dir'])


@main.command()
@click.pass_context
@click.argument('entry', nargs=-1, type=int)
@line_length
def delete(context, entry, line_length):
    entries = entry
    pyhistory.delete(entries, context.obj['history_dir'], line_length)


def _find_across_path(dir, file):
    wanted = dir / file
    while not wanted.exists() and wanted.parent != wanted.parent.parent:
        wanted = wanted.parent.parent / wanted.name

    if not wanted.exists():
        raise RuntimeError('History file not found!', file)

    return wanted
