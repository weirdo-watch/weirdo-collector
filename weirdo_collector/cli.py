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
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    envvar="WEIRDO_CONFIG",
    help="Location of configugration file",
)
@click.option(
    "--base-dir",
    "-b",
    type=click.Path(exists=True),
    envvar="WEIRDO_DIR",
    help="Base weirdo directory",
)
@click.pass_context
def main(ctx, verbose: bool, config: str, base_dir: str) -> None:
    """
    weirdo-collector collects the social media postings of your favorite weirdos.
    """
    ctx.obj = {"verbose": verbose, "config_file": config, "base_dir": base_dir}


@main.command()
@click.option("--user", "-u", type=str, help="Optional, specific user to collect")
@click.pass_context
def collect(ctx, user: str):
    """
    Collect data about your favorite weirdo and store it.
    """
    # try:
    app = App(
        ctx.obj.get("base_dir"),
        verbose=ctx.obj.get("verbose"),
        config_file=ctx.obj.get("config_file"),
    )
    app.get_em()
    # except Exception as e:
    # click.echo(
    #     "Collection failed... proper troubleshooting steps might appear one day: {}".format(e)
    # )


if __name__ == "__main__":
    main()
