import click
from ruamel.yaml import YAML
from .Consumers import *
from .Producers import *
import asyncio
from .Helpers import Worker, VALID_CONSUMERS, VALID_PRODUCERS
from loguru import logger
from io import StringIO

yaml = YAML()


def config_validation(ctx:click.Context, param, value):
    data = yaml.load(value)
    return dict(data)

async def gather_workers(*workers:Worker):
    await asyncio.gather(*(w.start() for w in workers))

@click.command
@click.pass_context
def start_producers(ctx:click.Context):
    producers:list[BaseProducer] = []
    for p in ctx.obj.get("producers",{}):
        producers.append(BaseProducer.from_config(p))
    asyncio.run(gather_workers(*producers))

@click.command
@click.pass_context
def start_consumers(ctx:click.Context):
    consumers:list[BaseConsumer] = []
    for c in ctx.obj.get("consumers",{}):
        consumers.append(BaseConsumer.from_config(c))
    asyncio.run(gather_workers(*consumers))

@click.group(chain=True)
@click.option("--config_file",type=click.types.File(),default="./archydra.yaml", callback=config_validation)
@click.option("--secret-file",type=click.types.File(),default="./secrets.yaml")
@click.pass_context
def cli(ctx:click.Context, secret_file, config_file):
    ctx.obj = {}
    secrets = dict(yaml.load(secret_file))
    config_stream = StringIO()
    yaml.dump(config_file, config_stream)
    str_form = config_stream.getvalue()
    config_stream.close()
    formatted = str_form.format(**secrets)
    formatted_stream = StringIO(formatted)
    templated_config = yaml.load(formatted_stream)
    ctx.obj.update(templated_config)
    


cli.add_command(start_consumers)
cli.add_command(start_producers)

if __name__ == "__main__":
    cli()
