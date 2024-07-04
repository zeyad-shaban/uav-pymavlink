public static class CodeParams
{
    // code related
    static public int POPULATION_SIZE = 20000;
    static public int CHROMOSOME_SIZE = 6;
    public static int MAX_GENERATIONS = 200;

    public static float REPLACE_RATE = 0.5f;
    public static float INDIVIDUAL_MUTATE_RATE = 0.1f;
    public static float GENE_MUTATE_RATE = 1f;
}

public static class MissionParams
{
    static public Waypoint BeforeStart = new(29.8134564, 30.8248365);
    static public Waypoint Start = new(29.8127582, 30.8246756);
    static public Waypoint Target = new(29.8132144, 30.8249545);

    static public Waypoint[] Fence = [
        new Waypoint(29.8117901, 30.8230877),
        new Waypoint(29.8113247, 30.8267570),
        new Waypoint(29.8200376, 30.8288169),
        new Waypoint(29.8206147, 30.8252120),
    ];
}

public static class DesignParams
{
    static public float MIN_TURN_RADIUS = 45; // meters

    public static double H1 = 80; // aircraft altitude
    public static double Vpa = 25; // aircraft velocity
    public static double Vag = 0; //windspeed
    public static double angle = 190;// wind bearing
}
