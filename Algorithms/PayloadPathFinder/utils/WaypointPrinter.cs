using System.Text;

public static class WaypointPrinter
{
    public static void PrintWaypoints(Waypoint[] waypoints)
    {
        StringBuilder sb = new StringBuilder();
        sb.AppendLine("QGC WPL 110");
        sb.AppendLine("0\t1\t0\t16\t0\t0\t0\t0\t29.8177921\t30.8277948\t100.000000\t1");

        for (int i = 0; i < waypoints.Length; i++)
        {
            sb.AppendLine($"{i + 1}\t0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t{waypoints[i].Lat:F8}\t{waypoints[i].Long:F8}\t100.000000\t1");
        }

        Console.WriteLine(sb.ToString());
    }
}