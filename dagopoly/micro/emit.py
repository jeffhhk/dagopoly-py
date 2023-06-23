
_emit_listeners = []
def emit(msg):
    for l in _emit_listeners:
        try:
            l(msg)
        except Exception as ex:
            # listeners are on their own for catching their exceptions!
            pass

def add_emit_listener(l):
    _emit_listeners.append(l)
