import queue
import signal
import soco

sonos = soco.SoCo('192.168.1.20')
subscription = sonos.group.coordinator.avTransport.subscribe(auto_renew=True)

while True:
    try:
        event = subscription.events.get(timeout=0.5)
        print(event.variables['transport_state'])

    except queue.Empty:
        pass
    except KeyboardInterrupt:
        subscription.unsubscribe()
        soco.events.event_listener.stop()
        break
