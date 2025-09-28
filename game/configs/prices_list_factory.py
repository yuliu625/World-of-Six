import random

from typing import Literal


_theoretical_solution_025 = dict(
    network_effect=dict(network_effect=0.25),
    prices_list=[
        dict(price=2.24),
        dict(price=2.99),
        dict(price=3.74),
        dict(price=4.49),
        dict(price=5.24),
        dict(price=5.99),
    ]
)

_theoretical_solution_075 = dict(
    network_effect=dict(network_effect=0.75),
    prices_list=[
        dict(price=4.74),
        dict(price=4.99),
        dict(price=5.24),
        dict(price=5.49),
        dict(price=5.74),
        dict(price=5.99),
    ]
)


class PricesListFactory:
    def __init__(self, network_effect: Literal[0.25, 0.75] = 0.25):
        self.theoretical_solution = None
        if network_effect == 0.25:
            self.theoretical_solution = _theoretical_solution_025
        elif network_effect == 0.75:
            self.theoretical_solution = _theoretical_solution_075
        self.prices_list = self.theoretical_solution['prices_list']

    def get_sequence_price(self) -> dict:
        return self.theoretical_solution.copy()

    def get_one_time_price_list(self, price_index) -> dict:
        dict_copy = self.theoretical_solution.copy()
        dict_copy['prices_list'] = [self.prices_list[price_index]]
        return dict_copy

    def get_same_price_list(self, price_index) -> dict:
        dict_copy = self.theoretical_solution.copy()
        dict_copy['prices_list'] = [self.prices_list[price_index] for _ in range(len(self.prices_list))]
        return dict_copy

    def get_reverse_price(self) -> dict:
        dict_copy = self.theoretical_solution.copy()
        dict_copy['prices_list'] = self.prices_list[::-1]
        return dict_copy

    def get_random_price(self) -> dict:
        dict_copy = self.theoretical_solution.copy()
        dict_copy['prices_list'] = random.sample(self.prices_list, len(self.prices_list))
        return dict_copy

    def _modify_dict(self, input_dict, key, value) -> dict:
        dict_copy = input_dict.copy()
        dict_copy[key] = value
        return dict_copy

