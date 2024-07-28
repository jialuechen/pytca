#include <vector>

double calculate_vwap(const std::vector<double>& prices, const std::vector<double>& volumes) {
    double volume_sum = 0.0;
    double weighted_sum = 0.0;

    for (size_t i = 0; i < prices.size(); ++i) {
        weighted_sum += prices[i] * volumes[i];
        volume_sum += volumes[i];
    }

    return volume_sum == 0.0 ? 0.0 : weighted_sum / volume_sum;
}
