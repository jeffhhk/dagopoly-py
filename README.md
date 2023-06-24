
# Synopsis

Dagopoly: Directed Acyclic Graph Merchant

## Etymology

Dag, for "Directed Acyclic Graph", plus "opoly" from Ancient Greek πωλέω (pōleō, "I barter, sell")

See also: https://www.wordnik.com/words/monopoly

## Running tests

    python -m unittest discover test/micro

## Running a minimal standalone example

    python test/autobin/test1.py 

## On logging

The library does not couple to any logging mechanism.  Instead, we can register a listener to recieve structured events.  If you would like to couple the structure events to the python logging mechanism, add this to your application:

    from dagopoly.micro.emit import add_emit_listener
    import logging
    logging.basicConfig(level=logging.DEBUG)
    def on_event(msg):
        kmsg=msg[0]
        if kmsg=='warning':
            logging.warning(msg[1:])
        else:
            logging.info(msg[1:])
    add_emit_listener(on_event)

For example, adding this to test/autobin/test1.py produces the following output:

    count_to_n=<class 'dagopoly.micro.block.count_to_n'>
    INFO:root:['computing', ['v0.0', 'count_to_n', 10]]
    count_to_n.get()=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    INFO:root:['computing', ['v0.0', 'square', ['v0.0', 'count_to_n', 10]]]
    INFO:root:['remembering', ['v0.0', 'count_to_n', 10], 'derived/0910a7f76852aa2f6040f1daf9b1bfac4996ba76']
    calculated 10 results

Take care not to throw an unhandled exception in the handler.
