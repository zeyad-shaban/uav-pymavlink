using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    internal static class UavTurnerCalculator
    {
        private const double EarthRadiusKm = 6371.0;

        public static (double requiredRadiusMeters, double arcLengthMeters, double theta) CalculateTurningRadiusAndArcLength(Waypoint A, Waypoint B, Waypoint C)
        {
            // Convert latitude and longitude from degrees to radians
            double latA = ExtraMath.ToRadians(A.Lat);
            double lonA = ExtraMath.ToRadians(A.Long);
            double latB = ExtraMath.ToRadians(B.Lat);
            double lonB = ExtraMath.ToRadians(B.Long);
            double latC = ExtraMath.ToRadians(C.Lat);
            double lonC = ExtraMath.ToRadians(C.Long);

            // Calculate vectors in meters using Haversine formula approximation
            var AB = (x: (latB - latA) * EarthRadiusKm * 1000, y: (lonB - lonA) * EarthRadiusKm * Math.Cos(latA) * 1000);
            var BC = (x: (latC - latB) * EarthRadiusKm * 1000, y: (lonC - lonB) * EarthRadiusKm * Math.Cos(latB) * 1000);

            // Calculate magnitudes
            double magAB = Math.Sqrt(AB.x * AB.x + AB.y * AB.y);
            double magBC = Math.Sqrt(BC.x * BC.x + BC.y * BC.y);

            // Calculate dot product
            double dotProduct = AB.x * BC.x + AB.y * BC.y;

            // Calculate the angle between vectors
            double cosTheta = dotProduct / (magAB * magBC);
            double theta = Math.Acos(cosTheta);

            bool ontopOfEachOther = Double.IsNaN(theta);
            bool isStraightLine = Math.Abs(theta) <= 1e-6;

            if (ontopOfEachOther) theta = 0;
            double requiredRadius = ontopOfEachOther ? 1 / theta : magBC / (2 * Math.Sin(theta / 2));

            // Calculate the arc length
            double arcLength = isStraightLine || ontopOfEachOther ? magBC : requiredRadius * theta;

            return (requiredRadius, arcLength, Double.IsNaN(theta) ? 0 : theta);
        }
    }
}
