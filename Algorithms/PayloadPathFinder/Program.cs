
/* TODOS
TODO When calculating fitness function ensure that no arc exceeds the fence, otherwise give penality
TODO Ensure the above rule for from the throw point, to the landing location
!TODO Add a gene for the angle we shoudl approach the payload from, and use it as the new target to drop from
*/

class Program
{
    static void Main()
    {
        Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE);

        float[] fitness = new float[population.Length];
        for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
        {
            fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
            Array.Sort(fitness, population);

            Genetic.Reproduce(population);
        }

        Console.WriteLine(fitness[0]);
        WaypointPrinter.PrintWaypoints(population[0]);
    }
}