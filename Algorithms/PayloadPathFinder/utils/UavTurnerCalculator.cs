public static class UavTurnerCalculator
{
    private const double EarthRadiusKm = 6371.0;

    public static (double requiredRadiusMeters, double arcLengthMeters) CalculateTurningRadiusAndArcLength(Waypoint A, Waypoint B, Waypoint C)
    {
        // Convert latitude and longitude from degrees to radians
        double latA = ToRadians(A.Lat);
        double lonA = ToRadians(A.Long);
        double latB = ToRadians(B.Lat);
        double lonB = ToRadians(B.Long);
        double latC = ToRadians(C.Lat);
        double lonC = ToRadians(C.Long);

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

        bool isStraightLine = Math.Abs(theta) <= 1e-6; // feel free to change this conditon as you like

        double requiredRadius = magBC / (2 * Math.Sin(theta / 2));

        // Calculate the arc length
        double arcLength = isStraightLine ? magBC : requiredRadius * theta;

        return (requiredRadius, arcLength);
    }

    private static double ToRadians(double degrees)
    {
        return degrees * (Math.PI / 180);
    }
}