using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Utils
{
    internal static class WaypointGenerator
    {
        private static Random random = new Random();

        public static Waypoint GenerateRandomWaypoint()
        {
            // Define the bounding box of the fence
            double minLat = Double.MaxValue, maxLat = Double.MinValue;
            double minLong = Double.MaxValue, maxLong = Double.MinValue;

            foreach (var point in MissionParams.Fence)
            {
                if (point.Lat < minLat) minLat = point.Lat;
                if (point.Lat > maxLat) maxLat = point.Lat;
                if (point.Long < minLong) minLong = point.Long;
                if (point.Long > maxLong) maxLong = point.Long;
            }

            Waypoint randomWaypoint;
            do
            {
                double randomLat = minLat + (maxLat - minLat) * random.NextDouble();
                double randomLong = minLong + (maxLong - minLong) * random.NextDouble();
                randomWaypoint = new Waypoint(randomLat, randomLong);
            }
            while (!IsPointInPolygon(randomWaypoint, MissionParams.Fence));

            return randomWaypoint;
        }

        private static bool IsPointInPolygon(Waypoint point, Waypoint[] polygon)
        {
            int n = polygon.Length;
            bool inside = false;

            for (int i = 0, j = n - 1; i < n; j = i++)
            {
                if (((polygon[i].Long > point.Long) != (polygon[j].Long > point.Long)) &&
                    (point.Lat < (polygon[j].Lat - polygon[i].Lat) * (point.Long - polygon[i].Long) / (polygon[j].Long - polygon[i].Long) + polygon[i].Lat))
                {
                    inside = !inside;
                }
            }

            return inside;
        }
    }
}
