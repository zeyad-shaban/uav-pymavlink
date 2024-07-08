using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    internal static class CodeParams
    {
        static public int POPULATION_SIZE = 20000;
        static public int CHROMOSOME_SIZE = 3;
        public static int MAX_GENERATIONS = 1000;

        public static float REPLACE_RATE = 0.7f;
        public static float INDIVIDUAL_MUTATE_RATE = 0.3f;
        public static float GENE_MUTATE_RATE = 0.8f;
        public static float GENE_MUTATE_ENTIRELY = 0.5f;
        static public float ELITE_RATE = 0.005f;
    }

    internal static class MissionParams
    {
        static public Waypoint BeforeStart;
        static public Waypoint Start;
        static public Waypoint Target;

        static public Waypoint[] Fence = {
            new Waypoint(29.8119391, 30.8234954),
            new Waypoint(29.8112502, 30.8272505),
            new Waypoint(29.8197397, 30.8298469),
            new Waypoint(29.8206147, 30.8251262),
        };
    }

    internal static class DesignParams
    {

        public static double H1 = 80; // aircraft altitude
        public static double Vpa = 25; // aircraft velocity
        public static double Vag = 0; // windspeed
        public static double angle = 190;// wind bearing

        // static public float BANK_ANGLE = 
        static public float MIN_TURN_RADIUS = 100; // meters 
    }

}
