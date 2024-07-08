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
            Waypoint newWp = CalculateWaypoint(wp.Lat, wp.Long, d, brng);
            if (!IsInsideFence(newWp.Lat, newWp.Long))
            {
                return FindPointWithinFence(wp.Lat, wp.Long, d, brng);
            }
            return newWp;
        }

        private static Waypoint CalculateWaypoint(double lat, double lon, double distance, double bearing)
        {
            double bearingRad = ToRadians(bearing);
            double latRad = ToRadians(lat);
            double lonRad = ToRadians(lon);

            double newLatRad = Math.Asin(Math.Sin(latRad) * Math.Cos(distance / R) +
                                         Math.Cos(latRad) * Math.Sin(distance / R) * Math.Cos(bearingRad));
            double newLonRad = lonRad + Math.Atan2(Math.Sin(bearingRad) * Math.Sin(distance / R) * Math.Cos(latRad),
                                                   Math.Cos(distance / R) - Math.Sin(latRad) * Math.Sin(newLatRad));

            double newLat = ToDeg(newLatRad);
            double newLon = ToDeg(newLonRad);

            return new Waypoint(newLat, newLon);
        }

        public static Waypoint FindPointWithinFence(double lat, double lon, double distance, double bearing)
        {
            double low = 0;
            double high = distance;
            Waypoint midWaypoint = null;

            while (high - low > 0.01) // Precision threshold
            {
                double mid = (low + high) / 2;
                midWaypoint = CalculateWaypoint(lat, lon, mid, bearing);

                if (IsInsideFence(midWaypoint.Lat, midWaypoint.Long))
                {
                    low = mid;
                }
                else
                {
                    high = mid;
                }
            }

            return midWaypoint;
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