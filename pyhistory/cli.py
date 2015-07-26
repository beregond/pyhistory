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
@click.option('--history-dir', help='History directory location.')
@click.option('--history-file', help='History file name.')
def cli(context, history_dir, history_file):
    history_dir = history_dir or 'history'
    history_dir = Path.cwd() / history_dir
    history_file = history_file or 'HISTORY.rst'
    history_file = history_dir.parent / history_file
    context.obj = {
        'history_dir': history_dir,
        'history_file': history_file,
    }


@cli.command()
@click.pass_context
@click.argument('message')
def add(context, message):
    pyhistory.add(message, context.obj['history_dir'])


@cli.command()
@click.pass_context
@line_length
def list(context, line_length):
    pyhistory.list_history(context.obj['history_dir'], line_length)


@cli.command()
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


@cli.command()
@click.pass_context
def clear(context):
    pyhistory.clear(context.obj['history_dir'])


@cli.command()
@click.pass_context
@click.argument('entry', nargs=-1)
@line_length
def delete(context, entry, line_length):
    entries = entry
    pyhistory.delete(entries, context.obj['history_dir'], line_length)
