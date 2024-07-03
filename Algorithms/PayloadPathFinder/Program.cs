
class Program
{
    static void Main()
    {
        // Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE);

    // why the hell is this valid
        bool valid = WaypointsMath.IsValidTurn(
            new Waypoint(29.81908139, 30.82646263),
            new Waypoint(29.81913072, 30.82646627),
            new Waypoint(29.81882443, 30.82655179)
        );
        // how is this even a possible solution it scord 343
        Waypoint[][] population = [
            [
                new Waypoint(29.81771463,30.82618236),
                new Waypoint(29.81805509,30.8263451),
                new Waypoint(29.81797865,30.82632255),
                new Waypoint(29.81821343,30.82639919),
                new Waypoint(29.81867237,30.8265383),
                new Waypoint(29.81908139,30.82646263),
                new Waypoint(29.81913072,30.82646627),
                new Waypoint(29.81882443,30.82655179),
                new Waypoint(29.81937615,30.826484),
                new Waypoint(29.81945604,30.82649934)
            ]
        ];

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