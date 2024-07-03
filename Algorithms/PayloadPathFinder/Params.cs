using System.Security.Cryptography.X509Certificates;

public static class CodeParams
{
    // code related
    static public int POPULATION_SIZE = 10000;
    static public int CHROMOSOME_SIZE = 10;
    public static int MAX_GENERATIONS = 120;

    public static float REPLACE_RATE = 0.5f;
    public static float INDIVIDUAL_MUTATE_RATE = 0.05f;
    public static float GENE_MUTATE_RATE = 0.8f;
}

public static class MissionParams
{
    static public Waypoint BeforeStart = new(29.8166214, 30.8259094);
    static public Waypoint Start = new(29.8175522, 30.8260703);
    static public Waypoint Target = new(29.8196838, 30.8265102);

    static public Waypoint[] Fence = [
        new Waypoint(29.8164631, 30.8240640),
        new Waypoint(29.8159419, 30.8275187),
        new Waypoint(29.8200841, 30.8284521),
        new Waypoint(29.8205867, 30.8250296),
    ];
}

public static class DesignParams
{
    static public float MAX_THROW_DIST = 40; // meters
    static public float MIN_TURN_RADIUS_IN_METERS = 45; // meters
    static public float PLANE_VELOCITY = 25; // meters/sec
}
