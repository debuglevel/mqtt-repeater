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


def map_topic(client, topic: str) -> List[str]:
    logging.debug(f"Mapping {topic}...")

    new_topics = []

    for mapped_topic in config[client._client_id]["mapped_topics"]:
        if topic.startswith(mapped_topic["from"]):
            logging.debug(f"{mapped_topic} starts with {mapped_topic['from']}")

            for to_topic in mapped_topic["to"]:
                new_topic = topic.replace(mapped_topic["from"],
                                          to_topic)

                logging.debug(f"Mapped {mapped_topic['from']} to {new_topic}")
                new_topics.append(new_topic)
        else:
            logging.debug(f"{mapped_topic} does not start with {mapped_topic['from']}")

    logging.debug(f"Mapped {topic} to {len(new_topics)} topics: {new_topics}")
    return new_topics


def on_connect(client, flags, rc, properties):
    logging.info('[connected {}]'.format(client._client_id))


def on_message(client, topic, payload, qos, properties):
    logging.debug(
        f'[received message {client._client_id}] topic: {topic} payload: {payload} QOS: {qos} properties: {properties}')

    new_topics = map_topic(client, topic)

    for other_client in clients:
        # if other_client._client_id == client._client_id:
        #     continue

        for new_topic in new_topics:
            # TODO: republish also properties
            logging.debug(f"Republishing {topic} as {new_topic} on {client._client_id}...")
            other_client.publish(new_topic, payload, qos=qos)


def on_disconnect(client, packet, exc=None):
    logging.info(f'[disconnected {client._client_id}]')


def on_subscribe(client, mid, qos, properties):
    logging.info(f'[subscribed {client._client_id}] QOS: {qos}')


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


async def main():
    global clients
    global config

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
        for topic in config[client_name]['subscribed_topics']:
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

    loop.run_until_complete(main())
