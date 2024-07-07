using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    internal static class PayloadCalculator
    {
        private const double EarthRadiusKm = 6371.0;

        private static (double x, double y) PayloadDropEq(double H1, double Vpa, double Vag, double angle)
        {
            double g = 9.81;  // acceleration due to gravity
            double Cd = 0.5;  // drag coefficient of payloads
            double rho = 1.225;  // density of air
            double A = 0.02;  // average cross section of the payload
            double m = 1;  // mass of the payload
            List<double> H = new List<double>(new double[] { H1 });  // height of the plane in meters
            List<double> ty = new List<double>(new double[] { 0 });  // duration of fall
            List<double> Vy = new List<double>(new double[] { 0 });  // velocity in downward direction
            List<double> acc = new List<double>(new double[] { 9.81 });  // acceleration in downward direction
            List<double> Dy = new List<double>(new double[] { 0 });  // upward drag force
            List<double> dy = new List<double>(new double[] { 0 });  // deceleration due to drag force
            int k = 1;
            double interval = 0.001;  // time intervals for calculation in the loops

            while (H[k - 1] > 0)
            {
                ty.Add(ty[k - 1] + interval);
                H.Add(H[k - 1] - (Vy[k - 1] * interval + 0.5 * acc[k - 1] * Math.Pow(interval, 2)));
                Vy.Add(Vy[k - 1] + acc[k - 1] * interval);
                Dy.Add(Cd * rho * Math.Pow(Vy[k - 1], 2) * A / 2);
                dy.Add(Dy[k - 1] / m);
                acc.Add(g - dy[k]);
                k++;
            }

            double Vpg = Vpa - Vag * Math.Cos(ExtraMath.ToRadians(angle));  // velocity of plane wrt ground
            List<double> Vx = new List<double>(new double[] { Vpg });  // velocity of payload in horizontal direction
            List<double> R = new List<double>(new double[] { 0 });  // distance covered by payload in horizontal direction
            List<double> Dx = new List<double>(new double[] { Cd * rho * Math.Pow(Vx[0], 2) * A / 2 });  // horizontal drag on the payload
            List<double> dx = new List<double>(new double[] { Dx[0] / m });  // horizontal deceleration on the payload
            k = 1;

            Vx.AddRange(new double[ty.Count - 1]);
            R.AddRange(new double[ty.Count - 1]);
            Dx.AddRange(new double[ty.Count - 1]);
            dx.AddRange(new double[ty.Count - 1]);

            for (int tx = 0; tx < ty.Count - 1; tx++)
            {
                R[k] = R[k - 1] + (Vx[k - 1] * interval - 0.5 * dx[k - 1] * Math.Pow(interval, 2));
                Vx[k] = Vx[k - 1] - dx[k - 1] * interval;
                Dx[k] = Cd * rho * 0.5 * A * Math.Pow(Vx[k], 2);
                dx[k] = Dx[k] / m;
                k++;
            }

            double x = R[k - 1];
            double y = H1;
            return (x, y);
        }

        public static Waypoint CalculateDropPoint(double angle)
        {
            Waypoint target = MissionParams.Target;

            var (distance, _) = PayloadDropEq(DesignParams.H1, DesignParams.Vpa, DesignParams.Vag, DesignParams.angle);

            // Calculate the new waypoint position
            double bearing = ExtraMath.ToRadians(angle);  // Convert bearing to radians
            double lat1 = ExtraMath.ToRadians(target.Lat);
            double lon1 = ExtraMath.ToRadians(target.Long);

            double lat2 = Math.Asin(Math.Sin(lat1) * Math.Cos(distance / 1000 / EarthRadiusKm) +
                                    Math.Cos(lat1) * Math.Sin(distance / 1000 / EarthRadiusKm) * Math.Cos(bearing));
            double lon2 = lon1 + Math.Atan2(Math.Sin(bearing) * Math.Sin(distance / 1000 / EarthRadiusKm) * Math.Cos(lat1),
                                            Math.Cos(distance / 1000 / EarthRadiusKm) - Math.Sin(lat1) * Math.Sin(lat2));

            // Convert radians back to degrees
            lat2 = ExtraMath.ToDeg(lat2);
            lon2 = ExtraMath.ToDeg(lon2);

            return new Waypoint(lat2, lon2);
        }
    }
}
