#pragma once
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>

bool isInsideFence(double fence[][2], int n, double lat, double lon) {
    int count = 0, i, j;
    for (i = 0, j = n - 1; i < n; j = i++) {
        if (((fence[i][1] > lon) != (fence[j][1] > lon)) &&
            (lat < (fence[j][0] - fence[i][0]) * (lon - fence[i][1]) / (fence[j][1] - fence[i][1]) + fence[i][0])) {
            count++;
        }
    }
    return count % 2 == 1;
}

void generateRandomLatLon(double fence[][2], int n, double &randomLat, double &randomLong) {
    double minLat = fence[0][0], maxLat = fence[0][0];
    double minLong = fence[0][1], maxLong = fence[0][1];
    for (int i = 1; i < n; ++i) {
        if (fence[i][0] < minLat) minLat = fence[i][0];
        if (fence[i][0] > maxLat) maxLat = fence[i][0];
        if (fence[i][1] < minLong) minLong = fence[i][1];
        if (fence[i][1] > maxLong) maxLong = fence[i][1];
    }

    do {
        randomLat = minLat + static_cast<double>(rand()) / RAND_MAX * (maxLat - minLat);
        randomLong = minLong + static_cast<double>(rand()) / RAND_MAX * (maxLong - minLong);
    } while (!isInsideFence(fence, n, randomLat, randomLong));
}

double calculateDistance(double point1[2], double point2[2]) {
    // Placeholder for actual distance calculation (e.g., Haversine formula for lat/long)
    // Assuming flat earth for simplicity
    double dx = point1[0] - point2[0];
    double dy = point1[1] - point2[1];
    return std::sqrt(dx * dx + dy * dy);
}

// Function to calculate the angle between three points
double calculateAngle(double point1[2], double point2[2], double point3[2]) {
    // Placeholder for actual angle calculation
    // Vector 1->2
    double v1x = point2[0] - point1[0];
    double v1y = point2[1] - point1[1];

    // Vector 2->3
    double v2x = point3[0] - point2[0];
    double v2y = point3[1] - point2[1];

    // Dot product and magnitudes
    double dot = v1x * v2x + v1y * v2y;
    double mag1 = std::sqrt(v1x * v1x + v1y * v1y);
    double mag2 = std::sqrt(v2x * v2x + v2y * v2y);

    // Cosine of the angle
    double cosAngle = dot / (mag1 * mag2);

    // Angle in degrees
    return std::acos(cosAngle) * 180.0 / M_PI;
}

void sortPopulationByFitness(double ***population, float *fitness, int populationSize, int wpCount) {
    // Create a vector of pairs (fitness, population index)
    std::vector<std::pair<float, double **>> fitnessPopulationPairs(populationSize);
    for (int i = 0; i < populationSize; ++i) {
        fitnessPopulationPairs[i] = {fitness[i], population[i]};
    }

    // Sort the vector of pairs based on the fitness values
    std::sort(fitnessPopulationPairs.begin(), fitnessPopulationPairs.end(),
              [](const std::pair<float, double **> &a, const std::pair<float, double **> &b) {
                  return a.first < b.first;
              });

    // Reorder the original population array based on the sorted pairs
    for (int i = 0; i < populationSize; ++i) {
        fitness[i] = fitnessPopulationPairs[i].first;
        population[i] = fitnessPopulationPairs[i].second;
    }
}