import click

from weirdo_collector.app import App


@click.group()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    envvar="WEIRDO_VERBOSE",
    help="Provide verbose output",
)
@click.pass_context
def main(ctx, verbose: bool) -> None:
    """
    weirdo-collector collects the social media postings of your favorite weirdos.
    """
    ctx.obj = {
        "verbose": verbose,
    }


@main.command()
@click.option("--user", "-u", type=str, help="Optional, specific user to collect")
@click.pass_context
def collect(ctx, user: str):
    """
    Collect data about your favorite weirdo and store it.
    """
    try:
        app = App("weirdos", verbose=ctx.obj["verbose"])
        app.get_em()
    except Exception:
        click.echo(
            "Collection failed... proper troubleshooting steps might appear one day"
        )


if __name__ == "__main__":
    main()
