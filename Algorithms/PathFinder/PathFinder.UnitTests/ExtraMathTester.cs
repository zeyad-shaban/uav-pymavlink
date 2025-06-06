﻿using Microsoft.VisualStudio.TestTools.UnitTesting;
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
        public void IsInsideFence_Inside_ReturnsTrue()
        {
            MissionParams.Fence = new Waypoint[]
{
                new Waypoint(29.8196652,  30.8248472),
                new Waypoint(29.8184924,  30.8315635),
                new Waypoint(29.8105055,  30.8300400),
                new Waypoint(29.8117343,  30.8227229),
            };

            Waypoint wp = new Waypoint(29.8189485, 30.8272719);

            bool insideFence = ExtraMath.IsInsideFence(wp.Lat, wp.Long);

            Assert.IsTrue(insideFence);
        }

        [TestMethod]
        public void IsInsideFence_Outside_ReturnsFalse()
        {
            Waypoint wp = new Waypoint(29.821668643211844, 30.8271861);

            bool insideFence = ExtraMath.IsInsideFence(wp.Lat, wp.Long);

            Assert.IsFalse(insideFence);
        }

        [TestMethod]
        public void WaypointMover_ExceedFenceWest_ReturnsInFenceTrue()
        {
            Waypoint wp = new Waypoint(29.8183202, 30.8253890);

            Waypoint movedWp = ExtraMath.WaypointMover(wp, 100, 270);
            bool insideFence = ExtraMath.IsInsideFence(wp.Lat, wp.Long);

            Assert.IsTrue(insideFence);
        }

        [TestMethod]
        public void WaypointMover_ExceedFenceNorth_ReturnsInFenceTrue()
        {
            MissionParams.Fence = new Waypoint[] {
                new Waypoint(29.8280982,  30.8213282),
                new Waypoint(29.8255293,  30.8457899),
                new Waypoint(29.8097793,  30.8419704),
                new Waypoint(29.8154392,  30.8164358),
            };
            Waypoint wp = new Waypoint(29.8198700, 30.8271861);

            Waypoint movedWp = ExtraMath.WaypointMover(wp, 200, 0);
            bool insideFence = ExtraMath.IsInsideFence(movedWp.Lat, movedWp.Long);

            Assert.IsTrue(insideFence);
        }

        [TestMethod]
        public void DistanceWaypoint_Wp1And2_DistInMeters()
        {
            Waypoint wp1 = new Waypoint(29.8162165, 30.8304209);
            Waypoint wp2 = new Waypoint(29.8172962, 30.8309519);

            double distance = ExtraMath.GetDistance2Wps(wp1, wp2);

            Assert.IsTrue(distance == 130.52988379939222);
        }
    }
}
