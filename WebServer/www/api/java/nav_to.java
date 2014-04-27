public class nav_to {

    public static void main(String[] args) {
        Robot robot = new Robot();
	String destination = "GraphicsLab";
        if (robot.navigateToLocation(destination))
            System.out.println("Robot assigned : " + robot.robotData[0]);
        else
            System.out.println("Sorry! No idle robot found");
	}
}
