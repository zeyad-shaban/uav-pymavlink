using Microsoft.VisualStudio.TestTools.UnitTesting;
using PathFinder.Fundamentals;
using System;

namespace PathFinder.UnitTests
{
    [TestClass]
    public class ExtraMathTester
    {
        [TestMethod]
        public void WaypointMover_MoveNorth50Meters_ReturnsSpecificWp()
        {
            Waypoint wp = new Waypoint(29.8170123, 30.8274221);

            Waypoint movedWp = ExtraMath.WaypointMover(wp, 50, 0);

            Assert.IsTrue(movedWp.Lat == 29.817461960802959 && movedWp.Long == 30.8274221);
        }

        [TestMethod]
        public void WaypointMover_ExceedFence_ReturnsInFenceTrue()
        {
            Waypoint wp = new Waypoint(29.8183202, 30.8253890);

            Waypoint movedWp = ExtraMath.WaypointMover(wp, 100, 270);
            bool insideFence = ExtraMath.IsInsideFence(wp.Lat, wp.Long);

            Assert.IsTrue(insideFence && movedWp.Lat == 29.818320195941169 && movedWp.Long == 30.824704873892152);
        }
    }
}
