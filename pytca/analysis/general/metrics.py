def calculate_vwap(prices, volumes):
    total_volume = sum(volumes)
    if total_volume == 0:
        return None
    return sum(p * v for p, v in zip(prices, volumes)) / total_volume
