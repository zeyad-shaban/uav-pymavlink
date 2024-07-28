using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PathFinder.Fundamentals
{
    public static class CodeParams
    {
        // many defeats brave method >:}
        static public int POPULATION_SIZE = 250000;
        static public int CHROMOSOME_SIZE = 3;
        public static int MAX_GENERATIONS = 200;

        public static float REPLACE_RATE = 0.4f;
        public static float INDIVIDUAL_MUTATE_RATE = 0.25f;
        public static float GENE_MUTATE_RATE = 0.75f;
        static public float ELITE_RATE = 0.005f;
    }

    public static class MissionParams
    {
        static public int obstacleRadius = 5; // meters
        static public Waypoint BeforeStart;
        static public Waypoint Start;
        static public Waypoint Target;

        static public Waypoint[] Fence = { };

        static public Waypoint[] Obstacles = { };
    }

    public static class DesignParams
    {

        public static double H1 = 80; // aircraft altitude
        public static double Vpa = 20; // aircraft velocity
        public static double Vag = 0; // windspeed
        public static double angle = 190;// wind bearing

        // static public float BANK_ANGLE = 
        static public float MIN_TURN_RADIUS = 28; // meters 
    }
}