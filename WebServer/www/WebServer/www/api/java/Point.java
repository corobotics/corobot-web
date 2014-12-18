import java.text.NumberFormat;

/**
 * Just a 2D point
 */
public class Point {

    // just a 2d point

    private double x, y;
    private static NumberFormat nf;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public String toString() {
        if (nf == null) {
            nf = NumberFormat.getInstance();
            nf.setMaximumFractionDigits(2);
        }
        return "(" + nf.format(x) + "," + nf.format(y) + ")";
    }
}