#! /usr/bin/env python3

import queue
import signal
import soco
import marantz
import sys
import logging

logging.basicConfig(level="INFO")

sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)
groupSubscription = sonos.zoneGroupTopology.subscribe()

avr = marantz.Marantz('192.168.1.53')
lastState=''

def shutdown(signal, frame):
    logging.info('shutdown(): Shutting down...')
    subscription.unsubscribe()
    groupSubscription.unsubscribe()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

while True:
    logging.debug("main(): Main loop: Start...")
    # Check zone event subscription
    if not groupSubscription.is_subscribed or groupSubscription.time_left <= 5:
        try:
            logging.info("Unsubscribing to zone events")
            groupSubscription.unsubscribe()
            soco.events.event_listener.stop()
        except Exception as e:
            logging.info("Unsubscription to zone events failed")

        try:
            groupSubscription = sonos.zoneGroupTopology.subscribe(
                                                                auto_renew=True
                                                                 )
        except Exception as e:
            logging.warning('Zone event subscription failed.')
            time.sleep(10)

    # Check playback event subscription
    if not subscription.is_subscribed or subscription.time_left <= 5:
        try:
            logging.info("Unsubscribing to playback events")
            subscription.unsubscribe()
            soco.events.event_listener.stop()
        except Exception as e:
            logging.info("Unsubscription to playback events failed")

        try:
            subscription = sonos.group.coordinator.avTransport.subscribe(
                                                                auto_renew=True
                                                                        )
        except Exception as e:
            logging.warning('Playback event subscription failed.')
            time.sleep(10)

    try:
        logging.debug("Checking zone events...")
        zoneEvent = None
        zoneEvent = groupSubscription.events.get(timeout=0.5)
        if zoneEvent is not None:
            logging.info("Zone event found.")
            if subscription.service.soco.uid != sonos.group.coordinator.uid:
                logging.info("Uid of coordinator has changed. Resubscribing...")
                subscription.unsubscribe()
                subscription = sonos.group.coordinator.avTransport.subscribe(
                                                                auto_renew=True
                                                                            )
    except queue.Empty:
        pass

    try:
        logging.debug("Checking playback events...")
        playEvent = None
        playEvent = subscription.events.get(timeout=0.5)
        if playEvent is not None:
            logging.info('Playback event: %s',
                         playEvent.variables['transport_state']
                        )
            if playEvent.variables['transport_state'] == 'PLAYING':
                lastState = playEvent.variables['transport_state']
                avr.cd()
            elif playEvent.variables['transport_state'] == 'TRANSITIONING':
                if lastState == 'PAUSED_PLAYBACK':
                    avr.cd()
            elif playEvent.variables['transport_state'] == 'PAUSED_PLAYBACK':
                lastState = playEvent.variables['transport_state']
                avr.tv()
            elif playEvent.variables['transport_state'] == 'STOPPED':
                lastState = playEvent.variables['transport_state']
                avr.tv()
    except queue.Empty:
        pass
