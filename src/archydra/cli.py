import click
from ruamel.yaml import YAML
from .Consumers import *
from .Producers import *
import asyncio
from .Helpers import Worker

yaml = YAML()

VALID_PRODUCERS = {"FileProducer":FileProducer}

VALID_CONSUMERS = {"ReadWiseConsumer":ReadWiseConsumer,"LoggingConsumer":LoggingConsumer}

def config_validation(ctx:click.Context, param, value):
    pass

async def gather_workers(*workers:Worker):
    await asyncio.gather(*(w.start() for w in workers))

@click.command
@click.pass_context
def start_producers(ctx:click.Context):
    producers:list[BaseProducer] = []
    for p in ctx.obj.get("producers",{}):
        type_str = p.get("type")
        if type_str not in VALID_PRODUCERS:
            click.echo(f"{type_str} is not a valid Producer!s")
            ctx.abort()
        prod_type:type = VALID_PRODUCERS[type_str]
        prod_args = p.get("args",{})
        producers.append(prod_type(**prod_args))
    asyncio.run(gather_workers(*producers))

@click.command
@click.pass_context
def start_consumers(ctx:click.Context):
    consumers:list[BaseConsumer] = []
    for c in ctx.obj.get("consumers",{}):
        type_str = c.get("type")
        if type_str not in VALID_CONSUMERS:
            click.echo(f"{type_str} is not a valid Consumer!s")
            ctx.abort()
        con_type:type = VALID_CONSUMERS[type_str]
        con_args = c.get("args",{})
        consumers.append(con_type(**con_args))
    asyncio.run(gather_workers(*consumers))

@click.group(chain=True)
@click.option("--config_file",type=click.types.File(),default="./archydra.yaml")
@click.pass_context
def cli(ctx:click.Context, config_file):
    ctx.obj = yaml.load(config_file)

cli.add_command(start_consumers)
cli.add_command(start_producers)

if __name__ == "__main__":
    cli()
