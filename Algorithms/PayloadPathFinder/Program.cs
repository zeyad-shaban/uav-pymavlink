
class Program
{
    static void Main()
    {
        double angle = WaypointsMath.AngleBetween3Points(
            new Waypoint(29.8173748, 30.8253897),
            new Waypoint(29.8175575, 30.8253904),
            new Waypoint(29.8174481, 30.8254608)
        );

        Console.WriteLine("hello");



        // Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE);

        // float[] fitness = new float[population.Length];
        // for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
        // {
        //     fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
        //     Array.Sort(fitness, population);

        //     Genetic.Reproduce(population);
        // }

        // Console.WriteLine(fitness[0]);
        // WaypointPrinter.PrintWaypoints(population[0]);
    }
}