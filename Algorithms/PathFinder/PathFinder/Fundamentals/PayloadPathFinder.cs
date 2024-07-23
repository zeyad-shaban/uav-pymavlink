using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace PathFinder.Fundamentals
{
    public static class PayloadPathFinder
    {
        public static double[,] FindOptimalPath(double[,] obs, double[] beforeStart, double[] start, double[] target, double[,] fence, int MAX_EXECUTE_TIME, float H1, float Vpa, float Vag, float angle)
        {
            DesignParams.H1 = H1;
            DesignParams.Vpa = Vpa;
            DesignParams.Vag = Vag;
            DesignParams.angle = angle;

            if (obs != null) MissionParams.Obstacles = Array.ConvertAll(Enumerable.Range(0, obs.GetLength(0)).ToArray(), i => new Waypoint(obs[i, 0], obs[i, 1]));

            MissionParams.BeforeStart = new Waypoint(beforeStart[0], beforeStart[1]);
            MissionParams.Start = new Waypoint(start[0], start[1]);
            MissionParams.Target = new Waypoint(target[0], target[1]);

            if (fence != null) MissionParams.Fence = Array.ConvertAll(Enumerable.Range(0, fence.GetLength(0)).ToArray(), i => new Waypoint(fence[i, 0], fence[i, 1]));

            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();

            Waypoint[][] population = Genetic.CreatePopulation(CodeParams.CHROMOSOME_SIZE, MissionParams.Target);
            float[] fitness = new float[population.Length];

            for (int generationsCount = 0; generationsCount < CodeParams.MAX_GENERATIONS && stopwatch.Elapsed.TotalSeconds < MAX_EXECUTE_TIME; ++generationsCount)
            {
                fitness = Genetic.MeasureFitness(fitness, population, MissionParams.BeforeStart, MissionParams.Start, MissionParams.Target);
                Array.Sort(fitness, population);
                Genetic.Reproduce(population);

                Console.WriteLine($"Generation: {generationsCount}/{CodeParams.MAX_GENERATIONS}, Best: {fitness[0]}, Time: {stopwatch.Elapsed.TotalSeconds}/{MAX_EXECUTE_TIME} seconds");
            }

            System.Diagnostics.Debug.WriteLine($"Shortest path found, Fitness value of: {fitness[0]}");
            Console.WriteLine($"Shortest path found, Fitness value of: {fitness[0]}");
            return ConvertChromosomeToDoubles(population[0]);
        }
        public static double[,] ConvertChromosomeToDoubles(Waypoint[] chromosome)
        {
            int chromosomeSize = chromosome.Length;
            double[,] result = new double[chromosomeSize, 2];

            for (int i = 0; i < chromosomeSize; i++)
            {
                result[i, 0] = chromosome[i].Lat;
                result[i, 1] = chromosome[i].Long;
            }

            return result;
        }
    }
}