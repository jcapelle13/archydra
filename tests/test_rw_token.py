import click

from archydra.Consumers import ReadWiseConsumer

if __name__ == "__main__":
    c = ReadWiseConsumer(click.prompt("Enter your ReadWise Reader API Key:"))
