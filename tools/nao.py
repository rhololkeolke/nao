#!/usr/bin/env python
"""Provides some quick shortcuts to common nao tasks."""

import click
import socket
from naoqi import ALProxy


def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0


@click.group()
@click.argument('hostname')
@click.option('--port', default=9559, type=click.IntRange(1, 65535))
@click.pass_context
def cli(ctx, hostname, port):
    if hostname_resolves(hostname):
        ctx.obj = {'HOSTNAME': hostname, 'PORT': port}
    else:
        raise click.BadParameter('Hostname could not be resolved.')


@click.command()
@click.pass_context
def battery(ctx):
    """Prints the battery level of the robot."""

    battery = ALProxy('ALBattery', str(ctx.obj['HOSTNAME']), ctx.obj['PORT'])
    click.echo('Battery Charge {:d}%'.format(battery.getBatteryCharge()))


@click.command()
@click.argument('pose_name',
                type=click.Choice(['standinit', 'sitrelax', 'standzero',
                                   'lyingbelly', 'lyingback', 'stand',
                                   'crouch', 'sit']))
@click.pass_context
def pose(ctx, pose_name):
    """Sends the robot to the given pose."""

    pose_name_map = {'standinit': 'StandInit',
                     'sitrelax': 'SitRelax',
                     'standzero': 'StandZero',
                     'lyingbelly': 'LyingBelly',
                     'lyingback': 'LyingBack',
                     'stand': 'Stand',
                     'crouch': 'Crouch',
                     'sit': 'Sit'}

    posture = ALProxy('ALRobotPosture', str(ctx.obj['HOSTNAME']),
                      ctx.obj['PORT'])
    posture.goToPosture(pose_name_map[str(pose_name)], 1.0)


def motors_are_on(motors, tolerance=1e-12):
    stiffnesses = motors.getStiffnesses('Body')
    return (reduce(lambda x, y: max(abs(x), abs(y)), stiffnesses, 0.0) >
            tolerance)


@click.command()
@click.argument('action', type=click.Choice(['on', 'off', 'toggle', 'status']))
@click.pass_context
def motors(ctx, action):
    """Interacts with the robot motors."""
    hostname = str(ctx.obj['HOSTNAME'])
    port = ctx.obj['PORT']
    action = str(action)

    motors = ALProxy('ALMotion', hostname, port)

    if action == 'status':
        if motors_are_on(motors):
            click.echo('Motors are on')
        else:
            click.echo('Motors are off')
    elif action == 'on':
        motors.wakeUp()
    elif action == 'off':
        motors.rest()
    elif action == 'toggle':
        if motors_are_on(motors):
            motors.rest()
        else:
            motors.wakeUp()


@click.command()
@click.argument('message')
@click.pass_context
def say(ctx, message):
    """Uses text to speech to say a message."""
    tts = ALProxy('ALTextToSpeech', str(ctx.obj['HOSTNAME']), ctx.obj['PORT'])
    tts.say(str(message))


cli.add_command(pose)
cli.add_command(motors)
cli.add_command(say)
cli.add_command(battery)
