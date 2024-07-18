using Microsoft.VisualStudio.TestTools.UnitTesting;
using PathFinder.Fundamentals;

using System;

namespace PathFinder.UnitTests
{
    [TestClass]
    public class ObstacleCalcTester
    {
        [TestMethod]
        public void IsNearObstacle_ObstacleInStraightLine_ReturnsFalse()
        {
            Waypoint a = new Waypoint(29.8150389, 30.8256090);
            Waypoint b = new Waypoint(29.8158395, 30.8256197);
            Waypoint c = new Waypoint(29.8167052, 30.8256841);
            Waypoint[] obs = new Waypoint[] { new Waypoint(29.8164492, 30.8256707) };

            bool valid = ObstacleCalc.IsPathValidWithObstacles(obs, a, b, c);

            Assert.IsFalse(valid);
        }

        [TestMethod]
        public void IsNearObstacle_ObstacleAway_ReturnsTrue()
        {

            Waypoint a = new Waypoint(29.8150389, 30.8256090);
            Waypoint b = new Waypoint(29.8158395, 30.8256197);
            Waypoint c = new Waypoint(29.8167052, 30.8256841);
            Waypoint[] obs = new Waypoint[] { new Waypoint(29.8160536, 30.8271003) };

            bool valid = ObstacleCalc.IsPathValidWithObstacles(obs, a, b, c);

            Assert.IsTrue(valid);
        }

        [TestMethod]
        public void IsNearObstacle_ObstacleInArc_ReturnsFalse()
        {
            Waypoint a = new Waypoint(29.8169937, 30.8253515);
            Waypoint b = new Waypoint(29.8178408, 30.8253729);
            Waypoint c = new Waypoint(29.8179060, 30.8266497);
            Waypoint[] obs = new Waypoint[] { new Waypoint(29.8184412, 30.8259684) };

            bool valid = ObstacleCalc.IsPathValidWithObstacles(obs, a, b, c);

            Assert.IsFalse(valid);
        }
    }
}
