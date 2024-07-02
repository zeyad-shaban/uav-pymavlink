
class Program
{
    static void Main()
    {
        Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE);

        double angle = WaypointsMath.AngleBetween3Points(
        new Waypoint(5, 0),
        new Waypoint(0, 0),
        new Waypoint(5, 5)

// new Waypoint(29.8186972, 30.8258772), // center
// new Waypoint(29.8167331, 30.8255768),
// new Waypoint(29.8185668, 30.8278835)
        );
        Console.WriteLine(angle);

        for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
        {
            // float[] fitness = Genetic.MeasureFitness(population);
        }
    }
}