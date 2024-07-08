using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    public class Genetic
    {
        public static Waypoint[][] CreatePopulation(int chromosomeSize, Waypoint target)
        {
            Random random = new Random();
            Waypoint[][] population = new Waypoint[CodeParams.POPULATION_SIZE][];

            for (int i = 0; i < population.Length; ++i)
            {
                population[i] = new Waypoint[chromosomeSize + 1];
                for (int geneIdx = 0; geneIdx < chromosomeSize; ++geneIdx)
                {
                    population[i][geneIdx] = WaypointGenerator.GenerateRandomWaypoint();
                }
                population[i][chromosomeSize] = new Waypoint(target.Lat, target.Long, random.Next(0, 360), true);
            }

            return population;
        }

        public static float[] MeasureFitness(float[] fitness, Waypoint[][] population, Waypoint beforeStart, Waypoint start, Waypoint target)
        {
            int invalidTurnPenality = 3000;
            int toTargetThetaPenalityMult = 300;
            int throwWpSpacingPenalityMult = 5;

            for (int indivIdx = 0; indivIdx < population.Length; ++indivIdx)
            {
                double score = 0;
                double requiredRadius;
                double arcLength;
                Waypoint[] individual = population[indivIdx];

                for (int wpIdx = 0; wpIdx < population[indivIdx].Length; ++wpIdx)
                {
                    Waypoint currWaypoint = individual[wpIdx];
                    Waypoint before = wpIdx == 0 ? start : individual[wpIdx - 1];
                    Waypoint beforeBefore = wpIdx == 0 ? beforeStart : (wpIdx == 1 ? start : individual[wpIdx - 2]);

                    (requiredRadius, arcLength, _) = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(beforeBefore, before, currWaypoint);
                    if (requiredRadius < DesignParams.MIN_TURN_RADIUS) score += invalidTurnPenality;
                    score += arcLength;
                }

                (_, _, double thetaToTarget) = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(individual[individual.Length - 2], individual[individual.Length - 1], target);
                score += toTargetThetaPenalityMult * ExtraMath.ToDeg(thetaToTarget);

                //double distance = ExtraMath.GetDistance2Wps(individual[individual.Length - 1], individual[individual.Length - 2]);
                //if (distance < 70)
                //{
                //    score += (70 - distance) * throwWpSpacingPenalityMult; // penaltyFactor is a value you determine through experimentation
                //}

                fitness[indivIdx] = (float)score;
            }

            return fitness;
        }

        public static void Reproduce(Waypoint[][] population)
        {
            Random random = new Random();
            int targetKill = (int)(population.Length * CodeParams.REPLACE_RATE);
            int targetElite = (int)(population.Length * CodeParams.ELITE_RATE);

            int offspringIdx = targetKill;
            for (int i = 0; i < targetElite; ++i)
            {
                Waypoint[] parentA = population[i];
                Waypoint[] parentB = population[++i];

                (Waypoint[] offspringA, Waypoint[] offspringB) = CrossOver(parentA, parentB, random);

                population[offspringIdx++] = offspringA;
                population[offspringIdx++] = offspringB;
            }

            while (true)
            {
                Waypoint[] parentA = population[random.Next(0, targetKill)];
                Waypoint[] parentB = population[random.Next(0, targetKill)];

                (Waypoint[] offspringA, Waypoint[] offspringB) = CrossOver(parentA, parentB, random);

                population[offspringIdx++] = offspringA;
                if (offspringIdx >= population.Length) break;
                population[offspringIdx++] = offspringB;
                if (offspringIdx >= population.Length) break;

            }
        }

        private static (Waypoint[] offspringA, Waypoint[] offspringB) CrossOver(Waypoint[] parentA, Waypoint[] parentB, Random random = null)
        {
            if (random == null) random = new Random();
            bool shouldMutateA = random.NextDouble() < CodeParams.INDIVIDUAL_MUTATE_RATE;
            bool shouldMutateB = random.NextDouble() < CodeParams.INDIVIDUAL_MUTATE_RATE;

            Waypoint[] offspringA = new Waypoint[parentA.Length];
            Waypoint[] offspringB = new Waypoint[parentA.Length];

            for (int geneIdx = 0; geneIdx < offspringA.Length; ++geneIdx)
            {
                offspringA[geneIdx] = random.Next(0, 2) == 0 ? parentA[geneIdx] : parentB[geneIdx];
                if (shouldMutateA && random.NextDouble() < CodeParams.GENE_MUTATE_RATE)
                {
                    if (geneIdx != CodeParams.CHROMOSOME_SIZE) offspringA[geneIdx] = ExtraMath.WaypointMover(offspringA[geneIdx], random.Next(1,75), random.Next(0, 360));
                    else offspringA[geneIdx] = new Waypoint(0, 0, random.Next(0, 360), true);
                }

                // B
                offspringB[geneIdx] = random.Next(0, 2) == 1 ? parentA[geneIdx] : parentB[geneIdx];
                if (shouldMutateB && random.NextDouble() < CodeParams.GENE_MUTATE_RATE)
                {
                    if (geneIdx != CodeParams.CHROMOSOME_SIZE) offspringB[geneIdx] = ExtraMath.WaypointMover(offspringA[geneIdx], random.Next(1,75), random.Next(0, 360));
                    else offspringB[geneIdx] = new Waypoint(0, 0, random.Next(0, 360), true);
                }
            }

            return (offspringA, offspringB);
        }
    }
}
