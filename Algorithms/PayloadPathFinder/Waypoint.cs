public class Waypoint
{
    public double Lat;
    public double Long;
    public double DropAngle;
    public bool IsDropTarget = false;

    public Waypoint(double lat, double longitude, double dropAngle = 0, bool isDropTarget = false)
    {
        if (isDropTarget)
        {
            Waypoint wp = PayloadCalculator.CalculateDropPoint(new Waypoint(lat, longitude), DropAngle);
            lat = wp.Lat;
            longitude = wp.Long;
        }

        Lat = lat;
        Long = longitude;
        DropAngle = dropAngle;
        IsDropTarget = isDropTarget;
    }
}