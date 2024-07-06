using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder
{
    public static class PayloadPathFinder
    {
        public static double[] FindOptimalPath(double[] beforeStart, double[] start, double[] target, double[,] fence)
        {
            MissionParams.BeforeStart = new Waypoint(beforeStart[0], beforeStart[1]);
            MissionParams.Start = new Waypoint(start[0], start[1]);
            MissionParams.Target = new Waypoint(target[0], target[1]);
            MissionParams.Fence = Array.ConvertAll(Enumerable.Range(0, fence.GetLength(0)).ToArray(), i => new Waypoint(fence[i, 0], fence[i, 1]));


            Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE, MissionParams.Target);

            float[] fitness = new float[population.Length];
            for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS; ++generationsCount)
            {
                fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
                Array.Sort(fitness, population);
                Genetic.Reproduce(population);
            }

            Console.WriteLine($"Shortest path found, Fitness value of: {fitness[0]}");
            return population[0].SelectMany(wp => new double[] { wp.Lat, wp.Long }).ToArray();
        }

    }
}
