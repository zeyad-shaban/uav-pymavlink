public static class ExtraMath
{
    public static double ToRadians(double degrees)
    {
        return degrees * (Math.PI / 180);
    }
    public static double ToDeg(double radians)
    {
        return radians * (180.0 / Math.PI);
    }
}