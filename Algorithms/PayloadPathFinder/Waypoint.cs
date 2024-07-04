public class Waypoint
{
    public double Lat;
    public double Long;
    public double DropAngle;
    public bool isDropTarget = false;

    public Waypoint(double lat, double longitude, double DropAngle = 0)
    {
        if (DropAngle != 0)
        {
            Waypoint wp = PayloadCalculator.CalculateDropPoint(new Waypoint(lat, longitude), DropAngle);
            lat = wp.Lat;
            longitude = wp.Long;
            isDropTarget = true;
        }

        Lat = lat;
        Long = longitude;
        this.DropAngle = DropAngle;
    }
}