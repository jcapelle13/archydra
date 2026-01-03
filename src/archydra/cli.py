import click

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    click.echo("This isn't ready yet!")

if __name__ == "__main__":
    cli()