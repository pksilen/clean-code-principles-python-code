# Just a simple counter that does not implement
# counting per labels
class Counter:
    def __init__(self, name: str):
        self.__name = name
        self.__count = 0

    def increment(
        self, increment: int, label_name_to_value: dict[str, str]
    ) -> None:
        print(
            f'Counter {self.__name} incremented by {increment} with labels: {label_name_to_value}'
        )
        self.__count += increment
