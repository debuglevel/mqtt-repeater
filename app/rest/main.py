#!/bin/usr/python3
import argparse
import configparser
import logging.config
import logging
from multiprocessing.connection import Client
import signal
import asyncio
from typing import List
import gmqtt


termination_event = asyncio.Event()

clients = []


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def on_connect(client, flags, rc, properties):
    logging.info('[connected {}]'.format(client._client_id))


def on_message(client, topic, payload, qos, properties):
    logging.debug('[received message {}] topic: {} payload: {} QOS: {} properties: {}'
                 .format(client._client_id, topic, payload, qos, properties))

    for client in clients:
        if client._client_id == client._client_id:
            continue

        # TODO: republish also properties
        client.publish(topic, payload, qos=qos)   


def on_disconnect(client, packet, exc=None):
    logging.info('[disconnected {}]'.format(client._client_id))


def on_subscribe(client, mid, qos, properties):
    logging.info('[subscribed {}] QOS: {}'.format(client._client_id, qos))


def configure_callbacks(client):
    logging.debug(f"Configuring client callbacks...")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe


def set_termination(*args):
    logging.info("Received SIGTERM or SIGKILL")
    termination_event.set()


async def disconnect_clients(clients: List[Client]):
    logging.info(f"Disconncting clients...")
    for client in clients:
        logging.debug(f"Disconncting client {client}...")
        await client.disconnect()

async def main(config):
    global clients

    logging.info(f"Connecting clients...")
    for client_name in config.keys():
        logging.debug(f"Configuring client...")
        # TODO: should probably not be just named liked this, but have a random part.
        client = gmqtt.Client(client_name, clean_session=False, session_expiry_interval=0xFFFFFFFF)
        configure_callbacks(client)
        client.set_auth_credentials(config[client_name]['username'],
                                    config[client_name]['password'])
        
        logging.debug(f"Connecting client...")
        await client.connect(config[client_name]['host'],
                             config[client_name]['port'],
                             ssl=config[client_name]['ssl'])

        logging.debug(f"Subscribing topics...")
        for topic in config[client_name]['topics']:
            logging.debug(f"Subscribing topic {topic}...")
            client.subscribe(topic, qos=1, no_local=True)

        clients.append(client)

    await termination_event.wait()
    await disconnect_clients(clients)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    import yaml
    logging.config.dictConfig(yaml.load(open("app/logging-config.yaml", 'r')))  # configured via cmdline

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', default='config.yaml')
    args = arg_parser.parse_args()
    config = yaml.load(open(args.config_path), Loader=yaml.FullLoader)

    loop.add_signal_handler(signal.SIGINT, set_termination)
    loop.add_signal_handler(signal.SIGTERM, set_termination)

    loop.run_until_complete(main(config))
