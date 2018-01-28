#! /usr/bin/env python3

import queue
import signal
import soco
import marantz


sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)
groupSubscription = sonos.zoneGroupTopology.subscribe()

avr = marantz.Marantz('192.168.1.53')
lastState=''

def shutdown(signal, frame):
    print('Shutting down...')
    subscription.unsubscribe()
    groupSubscription.unsubscribe()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

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
            groupSubscription = sonos.zoneGroupTopology.subscribe(
                                                                auto_renew=True
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
            if subscription.service.soco.uid != sonos.group.coordinator.uid:
                subscription.unsubscribe()
                subscription = sonos.group.coordinator.avTransport.subscribe(
                                                                auto_renew=True
                                                                            )

        playbackEvent = None
        playbackEvent = subscription.events.get(timeout=0.5)
        if playbackEvent is not None:
            print('Playback event:',
                  playbackEvent.variables['transport_state']
                 )
            if playbackEvent.variables['transport_state'] == 'PLAYING':
                lastState = playbackEvent.variables['transport_state']
                avr.cd()
            elif event.variables['transport_state'] == 'TRANSITIONING':
                if lastState == 'PAUSED_PLAYBACK':
                    avr.cd()
            elif event.variables['transport_state'] == 'PAUSED_PLAYBACK':
                lastState = playbackEvent.variables['transport_state']
                avr.tv()
    except queue.Empty:
        pass
    except KeyboardInterrupt:
        subscription.unsubscribe()
        soco.events.event_listener.stop()
        break
