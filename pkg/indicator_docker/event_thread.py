import logging
import threading


class EventThread(threading.Thread):
    """Threaded event handler implementation for dealing with Docker daemon events."""

    def __init__(self, docker_client):
        # We're a daemon thread (existence of which doesn't have to keep the whole program alive)
        super().__init__(daemon=True)
        self.terminated = False
        self.docker_client = docker_client

    def run(self):
        logging.debug("EventThread started, name `%s`",  self.name)

        # Loop over Docker events until terminated
        for event in self.docker_client.events():
            if self.terminated:
                break
            logging.debug("Docker event: %s", str(event))
