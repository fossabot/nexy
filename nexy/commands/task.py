import click
import urllib3

from nexy.utils.const import SERVICE


@click.group('task')
@click.pass_context
def command(ctx):
    """Manage tasks"""
    pass


@command.command('ls')
@click.pass_context
def ls(ctx):
    """List tasks"""
    nexus_service = ctx.obj[SERVICE]

    click.secho("⇒ Fetching all tasks", fg='yellow')
    try:
        tasks = nexus_service.find_tasks()
        if len(tasks) > 0:
            for task in tasks:
                click.secho("{}".format(task['id']), fg='blue')
                click.echo("├── Name: {}".format(task['name']))
                click.echo("├── Type: {}".format(task['type']))
                click.echo("├── Message: {}".format(task['message']))
                click.echo("├── Current state: {}".format(task['currentState']))
                click.echo("├── Next run: {}".format(task['nextRun']))
                click.echo("├── Last run: {}".format(task['lastRun']))
                click.echo("└── Last run result: {}".format(task['lastRunResult']))
        else:
            click.secho("✓ Task list is empty", fg='green')
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')


@command.command('start')
@click.argument('id')
@click.pass_context
def start(ctx, id):
    """Start a task"""
    nexus_service = ctx.obj[SERVICE]
    try:
        # Attempt to fetch all components
        click.secho("⇒ Starting task", fg='yellow')
        nexus_service.start_task(id)
        click.secho("✓ Task has been started", fg='green')
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')


@command.command('stop')
@click.argument('id')
@click.pass_context
def stop(ctx, id):
    """Stop a task"""
    nexus_service = ctx.obj[SERVICE]
    try:
        # Attempt to fetch all components
        click.secho("⇒ Stopping task", fg='yellow')
        nexus_service.stop_task(id)
        click.secho("✓ Task has been stopped", fg='green')
    except (urllib3.exceptions.NewConnectionError, ValueError) as identifier:
        click.secho("✗ Error: {0}".format(identifier), fg='red')
