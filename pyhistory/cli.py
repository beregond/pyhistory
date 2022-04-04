from pathlib import Path

import click

from . import __description__, file_config, pyhistory
from .exceptions import FileNotFound
from .utilities import find_file_across_parents, format_line

LINE_PREFIX = "* "

default_values = file_config.get_defaults_from_config_file_if_exists()

line_length = click.option(
    "--line-length",
    help="Formatted line length.",
    default=default_values.get("line_length", 79),
    show_default=True,
    type=int,
)


@click.group(help=__description__)
@click.pass_context
@click.version_option()
@click.help_option("-h")
@click.option(
    "--history-dir",
    help="History directory location.",
    default=default_values.get("history_dir", "history"),
    show_default=True,
)
@click.option(
    "--history-file",
    help="History file name.",
    default=default_values.get("history_file", "HISTORY.rst"),
    show_default=True,
)
def main(context, history_dir, history_file):
    try:
        history_file = find_file_across_parents(Path.cwd(), history_file)
    except FileNotFound:
        click.echo("Couldn't find history file ({}).".format(history_file))
        context.abort()
    history_dir = history_file.parent / history_dir
    context.obj = {
        "history_dir": history_dir,
        "history_file": history_file,
    }


@main.command()
@click.pass_context
@click.argument("message")
def add(context, message):
    pyhistory.add(message, context.obj["history_dir"])


@main.command()
@click.pass_context
@line_length
def list(context, line_length):
    lines = pyhistory.list_(context.obj["history_dir"])
    formatted_lines = [
        format_line(LINE_PREFIX, line, line_length) for line in lines.values()
    ]
    click.echo("\n" + "".join(formatted_lines))


def _maybe_positive(context, param, value):
    if value is None:
        return None
    if value < 1:
        click.echo('"{}" must be greater or equal to 1.'.format(param.name))
        context.abort()
    else:
        return value


@main.command()
@click.pass_context
@click.argument("version")
@line_length
@click.option(
    "--at-line",
    help="Update file at line. (By default after first headline.)",
    default=default_values.get("at_line"),
    callback=_maybe_positive,
    type=int,
)
@click.option(
    "--date",
    help="Date of update. By default today, but can be arbitrary value.",
)
def update(context, version, at_line, date, line_length):
    pyhistory.update(
        version,
        context.obj["history_dir"],
        context.obj["history_file"],
        at_line,
        date,
        line_length,
        LINE_PREFIX,
    )


@main.command()
@click.pass_context
@click.confirmation_option(prompt="Do you really want to remove all entries?")
def clear(context):
    pyhistory.clear(context.obj["history_dir"])


@main.command()
@click.pass_context
@click.argument("entry", nargs=-1, type=int)
@line_length
def delete(context, entry, line_length):
    entries = entry
    if entries:
        pyhistory.delete(entries, context.obj["history_dir"])
    else:
        files = pyhistory.list_(context.obj["history_dir"])
        click.echo()
        for number, message in files.items():
            prefix = "{}. ".format(number)
            line = format_line(prefix, message, line_length)
            click.echo(line, nl=False)

        click.echo("\n(Delete by choosing entries numbers.)")
