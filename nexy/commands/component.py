import re

import click
import urllib3

from nexy.utils.const import SERVICE


@click.group('component')
@click.pass_context
def command(ctx):
    """Manage components"""
    pass


def is_valid(filters, doc):
    """Filter documents based on filter list"""
    valid = True
    for f in filters:
        if f.startswith("id="):
            valid &= re.match(re.compile(f[3:]), doc['id']) is not None
        elif f.startswith("name="):
            valid &= re.match(re.compile(f[5:]), doc['name']) is not None
        elif f.startswith("version="):
            valid &= re.match(re.compile(f[8:]), doc['version']) is not None
        else:
            return False
    return valid


@command.command('ls')
@click.argument('repository')
@click.option('--filter', help='Apply filter on result list', multiple=True)
@click.pass_context
def ls(ctx, repository, filter):
    """List components in repository"""
    nexus_service = ctx.obj[SERVICE]

    click.secho("⇒ Fetching all components in repository", fg='yellow')
    try:
        repos = nexus_service.find_components(repository)
        repos = [repo for repo in repos if is_valid(filter, repo)]
        for repo in repos:
            click.secho("{}".format(repo['id']), fg='blue')
            click.echo("├── Name: {}".format(repo['name']))
            if repo['group'] is not None:
                click.echo("├── Group: {}".format(repo['group']))
            click.echo("└── Version: {}".format(repo['version']))
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')


@command.command('rm')
@click.option('--id', help='Id of the component to remove')
@click.option('--repository', help='Repository of the component')
@click.option('--filter', help='Apply filter on result list', multiple=True)
@click.pass_context
def rm(ctx, repository, id, filter):
    """Remove one or more components"""
    if (id is not None and filter is not None) or (id is None and filter is None):
        raise click.UsageError("Use either id or filter option")

    nexus_service = ctx.obj[SERVICE]
    try:
        if id is not None:
            click.secho("⇒ Deleting component", fg='yellow')
            nexus_service.delete_component(id)
            click.secho("✓ Component have been deleted", fg='green')
        else:
            # Attempt to fetch all components
            click.secho("⇒ Fetching all components", fg='yellow')

            components = nexus_service.find_components(repository)
            components = [component for component in components if is_valid(filter, component)]

            click.secho("⇒ Deleting all components", fg='yellow')
            with click.progressbar(components) as cpnts:
                for component in cpnts:
                    nexus_service.delete_component(component['id'])
            click.secho("✓ Components have been deleted", fg='green')
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')
