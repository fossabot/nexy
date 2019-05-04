# Nexy
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Famannocci%2Fnexy.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Famannocci%2Fnexy?ref=badge_shield)

Nexy is a tool design to manage Nexus from command line.

# Prerequisites
* [Python 3](https://docs.python.org/3/)
* [Python 3 - Pip](https://pypi.org/project/pip/)

# Features
* Manage tasks.
* Manage components in repository
* Manage repositories.

# Build
* To build `nexy` you will need to install prerequisites packages.
* Then run the command below to install nexy in dev mode into your local environment.

```bash
pip3 install --editable .
```

* You can now develop awesome `nexy` features interactively by running `nexy` command
* You can also build a standalone executable
```bash
pyinstaller nexy.spec
```

# Usage

## Obtain some help
* This tool is implement as a set of various sub-commands
* At any moment you can add the global option `--help` to obtain some help

```bash
Usage: nexy [OPTIONS] COMMAND [ARGS]...

  Sonatype Nexus CLI

Options:
  --url TEXT       Url of the nexus  [required]
  --username TEXT  Username to use as credential for the nexus  [required]
  --password TEXT  Password to use as credential for the nexus  [required]
  --help           Show this message and exit.

Commands:
  component   Manage components
  repository  List repositories
  task        Manage tasks
```

## Use environment
* You can use either explicit options or environment to define options.
```bash
export NEXY_URL=https://example.com
export NEXY_USERNAME=manage
export NEXY_PASSWORD=xxxxxxxxx

nexy repository ls
```
OR
```bash
nexy --url https://example.com --username manage --password xxxxxxxxx repository ls
```

## List all repositories
* You can run the command below to list repositories

```bash
nexy repository ls
```

## List all components in a repository
* You can run the command below to list all components in the repository `example`

```bash
nexy component ls example
```

## List all tasks
* You can run the command below to list all tasks

```bash
nexy task ls
```

## Start a task
* You can run the command below to start the task `id`

```bash
nexy task start <id>
```

## Stop a task
* You can run the command below to stop the task `id`

```bash
nexy task stop <id>
```

# Contributing
If you find this image useful here's how you can help :

* Send a Pull Request with your awesome new features and bug fixed
* Be a part of the community and help resolve [Issues](https://github.com/amannocci/nexy/issues)


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Famannocci%2Fnexy.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Famannocci%2Fnexy?ref=badge_large)