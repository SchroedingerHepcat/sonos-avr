#! /usr/bin/env python3

import queue
import signal
import soco
import marantz

sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)

avr = marantz.Marantz('192.168.1.53')

lastState=''

while True:
    try:
        event = subscription.events.get(timeout=0.5)
        print(event.variables['transport_state'])

        if event.variables['transport_state'] == 'PLAYING':
            lastState = event.variables['transport_state']
            avr.cd()
        elif event.variables['transport_state'] == 'TRANSITIONING':
            if lastState == 'PAUSED_PLAYBACK':
                avr.cd()
        elif event.variables['transport_state'] == 'PAUSED_PLAYBACK':
            lastState = event.variables['transport_state']
            avr.tv()

    except queue.Empty:
        pass
    except KeyboardInterrupt:
        subscription.unsubscribe()
        soco.events.event_listener.stop()
        break
