public static class WaypointsMath
{
    public static double ToRadians(double degrees)
    {
        return degrees * Math.PI / 180;
    }


    public static double AngleBetween3Points(Waypoint p, Waypoint q, Waypoint r)
    { // where p1 is the center
        double a = Math.Sqrt(Math.Pow(p.Lat - q.Lat, 2) + Math.Pow(q.Long - q.Long, 2));
        double b = Math.Sqrt(Math.Pow(p.Lat - r.Lat, 2) + Math.Pow(p.Long - r.Long, 2));
        double c = Math.Sqrt(Math.Pow(q.Lat - r.Lat, 2) + Math.Pow(q.Long - r.Long, 2));



        
        double angle = 0;

        return angle;
    }
}