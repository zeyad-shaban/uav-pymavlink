using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    public static class UavTurnerCalculator
    {
        private const double EarthRadiusKm = 6371.0;

        public static (double requiredRadiusMeters, double arcLengthMeters, double theta) CalculateTurningRadiusAndArcLength(Waypoint A, Waypoint B, Waypoint C)
        {
            //onvert latitude and longitude from degrees to radians
            double latA = ExtraMath.ToRadians(A.Lat);
            double lonA = ExtraMath.ToRadians(A.Long);
            double latB = ExtraMath.ToRadians(B.Lat);
            double lonB = ExtraMath.ToRadians(B.Long);
            double latC = ExtraMath.ToRadians(C.Lat);
            double lonC = ExtraMath.ToRadians(C.Long);

            //alculate vectors in meters using Haversine formula approximation
            var AB = (x: (latB - latA) * EarthRadiusKm * 1000, y: (lonB - lonA) * EarthRadiusKm * Math.Cos(latA) * 1000);
            var BC = (x: (latC - latB) * EarthRadiusKm * 1000, y: (lonC - lonB) * EarthRadiusKm * Math.Cos(latB) * 1000);

            //alculate magnitudes
            double magAB = Math.Sqrt(AB.x * AB.x + AB.y * AB.y);
            double magBC = Math.Sqrt(BC.x * BC.x + BC.y * BC.y);

            //alculate dot product
            double dotProduct = AB.x * BC.x + AB.y * BC.y;

            //alculate the angle between vectors
            double cosTheta = dotProduct / (magAB * magBC);
            double theta = Math.Acos(cosTheta);

            bool ontopOfEachOther = Double.IsNaN(theta);
            bool isStraightLine = Math.Abs(theta) <= 1e-6;

            if (ontopOfEachOther) theta = 0;
            double requiredRadius = ontopOfEachOther ? 1 / theta : magBC / (2 * Math.Sin(theta / 2));

            //alculate the arc length
            double arcLength = isStraightLine || ontopOfEachOther ? magBC : requiredRadius * theta;

            return (requiredRadius, arcLength, Double.IsNaN(theta) ? 0 : theta);
        }

        // REMOVE ANYTHING UNDER THIS
        public static List<Waypoint> CalculateTurningRadiusAndArcLength(Waypoint A, Waypoint B, Waypoint C, int numberOfPoints)
        {
            var (requiredRadius, arcLength, theta) = CalculateTurningRadiusAndArcLength(A, B, C);
            requiredRadius /= 100;

            List<Waypoint> waypoints = new List<Waypoint>();

            double initialBearingAB = ExtraMath.GetBearing2Points(A.Lat, A.Long, B.Lat, B.Long);
            double finalBearingBC = ExtraMath.GetBearing2Points(B.Lat, B.Long, C.Lat, C.Long);

            double angleBisector = (initialBearingAB + finalBearingBC) / 2;
            double latCenter = B.Lat + (requiredRadius / EarthRadiusKm) * Math.Cos(ExtraMath.ToRadians(angleBisector));
            double lonCenter = B.Long + (requiredRadius / EarthRadiusKm) * Math.Sin(ExtraMath.ToRadians(angleBisector)) / Math.Cos(ExtraMath.ToRadians(B.Lat));

            for (int i = 0; i < numberOfPoints; i++)
            {
                double fraction = (double)i / (numberOfPoints - 1);
                double angleAtPoint = theta * fraction;

                double latPoint = latCenter + (requiredRadius / EarthRadiusKm) * Math.Cos(ExtraMath.ToRadians(initialBearingAB + angleAtPoint));
                double lonPoint = lonCenter + (requiredRadius / EarthRadiusKm) * Math.Sin(ExtraMath.ToRadians(initialBearingAB + angleAtPoint)) / Math.Cos(ExtraMath.ToRadians(latCenter));

                waypoints.Add(new Waypoint(latPoint, lonPoint));
            }

            return waypoints;
        }

        public static List<Waypoint> CalculateTurningRadiusAndArcLengthUsingBezier(Waypoint A, Waypoint B, Waypoint C, Waypoint D, int numberOfPoints)
        {
            List<Waypoint> waypoints = new List<Waypoint>();

            for (int i = 0; i < numberOfPoints; i++)
            {
                double t = (double)i / (numberOfPoints - 1);
                double lat = Math.Pow(1 - t, 3) * A.Lat +
                             3 * Math.Pow(1 - t, 2) * t * B.Lat +
                             3 * (1 - t) * Math.Pow(t, 2) * C.Lat +
                             Math.Pow(t, 3) * D.Lat;

                double lon = Math.Pow(1 - t, 3) * A.Long +
                             3 * Math.Pow(1 - t, 2) * t * B.Long +
                             3 * (1 - t) * Math.Pow(t, 2) * C.Long +
                             Math.Pow(t, 3) * D.Long;

                waypoints.Add(new Waypoint(lat, lon));
            }

            return waypoints;
        }

    }
}
