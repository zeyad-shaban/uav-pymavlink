
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
        int invalidTurnPenality = 1500;
        int invalidThrowDistPenality = 2000;

        for (int indivIdx = 0; indivIdx < population.Length; ++indivIdx)
        {
            double score = 0;
            Waypoint[] individual = population[indivIdx];

            for (int wpIdx = 0; wpIdx < population[indivIdx].Length; ++wpIdx)
            {
                Waypoint currWaypoint = individual[wpIdx];
                Waypoint before = wpIdx == 0 ? start : individual[wpIdx - 1];
                Waypoint beforeBefore = wpIdx == 0 ? beforeStart : (wpIdx == 1 ? start : individual[wpIdx - 2]);

                if (!WaypointsMath.IsValidTurn(beforeBefore, before, currWaypoint)) score += invalidTurnPenality;
                score += WaypointsMath.GetArcLengthLast2Wp(beforeBefore, before, currWaypoint);

            }

            double distToTarget = WaypointsMath.GetArcLengthLast2Wp(individual[^2], individual[^1], target);
            if (distToTarget >= DesignParams.MAX_THROW_DIST) score += invalidThrowDistPenality;

            score += distToTarget;
            fitness[indivIdx] = (float)score;
        }

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
            // B
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