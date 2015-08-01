from pathlib import Path

import click

from . import pyhistory, __description__
from .utilities import find_file_across_parents, format_line


LINE_PREFIX = '* '

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
    history_file = find_file_across_parents(Path.cwd(),  history_file)
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
    lines = pyhistory.list_history(context.obj['history_dir'])
    formatted_lines = [
        format_line(LINE_PREFIX, line, line_length)
        for line
        in lines
    ]
    click.echo('\n' + ''.join(formatted_lines))


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
        LINE_PREFIX,
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
    if entries:
        pyhistory.delete(entries, context.obj['history_dir'])
    else:
        files = pyhistory.list_for_delete(context.obj['history_dir'])
        click.echo()
        for number, file in files.items():
            prefix = '{}. '.format(number)
            with file.open() as src:
                line = format_line(prefix, src.read(), line_length)
            click.echo(line, nl=False)

        click.echo('\n(Delete by choosing entries numbers.)')
