public static class WaypointsMath
{
    public static bool IsBelowMaxTurnRadius()
    {
        // edit this function, and please provide a full solution fo the function and use all the parameters you need
    }
    public static double AngleBetween3Points(Waypoint p, Waypoint center, Waypoint r)
    {
        double a = HaversineDistance(center, p);
        double b = HaversineDistance(p, r);
        double c = HaversineDistance(center, r);

        double angle = Math.Acos((Math.Pow(a, 2) + Math.Pow(c, 2) - Math.Pow(b, 2)) / (2 * a * c));

        return angle; //  * 180 / Math.PI; // uncomment to return degrees instead of rad
    }

    public static double GetDistanceBetweenWaypoints(Waypoint point1, Waypoint point2)
    {
        double R = 6371e3; // Earth's radius in meters

        double lat1Rad = DegreesToRadians(point1.Lat);
        double lat2Rad = DegreesToRadians(point2.Lat);
        double deltaLatRad = DegreesToRadians(point2.Lat - point1.Lat);
        double deltaLonRad = DegreesToRadians(point2.Long - point1.Long);

        double a = Math.Sin(deltaLatRad / 2) * Math.Sin(deltaLatRad / 2) +
                   Math.Cos(lat1Rad) * Math.Cos(lat2Rad) *
                   Math.Sin(deltaLonRad / 2) * Math.Sin(deltaLonRad / 2);

        double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));

        return R * c;
    }

    private static double HaversineDistance(Waypoint point1, Waypoint point2)
    {
        double R = 6371e3; // Earth's radius in meters

        double lat1Rad = DegreesToRadians(point1.Lat);
        double lat2Rad = DegreesToRadians(point2.Lat);
        double deltaLatRad = DegreesToRadians(point2.Lat - point1.Lat);
        double deltaLonRad = DegreesToRadians(point2.Long - point1.Long);

        double a = Math.Sin(deltaLatRad / 2) * Math.Sin(deltaLatRad / 2) +
                   Math.Cos(lat1Rad) * Math.Cos(lat2Rad) *
                   Math.Sin(deltaLonRad / 2) * Math.Sin(deltaLonRad / 2);

        double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));

        return R * c;
    }

    private static double DegreesToRadians(double degrees)
    {
        return degrees * Math.PI / 180;
    }
}