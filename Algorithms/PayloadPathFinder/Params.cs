public static class CodeParams
{
    // code related
    static public int POPULATION_SIZE = 9000;
    static public int CHROMOSOME_SIZE = 6;
    public static int MAX_GENERATIONS = 100;

    public static float REPLACE_RATE = 0.5f;
    public static float INDIVIDUAL_MUTATE_RATE = 0.1f;
    public static float GENE_MUTATE_RATE = 1f;
    static public float ELITE_RATE = 0.05f;
}

public static class MissionParams
{
    static public Waypoint BeforeStart = new(29.8149644, 30.8251369);
    static public Waypoint Start = new(29.8157371, 30.8247185);
    static public Waypoint Target = new(29.8148993, 30.8269608);

    static public Waypoint[] Fence = [
        new Waypoint(29.8119391, 30.8234954),
        new Waypoint(29.8112502, 30.8272505),
        new Waypoint(29.8197397, 30.8298469),
        new Waypoint(29.8206147, 30.8251262),
    ];
}

public static class DesignParams
{

    public static double H1 = 80; // aircraft altitude
    public static double Vpa = 25; // aircraft velocity
    public static double Vag = 0; //windspeed
    public static double angle = 190;// wind bearing

    // static public float BANK_ANGLE = 
    static public float MIN_TURN_RADIUS = 70; // meters 
}
