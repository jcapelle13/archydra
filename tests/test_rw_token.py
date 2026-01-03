from archydra.Consumers import ReadWiseConsumer
import click

if __name__ == "__main__":
    c = ReadWiseConsumer(click.prompt("Enter your ReadWise Reader API Key:"))
