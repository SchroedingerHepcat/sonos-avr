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


sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)
groupSubscription = sonos.zoneGroupTopology.subscribe()

avr = marantz.Marantz('192.168.1.53')
lastState=''

while True:
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
