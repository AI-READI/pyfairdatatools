"""A sample CLI."""

import click
# import log

from art import tprint

# from . import utils


# @click.command()
# @click.argument("feet")
# def cli(feet: str):
#     log.init()

#     meters = utils.feet_to_meters(feet)

#     if meters is not None:
#         click.echo(meters)


def main():
    """CLI entrypoint."""
    tprint("Fair Data Tools")

    click.echo("Refer to the documentation for usage instructions.")
    click.echo("https://fairdatatools.github.io/fairdatatools/")

    return None


if __name__ == "__main__":  # pragma: no cover
    main()  # pylint: disable=no-value-for-parameter
