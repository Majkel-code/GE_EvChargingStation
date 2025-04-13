

def calculate_expected_kw(percent, max_capacity):
    """
    Calculate the expected kW based on the battery level and maximum battery capacity.
    """

    return (int(percent) / 100) * int(max_capacity)
    