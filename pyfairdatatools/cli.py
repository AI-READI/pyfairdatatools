"""A sample CLI."""

import click
from art import tprint

# import log


# from . import utils


# @click.command()
# @click.argument("feet")
# def cli(feet: str):
#     log.init()

#     meters = utils.feet_to_meters(feet)

#     if meters is not None:
#         click.echo(meters)


@click.command()
def main():
    """CLI entrypoint."""
    tprint("Pyfairdatatools")

    click.echo("Refer to the documentation for usage instructions.")
    click.echo("https://aireadi.github.io/pyfairdatatools/")


if __name__ == "__main__":  # pragma: no cover
    main()  # pylint: disable=no-value-for-parameter
