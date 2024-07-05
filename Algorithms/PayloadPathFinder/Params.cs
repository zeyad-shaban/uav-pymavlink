public static class CodeParams
{
    // code related
    static public int POPULATION_SIZE = 20000;
    static public int CHROMOSOME_SIZE = 4;
    public static int MAX_GENERATIONS = 500;

    public static float REPLACE_RATE = 0.5f;
    public static float INDIVIDUAL_MUTATE_RATE = 0.15f;
    public static float GENE_MUTATE_RATE = 0.25f;
    static public float ELITE_RATE = 0.05f;
}

public static class MissionParams
{
    static public Waypoint BeforeStart = new(29.8149644, 30.8262312);
    static public Waypoint Start = new(29.8143780, 30.8270466);
    static public Waypoint Target = new(29.8147503, 30.8246970);

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
