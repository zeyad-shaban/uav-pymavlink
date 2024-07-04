
/* TODOS
TODO When calculating fitness function ensure that no arc exceeds the fence, otherwise give penality
TODO Ensure the above rule for from the throw point, to the landing location
TODO calculate turn radius using the equation thingy
*/

class Program
{
    static void Main()
    {
        Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE, MissionParams.Target);

        float[] fitness = new float[population.Length];
        for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
        {
            fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
            Array.Sort(fitness, population);
            // break;
            Genetic.Reproduce(population);
        }

        Console.WriteLine(fitness[0]);
        WaypointPrinter.PrintWaypoints([MissionParams.BeforeStart, MissionParams.Start, .. population[0], MissionParams.Target]);
    }
}