import sys

from BusDriversParserImpl import BusDriversParserImpl
from GossipingBusDrivers import GossipingBusDrivers
from MaxDrivenStopCountParserImpl import MaxDrivenStopCountParserImpl


class Main:
    @staticmethod
    def run():
        max_driven_stop_count = MaxDrivenStopCountParserImpl().parse(
            sys.argv[1]
        )

        print(sys.argv[2:])

        bus_drivers = BusDriversParserImpl().parse(sys.argv[2:])

        all_rumors_were_shared = GossipingBusDrivers(
            bus_drivers
        ).drive_until_all_rumors_shared(max_driven_stop_count)

        code = 0 if all_rumors_were_shared else 1
        sys.exit(code)


if __name__ == '__main__':
    Main().run()
