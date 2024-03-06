class MaxDrivenStopCountParserImpl(MaxDrivenStopCountParser):
    def parse(self, max_driven_stop_count_as_str: str) -> int:
        return int(max_driven_stop_count_as_str)