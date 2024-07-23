using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using PathFinder.Fundamentals;

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
    }
}
