public static class WaypointsMath
{
    public static bool IsValidTurn(Waypoint p1, Waypoint p2, Waypoint p3) => GetArcRadius(p1, p2, p3) > DesignParams.MIN_TURN_RADIUS_IN_METERS;

    public static double GetArcRadius(Waypoint p1, Waypoint p2, Waypoint p3)
    {
        double a = GetDistanceBetweenWaypoints(p1, p2);
        double b = GetDistanceBetweenWaypoints(p2, p3);
        double c = GetDistanceBetweenWaypoints(p1, p3);

        // Semi-perimeter of the triangle
        double s = (a + b + c) / 2;

        // Area of the triangle using Heron's formula
        double area = Math.Sqrt(s * (s - a) * (s - b) * (s - c));

        // Circumradius (R) formula: R = (a * b * c) / (4 * area)
        double radius = (a * b * c) / (4 * area);

        return radius;
    }

    public static double AngleBetween3Points(Waypoint p, Waypoint center, Waypoint r)
    {
        double a = GetDistanceBetweenWaypoints(center, p);
        double b = GetDistanceBetweenWaypoints(p, r);
        double c = GetDistanceBetweenWaypoints(center, r);

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

    public static double GetCentralAngle(Waypoint p1, Waypoint p2, Waypoint p3)
    {
        double b = GetDistanceBetweenWaypoints(p2, p3);
        double radius = GetArcRadius(p1, p2, p3);

        double centralAngle = 2 * Math.Asin(b / (2 * radius));

        return centralAngle;
    }

    public static double GetArcLengthLast2Wp(Waypoint p1, Waypoint p2, Waypoint p3)
    {
        double radius = GetArcRadius(p1, p2, p3);
        double centralAngle = GetCentralAngle(p1, p2, p3);

        double arcLength = radius * centralAngle;

        return arcLength;
    }


    private static double DegreesToRadians(double degrees)
    {
        return degrees * Math.PI / 180;
    }
}