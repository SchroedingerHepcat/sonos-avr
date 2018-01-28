#! /usr/bin/env python3

import queue
import signal
import soco
import marantz

def shutdown(signal, frame):
    print('Shutting down...')
    subscription.unsubscribe()
    groupSubscription.unsubscribe()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

def handleSonosPlaybackEvent(event, avr):
    print('Playback event:', event.variables['transport_state'])
    if event.variables['transport_state'] == 'PLAYING':
        lastState = event.variables['transport_state']
        avr.cd()
    elif event.variables['transport_state'] == 'TRANSITIONING':
        if lastState == 'PAUSED_PLAYBACK':
            avr.cd()
    elif event.variables['transport_state'] == 'PAUSED_PLAYBACK':
        lastState = event.variables['transport_state']
        avr.tv()

def handleSonosZoneEvent(event, avr):
    if subscription.service.soco.uid != sonos.group.coordinator.uid:
        subscription.unsubscribe()
        subscription = sonos.group.coordinator.avTransport.subscribe(
                                                                 auto_renew=True
                                                                    )

def maintainZoneEventSubscription(subscription, sonos):
    if not subscription:
        pass
    elif not subscription.is_subscribed or subscription.time_left <= 5:
        try:
            print("Unsubscribing to zone events")
            subscription.unsubscribe()
            soco.events.event_listener.stop()
        except Exception as e:
            print("Unsubscription failed")

    try:


def maintainPlaybackEventSubscription(subscription, sonos):
    pass


sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)
groupSubscription = sonos.zoneGroupTopology.subscribe()

avr = marantz.Marantz('192.168.1.53')
lastState=''

while True:
    # Check zone event subscription
    if not groupSubscription.is_subscribed or groupSubscription.time_left <= 5:
        try:
            print("Unsubscribing to zone events")
            groupSubscription.unsubscribe()
            soco.events.event_listener.stop()
        except Exception as e:
            print("Unsubscription to zone events failed")

        try:
            groupSubscription = sonos.zoneGroupTopology.subscribe(auto_renew=True
                                                                 )
        except Exception as e:
            print('Zone event subscription failed.')
            time.sleep(10)

    # Check playback event subscription
    if not subscription.is_subscribed or subscription.time_left <= 5:
        try:
            print("Unsubscribing to playback events")
            subscription.unsubscribe()
            soco.events.event_listener.stop()
        except Exception as e:
            print("Unsubscription to playback events failed")

        try:
            subscription = sonos.group.coordinator.avTransport.subscribe(
                                                                 auto_renew=True
                                                                        )
        except Exception as e:
            print('Playback event subscription failed.')
            time.sleep(10)

    try:
        zoneEvent = None
        zoneEvent = groupSubscription.events.get(timeout=0.5)
        if zoneEvent is not None:
            handleSonosZoneEvent(zoneEvent)

        playbackEvent = None
        playbackEvent = subscription.events.get(timeout=0.5)
        if event is not None:
            handleTransportEvent(playbackEvent, avr)
    except queue.Empty:
        pass
    except KeyboardInterrupt:
        subscription.unsubscribe()
        soco.events.event_listener.stop()
        break
