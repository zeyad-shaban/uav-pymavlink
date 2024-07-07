using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    public static class ExtraMath
    {
        private const double R = 6371e3; // Earth's radius in meters

        public static double ToRadians(double degrees)
        {
            return degrees * (Math.PI / 180);
        }
        public static double ToDeg(double radians)
        {
            return radians * (180.0 / Math.PI);
        }

        public static Waypoint WaypointMover(Waypoint wp, double d, double brng)
        {
            const double stepSize = 1; // Step size in meters
            double newLat, newLong;

            (newLat, newLong) = CalculateNewWaypoint(wp.Lat, wp.Long, d, brng);

            while (!IsInsideFence(newLat, newLong))
            {
                (newLat, newLong) = CalculateNewWaypoint(newLat, newLong, stepSize, brng + 180);
            }

            return new Waypoint(newLat, newLong);
        }

        private static (double, double) CalculateNewWaypoint(double lat1, double long1, double d, double brng)
        {
            brng = ToRadians(brng);
            lat1 = ToRadians(lat1);
            long1 = ToRadians(long1);

            double lat2_r = Math.Asin(Math.Sin(lat1) * Math.Cos(d / R) + Math.Cos(lat1) * Math.Sin(d / R) * Math.Cos(brng));
            double long2_r = long1 + Math.Atan2(Math.Sin(brng) * Math.Sin(d / R) * Math.Cos(lat1), Math.Cos(d / R) - Math.Sin(lat1) * Math.Sin(lat2_r));

            return (ToDeg(lat2_r), ToDeg(long2_r));
        }

        public static bool IsInsideFence(double lat, double lon)
        {
            Waypoint[] Fence = MissionParams.Fence;
            int n = Fence.Length;
            bool inside = false;
            for (int i = 0, j = n - 1; i < n; j = i++)
            {
                if (((Fence[i].Long > lon) != (Fence[j].Long > lon)) &&
                    (lat < (Fence[j].Lat - Fence[i].Lat) * (lon - Fence[i].Long) / (Fence[j].Long - Fence[i].Long) + Fence[i].Lat))
                {
                    inside = !inside;
                }
            }
            return inside;
        }
    }
}