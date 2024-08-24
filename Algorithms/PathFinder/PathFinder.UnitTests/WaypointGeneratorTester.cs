using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using PathFinder.Fundamentals;
using System.Collections.Generic;
using System.Linq;

namespace PathFinder.UnitTests
{
    [TestClass]
    public class WaypointGeneratorTester
    {
        [TestMethod]
        public void TestMethod1GenerateRandomWaypoint_6octFence_ReturnsWpIn6oct()
        {
            MissionParams.Fence = new Waypoint[]
            {
                new Waypoint(29.8931922, 30.8992195),
                new Waypoint(29.8597014, 30.9004211),
                new Waypoint(29.8653584, 30.9495163),
                new Waypoint(29.9007819, 30.9429932),
            };

            Waypoint wp = WaypointGenerator.GenerateRandomWaypoint();
            bool wpInsideFence = WaypointGenerator.IsPointInPolygon(wp, MissionParams.Fence);

            Assert.IsTrue(wpInsideFence);
        }

        // the under were made for test remove later
        [TestMethod]
        public void TestCalculateTurnRadius()
        {
            Waypoint A = new Waypoint(29.8150296, 30.8249760);
            Waypoint B = new Waypoint(29.8181759, 30.8247185);
            Waypoint C = new Waypoint(29.8167052, 30.8261561);

            (double requiredRadiusMeters, double arcLengthMeters, double theta) = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(A, B, C);

            double degTheta = ExtraMath.ToDeg(theta);
        }


        // ! REMOVE THIS
        //[TestMethod]
        //public void TestCalcualteTurnPoints()
        //{
            //Waypoint A = new Waypoint(29.8157743, 30.8245897);
            //Waypoint B = new Waypoint(29.8185482, 30.8250833);
            //Waypoint C = new Waypoint(29.8184924, 30.8272290);
            //Waypoint D = new Waypoint(29.8154392, 30.8260059);

            //List<Waypoint> wpsABC = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(A, B, C, 10);
            //List<Waypoint> wpsBCD = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(B, C, D, 10);

            //System.Diagnostics.Debug.WriteLine(WaypointPrinter.PrintWaypoints(wpsABC.ToArray()));
            //System.Diagnostics.Debug.WriteLine(WaypointPrinter.PrintWaypoints(wpsBCD.ToArray()));
        //}

        [TestMethod]
        public void TestCalcualteTurnPoints_Bezeir()
        {
            Waypoint A = new Waypoint(29.8176732, 30.8251691);
            Waypoint B = new Waypoint(29.8202982, 30.8263493);
            Waypoint C = new Waypoint(29.8194418, 30.8305979);
            Waypoint D = new Waypoint(29.8165376, 30.8289886);

            List<Waypoint> wpsABC = UavTurnerCalculator.CalculateTurningRadiusAndArcLengthUsingBezier(A, B, C, D, 10);

            System.Diagnostics.Debug.WriteLine(WaypointPrinter.PrintWaypoints(wpsABC.ToArray()));
        }
    }
}
