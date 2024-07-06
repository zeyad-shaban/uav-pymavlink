using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder
{
    public static class PayloadPathFinder
    {
        public static Waypoint[] FindOptimalPath((double lat, double longitude) beforeStart, (double lat, double longitude) start, (double lat, double longitude) target, (double lat, double longitude)[] fence)
        {
            MissionParams.BeforeStart = new Waypoint(beforeStart.lat, beforeStart.longitude);
            MissionParams.Start = new Waypoint(start.lat, start.longitude);
            MissionParams.Target = new Waypoint(target.lat, target.longitude);
            MissionParams.Fence = Array.ConvertAll(fence, item => new Waypoint(item.lat, item.longitude));


            Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE, MissionParams.Target);

            float[] fitness = new float[population.Length];
            for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
            {
                fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
                Array.Sort(fitness, population);
                // break;
                Genetic.Reproduce(population);
            }

            Console.WriteLine($"Shortest path found, Fitness value of: {fitness[0]}");
            return population[0];
        }
    }
}
