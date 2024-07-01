#include "utils.h"
#include <limits>
#include <stdio.h>

// Critical Params
#define WP_COUNT 10
#define POPULATION_SIZE 5
#define FLOAT_MAX_VALUE std::numeric_limits<float>::max()

// Design related params
#define MAX_TURN_ANGLE 450
#define SAFE_THROW_DISTANCE_IN_METERS 10

// Extra params
#define MAX_GENERATIONS 100

double ***CreatePopulation(double fence[][2]) {
    double ***population = new double **[POPULATION_SIZE];

    for (int individualIdx = 0; individualIdx < POPULATION_SIZE; ++individualIdx) {
        population[individualIdx] = new double *[WP_COUNT];
        for (int geneIdx = 0; geneIdx < WP_COUNT; ++geneIdx) {
            double randomLat, randomLong;
            generateRandomLatLon(fence, 4, randomLat, randomLong);
            population[individualIdx][geneIdx] = new double[2]{randomLat, randomLong};
        }
    }

    return population;
}

void PrintFirstIndividual(double ***population) {
    printf("QGC WPL 110\n");
    for (int i = 0; i < WP_COUNT; ++i) {
        printf("%d 0 3 16 0 0 0 0 %.20lf %.20lf 100 1\n", i,
               population[0][i][0], population[0][i][1]);
    }
}

float *MeasureFitness(double ***population, double beforeStart[2], double start[2], double target[2]) {
    float *fitness = new float[POPULATION_SIZE];

    for (int individualIdx = 0; individualIdx < POPULATION_SIZE; ++individualIdx) {
        fitness[individualIdx] = 0;
        bool isValid = true;

        // Handle the first waypoint separately
        double firstPoint[2] = {population[individualIdx][0][0], population[individualIdx][0][1]};
        double initialAngle = calculateAngle(beforeStart, start, firstPoint);
        if (initialAngle >= MAX_TURN_ANGLE) {
            fitness[individualIdx] = FLOAT_MAX_VALUE;
            continue;
        }
        fitness[individualIdx] += calculateDistance(start, firstPoint);

        // Iterate over waypoints
        for (int wpIdx = 1; wpIdx < WP_COUNT; ++wpIdx) {
            double currentPoint[2] = {population[individualIdx][wpIdx - 1][0], population[individualIdx][wpIdx - 1][1]};
            double nextPoint[2] = {population[individualIdx][wpIdx][0], population[individualIdx][wpIdx][1]};

            if (wpIdx < WP_COUNT - 1) {
                // Calculate the angle between the current waypoint, the next waypoint, and the waypoint after
                double nextNextPoint[2] = {population[individualIdx][wpIdx + 1][0], population[individualIdx][wpIdx + 1][1]};
                double angle = calculateAngle(currentPoint, nextPoint, nextNextPoint);
                if (angle >= MAX_TURN_ANGLE) {
                    fitness[individualIdx] = FLOAT_MAX_VALUE;
                    isValid = false;
                    break;
                }
            } else {
                // Last waypoint, calculate distance to the target
                double lastPoint[2] = {population[individualIdx][wpIdx][0], population[individualIdx][wpIdx][1]};
                double angle = calculateAngle(currentPoint, nextPoint, target);
                if (angle >= MAX_TURN_ANGLE) {
                    fitness[individualIdx] = FLOAT_MAX_VALUE;
                    isValid = false;
                    break;
                }
                float distanceToTarget = calculateDistance(nextPoint, target);
                if (distanceToTarget <= SAFE_THROW_DISTANCE_IN_METERS) {
                    fitness[individualIdx] = FLOAT_MAX_VALUE;
                    isValid = false;
                    break;
                }
                fitness[individualIdx] += distanceToTarget;
            }

            // Add distance to the total fitness
            fitness[individualIdx] += calculateDistance(currentPoint, nextPoint);
        }
    }

    return fitness;
}

int main() {
    // PARAMS FROM PYTHON
    // LAT, LONG
    double beforeStart[] = {29.8128513, 30.8248258};
    double start[] = {29.8122090, 30.8246648};
    double target[] = {29.8151506, 30.8272398};

    double fence[][2] = {
        {29.8114364, 30.8233023},
        {29.8201679, 30.8249760},
        {29.8197769, 30.8290315},
        {29.8108592, 30.8268857},
    };

    // END PARAMS FROM PYTHON

    srand(static_cast<unsigned>(time(0))); // Seed the random number generator once

    double ***population = CreatePopulation(fence);
    PrintFirstIndividual(population);
    int generations = -1;

    while (++generations < MAX_GENERATIONS) {
        float *fitness = MeasureFitness(population, beforeStart, start, target);
        sortPopulationByFitness(population, fitness, POPULATION_SIZE, WP_COUNT);
        printf("fuck you");
    }
}