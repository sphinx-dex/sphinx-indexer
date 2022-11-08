from apibara import EventFilter, IndexerRunner, Info, NewEvents
from apibara.indexer import IndexerRunnerConfiguration
from decouple import config

MONGODB_URL = config('MONGODB_URL')
indexer_id = "StarkdexIndexer"

async def handle_events(info: Info, block_events: NewEvents):
    """Handle a group of events grouped by block."""
    print(f"Received events for block {block_events.block.number}")
    for event in block_events.events:
        print(event)

    events = [
        {"address": event.address, "data": event.data, "name": event.name}
        for event in block_events.events
    ]

    # Insert multiple documents in one call.
    await info.storage.insert_many("events", events)


async def run_indexer(server_url=None, mongo_url=None, restart=None):
    print("Starting Apibara indexer")

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            apibara_url=server_url,
            apibara_ssl=True,
            storage_url=MONGODB_URL,
        ),
        reset_state=1,
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    # Create the indexer if it doesn't exist on the server,
    # otherwise it will resume indexing from where it left off.
    #
    # For now, this also helps the SDK map between human-readable
    # event names and StarkNet events.
    runner.add_event_filters(
        filters=[
            EventFilter.from_event_name(
                name="log_create_market",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_create_bid",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_create_ask",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_bid_taken",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_offer_taken",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_buy_filled",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_sell_filled",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
            EventFilter.from_event_name(
                name="log_delete_order",
                address="0x0602fc01bd2603baf9946e1a532e37bbeb1ea2faa9f4b5b91bf9a1e10b3ebfcd",
            ),
        ],
        index_from_block=0,
    )

    print("Initialization completed. Entering main loop.")

    await runner.run()
