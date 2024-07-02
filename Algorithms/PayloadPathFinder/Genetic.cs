
public static class Genetic
{
    public static Waypoint[][] CreatePopulation(int chromosomeSize)
    {
        Waypoint[][] population = new Waypoint[CodeParams.POPULATION_SIZE][];

        for (int i = 0; i < population.Length; ++i)
        {
            population[i] = new Waypoint[CodeParams.CHROMOSOME_SIZE];
            for (int geneIdx = 0; geneIdx < chromosomeSize; ++geneIdx)
            {
                population[i][geneIdx] = WaypointGenerator.GenerateRandomWaypoint();
            }
        }



        return population;
    }

    public static float[] MeasureFitness(float[] fitness, Waypoint[][] population, Waypoint beforeStart, Waypoint start, Waypoint target)
    {
        // for (int indivIdx = 0; indivIdx < population.Length; ++indivIdx)
        // {
        //     double totalDistance = 0;
        //     Waypoint[] individual = population[indivIdx];

        //     Waypoint lastWp = individual[^1];
        //     double distance = WaypointsMath.GetDistanceBetweenWaypoints(lastWp, target);
        //     double angle = WaypointsMath.AngleBetween3Points(individual[^2], lastWp, target);


        //     if (distance < DesignParams.MIN_THROW_DISTANCE_IN_METERS ||
        //         distance > DesignParams.MAX_WP_SPACING ||
        //         angle < DesignParams.MIN_TURN_RADIUS
        //         )
        //     {
        //         fitness[indivIdx] = float.MaxValue;
        //         continue;
        //     }

        //     totalDistance += distance;

        //     for (int wpIdx = 0; wpIdx < population[indivIdx].Length; ++wpIdx)
        //     {
        //         Waypoint currWaypoint = individual[wpIdx];
        //         Waypoint before = wpIdx == 0 ? start : individual[wpIdx - 1];
        //         Waypoint beforeBefore = wpIdx == 0 ? beforeStart : (wpIdx == 1 ? start : individual[wpIdx - 2]);

        //         angle = WaypointsMath.AngleBetween3Points(before, currWaypoint, beforeBefore);
        //         distance = WaypointsMath.GetDistanceBetweenWaypoints(before, currWaypoint);

        //         if (distance > DesignParams.MAX_WP_SPACING ||
        //             distance < DesignParams.MIN_WP_SPACING ||
        //             angle < DesignParams.MIN_TURN_RADIUS
        //             )
        //         {
        //             totalDistance = double.MaxValue;
        //             break;
        //         }

        //         totalDistance += distance;

        //     }
        //     fitness[indivIdx] = (float)totalDistance;
        // }

        return fitness;
    }

    public static void Reproduce(Waypoint[][] population)
    {
        Random random = new();
        int targetKill = (int)(population.Length * CodeParams.REPLACE_RATE);

        int offspringIdx = targetKill;
        for (int i = 0; i < targetKill; ++i)
        {
            Waypoint[] parentA = population[random.Next(0, targetKill)];
            Waypoint[] parentB = population[random.Next(0, targetKill)];


            (Waypoint[] offspringA, Waypoint[] offspringB) = CrossOver(parentA, parentB, random);
            population[offspringIdx] = offspringA;
            if (offspringIdx + 1 < population.Length) population[++offspringIdx] = offspringB;
        }
    }

    private static (Waypoint[] offspringA, Waypoint[] offspringB) CrossOver(Waypoint[] parentA, Waypoint[] parentB, Random? random = null)
    {
        random ??= new();
        bool shouldMutateA = random.NextDouble() < CodeParams.INDIVIDUAL_MUTATE_RATE;
        bool shouldMutateB = random.NextDouble() < CodeParams.INDIVIDUAL_MUTATE_RATE;

        Waypoint[] offspringA = new Waypoint[parentA.Length];
        Waypoint[] offspringB = new Waypoint[parentA.Length];

        for (int geneIdx = 0; geneIdx < offspringA.Length; ++geneIdx)
        {
            if (shouldMutateA && random.NextDouble() < CodeParams.GENE_MUTATE_RATE)
            {
                offspringA[geneIdx] = WaypointGenerator.GenerateRandomWaypoint();
            }
            else
            {
                offspringA[geneIdx] = random.Next(0, 2) == 0 ? parentA[geneIdx] : parentB[geneIdx];
            }
            if (shouldMutateB && random.NextDouble() < CodeParams.GENE_MUTATE_RATE)
            {
                offspringB[geneIdx] = WaypointGenerator.GenerateRandomWaypoint();
            }
            else
            {
                offspringB[geneIdx] = random.Next(0, 2) == 1 ? parentA[geneIdx] : parentB[geneIdx];
            }
        }

        return (offspringA, offspringB);
    }
}