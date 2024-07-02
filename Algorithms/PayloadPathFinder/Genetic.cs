
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

    public static float[] MeasureFitness(Waypoint[][] population)
    {
        float[] fitness = new float[population.Length];

        for (int indivIdx = 0; indivIdx < population.Length; ++indivIdx)
        {
            float score = float.MaxValue;
            foreach (Waypoint waypoint in population[indivIdx])
            {
                
            }
            fitness[indivIdx] = score;
        }


        return fitness;
    }
}