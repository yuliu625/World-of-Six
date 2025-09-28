
def calculate_utility(
        standalone_value: int,
        participant_number: int,
        network_effect: float,
        price: float = 5
) -> float:
    return standalone_value + network_effect * participant_number - price

