using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using PathFinder.Fundamentals;

namespace PathFinder.Fundamentals
{
    static public class ObstacleCalc
    {
        private const double R = 6371e3; // Earth's radius in meters

        public static bool IsPathValidWithObstacles(Waypoint[] obstacles, Waypoint A, Waypoint B, Waypoint C)
        {
            // Calculate turning arc
            var (requiredRadius, arcLength, theta) = UavTurnerCalculator.CalculateTurningRadiusAndArcLength(A, B, C);

            foreach (var obstacle in obstacles)
            {
                if (IsPointNearArc(obstacle, B, C, requiredRadius, theta))
                {
                    return false; // Collision detected
                }
            }

            return true; // No collision detected
        }


        static bool IsPointNearArc(Waypoint point, Waypoint arcStart, Waypoint arcEnd, double arcRadius, double arcTheta)
        {
            // Convert latitude and longitude from degrees to radians
            double latPoint = ExtraMath.ToRadians(point.Lat);
            double lonPoint = ExtraMath.ToRadians(point.Long);
            double latStart = ExtraMath.ToRadians(arcStart.Lat);
            double lonStart = ExtraMath.ToRadians(arcStart.Long);
            double latEnd = ExtraMath.ToRadians(arcEnd.Lat);
            double lonEnd = ExtraMath.ToRadians(arcEnd.Long);

            // Calculate vector from arc start to point
            var vectorToPoint = (x: (latPoint - latStart) * R, y: (lonPoint - lonStart) * R * Math.Cos(latStart));

            // Calculate the distance from the arc start to the point
            double distanceToPoint = Math.Sqrt(vectorToPoint.x * vectorToPoint.x + vectorToPoint.y * vectorToPoint.y);

            // If the path is a straight line, check the distance directly
            if (double.IsInfinity(arcRadius))
            {
                return distanceToPoint <= MissionParams.obstacleRadius;
            }

            // Calculate the angle subtended by the point with respect to the arc center
            double angleToPoint = distanceToPoint / arcRadius;

            // Check if the point is within the obstacle radius from the arc
            return distanceToPoint <= arcRadius + MissionParams.obstacleRadius && angleToPoint <= arcTheta;
        }
    }
}