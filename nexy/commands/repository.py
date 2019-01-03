import click
import urllib3

from nexy.utils.const import SERVICE


@click.command('repository')
@click.pass_context
def command(ctx):
    """List repositories"""
    nexus_service = ctx.obj[SERVICE]

    click.secho("⇒ Fetching all repositories", fg='yellow')
    try:
        repos = nexus_service.find_repositories()
        if len(repos) > 0:
            for repo in repos:
                click.secho("{}".format(repo['name']), fg='blue')
                click.echo("├── Format: {}".format(repo['format']))
                click.echo("├── Type: {}".format(repo['type']))
                click.echo("└── Url: {}".format(repo['url']))
        else:
            click.secho("✓ Repository is empty", fg='green')
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')
