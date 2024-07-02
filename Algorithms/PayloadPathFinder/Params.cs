using System.Security.Cryptography.X509Certificates;

public static class CodeParams
{
    // code related
    static public int POPULATION_SIZE = 10000;
    static public int CHROMOSOME_SIZE = 3;
    public static int MAX_GENERATIONS = 500;

    public static float REPLACE_RATE = 0.5f;
    public static float INDIVIDUAL_MUTATE_RATE = 0.05f;
    public static float GENE_MUTATE_RATE = 0.75f;
}

public static class MissionParams
{
    static public Waypoint BeforeStart = new(29.8163607, 30.8250833);
    static public Waypoint Start = new(29.8171240, 30.8252549);
    static public Waypoint Target = new(29.8200003, 30.8256948);

    static public Waypoint[] Fence = [
        new Waypoint(29.8163421, 30.8241391),
        new Waypoint(29.8160815, 30.8258665),
        new Waypoint(29.8202423, 30.8267891),
        new Waypoint(29.8205774, 30.8249652),
    ];
}

public static class DesignParams
{
    static public float MIN_THROW_DISTANCE_IN_METERS = 40;

    static public float MIN_TURN_RADIUS_IN_METERS = 45; // meters
    static public float PLANE_SPEED = 25; // m per sec

    static public float MAX_TURN_RATE = PLANE_SPEED / MIN_TURN_RADIUS_IN_METERS;
}
