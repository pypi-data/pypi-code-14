import os
import json
import time
import click

import educube.util.display as display
import educube.util.educube_conn as educonn
from educube.util.telemetry_parser import TelemetryParser

import logging
logger = logging.getLogger(__name__)


def read_telemetry(educube_connection):
    '''Shows the latest telemetry received from the EduCube'''
    parser = TelemetryParser()
    telemetry_packets = educube_connection.get_telemetry()
    for telem in telemetry_packets:
        try:
            telemetry = parser.parse_telemetry(telem)
        except Exception as e:
            logger.exception("Telemetry badly formed: %s\n%s" % (telem, e))
    print display.display_color_json(parser.last_board_telemetry)


def write_command(educube_connection):
    '''Writes a command to a chosen board on the EduCube (e.g. 'MAG|X|+' -> ADC) '''
    parser = TelemetryParser()
    board_choices = parser.BOARD_CONFIG.keys()

    board = None

    click.secho("Select and EduCube board for command: %s" % board_choices, fg='cyan')
    while board not in board_choices:
        if board:
            print "Bad selection"
        board = click.prompt("Enter board ID:")
    command = click.prompt("Enter command for %s board" % board)
    formatted_command = educube_connection.format_command(board, command)
    if click.confirm("Send command (%s) to EduCube?" % formatted_command, default=True):
        response = educube_connection.send_command(formatted_command)
 