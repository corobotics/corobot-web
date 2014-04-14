/**
 * Simple example to show some use of the corobot user API.
 * 
 * @author Zack Butler
 *
 */
public class SimpleExample {

    /**
     * Main method (all the code(
     * 
     * @param args (ignored)
     */
    public static void main(String[] args) {
        
        Robot robot = new Robot();
        System.out.println("Connected!");
        Point p = robot.getPos();
        System.out.println("Starting at " + p);
        //      String loc = robot.getClosestLoc();
        //      System.out.println("Closest location is " + loc);
        //      robot.goToLocation(loc, true);
        robot.showMessage("I'm heading to the Atrium!", 20);
        if(robot.navigateToLocation("AtriumS3"))
        //if (robot.goToXY(p.getX() - 1.5, p.getY() + 1.0)) 
            System.out.println("Made it!");
        else
            System.out.println("didn't make it.");
		robot.closeSocket();
    }
}
