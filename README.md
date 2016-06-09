# nao
Nao Utilities and Demos

## Tools

### Install

Enter the tools folder and run the command:

```
pip install .
```

Alternatively, if you want to be able to pull changes and have your command update you can add the `-e` option like so:

```
pip install -e .
```

### nao command

This program uses the Python SDK and provides shortcuts to common
tasks such as making the robot stand or sit. For example to make the
robot say "hello" you can use the command:

```
nao <hostname> say hello
```

To see a full list of commands use the `--help` option with the command.

