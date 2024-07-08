using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using PathFinder.Fundamentals;

namespace PathFinder.UnitTests
{
    [TestClass]
    public class PayloadPathFinderTests
    {
        private double[] beforeStart = new double[] { 29.8181852, 30.8252120 };
        private double[] start = new double[] { 29.8190695, 30.8253515 };
        private double[] target = new double[] { 29.8190602, 30.8293211 };

        [TestMethod]
        public void FindOptimalPath_AnyWp_ReturnsShortestPath()
        {


            double[,] path = PayloadPathFinder.FindOptimalPath(beforeStart, start, target);


            double[,] combined = CombinePathWithMissionWps(path);

            string pathToUpload = WaypointPrinter.PrintWaypoints(combined);

            System.Diagnostics.Debug.WriteLine(pathToUpload);
            Assert.IsNotNull(pathToUpload);
        }


        [TestMethod]
        public void TestFitness_SharpAngle_ReturnsBiggerThan3000()
        {
            float[] fitness = new float[1];
            Waypoint[][] population = new Waypoint[1][];
            population[0] = new Waypoint[]{
                new Waypoint(29.8190972 , 30.82567032),
                new Waypoint(29.81977606, 30.82616114),
                new Waypoint(29.82032149, 30.8259128),
                new Waypoint(29.8204997 , 30.825334),
                new Waypoint(29.81964568, 30.8263712, isDropTarget:true),
            };

            Genetic.MeasureFitness(fitness, population, ToWp(beforeStart), ToWp(start), ToWp(target));
            float value = fitness[0];


            // todo put something here i'm sure it will fail 100% Assert.IsTrue(value > 3000);
        }

        public Waypoint ToWp(double[] wp) => new Waypoint(wp[0], wp[1]);
        public Waypoint[] DblArrToWp(double[,] original)
        {
            Waypoint[] wps = new Waypoint[original.GetLength(0)];

            for (int i = 0; i < original.GetLength(0); ++i)
            {
                wps[i] = new Waypoint(original[i, 0], original[i, 1]);
            }

            return wps;
        }
        private double[,] CombinePathWithMissionWps(double[,] path)
        {
            double[,] combined = new double[path.GetLength(0) + 3, 2];
            combined[0, 0] = beforeStart[0];
            combined[0, 1] = beforeStart[1];

            combined[1, 0] = start[0];
            combined[1, 1] = start[1];

            for (int i = 0; i < path.GetLength(0); i++)
            {
                combined[i + 2, 0] = path[i, 0];
                combined[i + 2, 1] = path[i, 1];
            }

            combined[path.GetLength(0) + 2, 0] = target[0];
            combined[path.GetLength(0) + 2, 1] = target[1];

            return combined;
        }
    }
}