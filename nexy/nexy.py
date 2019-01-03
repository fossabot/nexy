import click

from nexy.commands import component
from nexy.commands import repository
from nexy.commands import task
from nexy.services.nexus import NexusService
from nexy.utils.const import SERVICE


@click.group()
@click.option('--url', required=True, help='Url of the nexus', envvar='NEXY_URL')
@click.option('--username', required=True, help='Username to use as credential for the nexus', envvar='NEXY_USERNAME')
@click.option('--password', required=True, help='Password to use as credential for the nexus', envvar='NEXY_PASSWORD')
@click.pass_context
def main(ctx, url, username, password):
    """Sonatype Nexus CLI"""
    ctx.ensure_object(dict)
    ctx.obj[SERVICE] = NexusService(url, username, password)


# Register all commands
main.add_command(repository.command)
main.add_command(component.command)
main.add_command(task.command)
