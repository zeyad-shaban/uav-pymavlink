using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Utils
{
    internal static class ExtraMath
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
}
