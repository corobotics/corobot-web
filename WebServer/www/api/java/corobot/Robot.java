/**
 * Robot library in Java
 * 
 * Sketched version for simple simulator testing
 * Could be used as starting point for "real" API
 *
 * @author Z. Butler, Jan 2013
 * @author E. Klei, Dec 2014
 */

/*
  Current questions:
  * How to be informed which robot to connect to? Server
  * What to do if robot connection can't be established? Give Up
  * Or if connection is lost? Wait for response, otherwise, Give Up
  * Robot should detect user program finishing by socket
  being dropped - should make sure that status is updated
  to idle from running
*/

package corobot;
import java.util.*;
import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.awt.Image;

public class Robot {

    // this should come from config file or something? Apparently not
    private static int USER_PORT = 15001;

    private Socket sock;
    private PrintWriter out;
    private BufferedReader in;
    private Map<Integer, Future> futures;
    private readerThread read;
    public String robotData[];
    public static RobotMap robotMap = new RobotMap();

	private int msgId;

	public static final String CMD_NAVTOLOC = "NAVTOLOC",
								CMD_NAVTOXY = "NAVTOXY",
								CMD_GOTOLOC = "GOTOLOC",
								CMD_GOTOXY = "GOTOXY",
								CMD_GETPOS = "GETPOS",
								CMD_POS = "POS",
								CMD_SHOW_MSG = "SHOW_MSG",
								CMD_SHOW_MSG_CONFIRM = "SHOW_MSG_CONFIRM",
								CMD_CONFIRM = "CONFIRM";	

    /**
     * Constructor, starts connection to a robot...
     */
    public Robot() {
    // offloaded to another function for now mostly so that
    // Javadocs can be hidden 
        robotData = null;
        robotData = openSocket();
        msgId = 0;
	read = new readerThread();
        futures = new HashMap<Integer, Future>();
        if ((robotData[1].equals("None")) || (robotData[1].equals("")) || (robotData[0] == null))  {
        	System.out.println ("No idle robot found");
            System.exit(1);
        }
        System.out.println("Robot assigned : " + robotData[0]);
        try {
        	sock = new Socket (robotData[1],USER_PORT);
        	out = new PrintWriter(sock.getOutputStream());
        	in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            } catch (IOException e) {
                System.err.println("Error connecting to assigned robot.  Please try again.");
                throw new RobotConnectionException("in constructor");
        }
    }

	/**
	 * Overriding Object.finalize() method in which we close the socket connection.
	 * Finalize is not guaranteed to be called immediately or might not get called at all 
	 * if the robot object is still referenced in code.
	 */
    protected void finalize() throws Throwable {
    try{
		this.closeSocket();
    }finally{
        super.finalize();
    }
    }
    /**
     * crap!  how does the server tell us which robot 
     * without making the user code do something? By giving us the name of the robot
     * Environment var maybe? Server message
     */
    private String[] openSocket() {
	String robotData[] = null;
        try {
            //String robotName = "corobot2.rit.edu";//System.getenv("ROBOT");
	    String hostname = "vhost1.cs.rit.edu";
            sock = new Socket(hostname, 65000);
            out = new PrintWriter(sock.getOutputStream());
            in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            robotData = in.readLine().split("-");
        } catch (IOException e) {
            System.err.println("Error connecting to assigned robot.  Please try again.");
            throw new RobotConnectionException("in openSocket()");
        }
	finally {
		this.closeSocket();
		return robotData;
	}
    }
	/**
	 * Manually close the connection with the robot.
	 * Should be called by the user at the end of thier program
	 */
	public void closeSocket(){
		try{
			if(sock != null && !sock.isClosed())
				sock.close(); // closes the in and out streams too
		} catch(Exception e){
			System.err.println("IOException thrown in Robot.closeSocket()");
		}
		//System.out.println ("Connection to server closed");
	}

	/**
	 * This method can send commands (messages) to the robot as per the specified format in API.md
	 *
	 * @param args: String vararg parameters to take the command and its options and send it to the 
	 * robot over the socket connection.
	 */
	public Future sendMsgToRobot(String... args){
		Future fut = new Future();
		futures.put(msgId, fut);
		if(!read.isAlive()){
			read.start();
		}
		StringBuilder msgToSend = new StringBuilder((msgId++) + "");
		for (String arg : args )
			msgToSend.append(" " + arg);
		out.println(msgToSend.toString());
		out.flush();
		return fut;
	}

	/**
	 * Checks the messages from the robot for information on resolving futures
	 */
	private void checkArrivedResponse(){
		String response = null;
		try {
			response = in.readLine();
			if(response == null){
				for(Future f: futures.values()){
					f.error_occured("Robot Connection Closed");
				}
				System.exit(1);
			}
			String[] msgs = response.split(" ");
			int id = Integer.parseInt(msgs[0]) -1;
			Future future = futures.remove(id);
			String[] data = Arrays.copyOfRange(msgs, 2, msgs.length);
			if( msgs[1] != "ERROR" ){
				future.fulfilled(data);
			}else{
				future.error_occured(data);
			} 
		} catch (IOException e) {
			System.err.println("Lost connection with robot!");
			throw new RobotConnectionException("Lost connection with robot!");
		}
	}

    /**
     * Tells the robot to plan a path to a location, then follow that path
     *
     * @param location Name (as on map) 
     * @return A future corresponding to the robot executing this operation
     */
    public Future navigateToLocation(String location) throws MapException{
        System.out.println("Navigating to "+location);
        location = location.toUpperCase();
        if (robotMap.isNode(location)) {
		return sendMsgToRobot(CMD_NAVTOLOC, location.toUpperCase());
		//return checkArrivedResponse("navigateToLocation");
        }else{
		throw new MapException("Location does not exist");
	}
    }
    

	/**
     * Plans and executes a path to the given coordinates.  Planning is done by the robot.
     *
     * @param x : x-coordinate in the map
     * @param y: y-coordinate in the map
     * @return A future that corresponds to the robot executing this command
     */
	public Future navigateToXY(double x, double y){
           System.out.println("Navigate to ( "+String.valueOf(x) + ", "+String.valueOf(y)+")");
	   return sendMsgToRobot(CMD_NAVTOXY, x+"", y+"");
	}

    /**
     * Attempts to move in a straight line to the given location.
     *
     * 
     * @param location Name (as on map) 
     * @return Future representing the current execution of the command
     */
    public Future goToLocation(String location) throws MapException{
        System.out.println("Going to " + location);
        location = location.toUpperCase();
        if (robotMap.isNode(location)) {
		return sendMsgToRobot(CMD_GOTOLOC, location.toUpperCase());
			//return checkArrivedResponse("goToLocation");
			
	} else
		throw new MapException("Location does not exist");
    }

    /**
     * Attempts to move in a straight line to the given X,Y location
     * @param x X coordinate of destination (in map coordinate system) 
     * @param y Y coordinate of destination (in map coordinate system) 
     * @return A Future that represents the execution of this command
     */
    public Future goToXY(double x, double y) {
        System.out.println("Going to ( " + x + ", " + y + ")");
       	return sendMsgToRobot(CMD_GOTOXY, x+"", y+"");
    }
	/**
	 * Retrieves the current position of the robot
	 * @return A Future where the position has been reached
     */
    public Future getPos() {
		System.out.println("Getting position");
        return sendMsgToRobot(CMD_GETPOS);
    }
/**
#TODO Update this too
     * Gives the named location closest to the robot's current position.
     *
     * @return Name of location
    public String getClosestLoc() {
        Point p = getPos();
        return robotMap.getClosestNode(p.getX(),p.getY());
    }

    /**
     * Returns all named locations close to the robot's current position.
     * not sure how to define "close" here, but likely to be useful
     *
     * Currently not implemented.
     *
     * @return list of nearby location names
    public List<String> getAllCloseLocs() {
        throw new UnsupportedOperationException();
    }

    /**
     * Sends a message for display on the local (robot) GUI
     * @param msg Message to display (&lt; 256 chars suggested)
	 * @param timeout : timeout duration 
	 * @return A Future representing the running of this operation
     */
    public Future showMessage(String msg, int timeout) {
	System.out.println("Displaying Message");
        if (msg.length() > 255)
            msg = msg.substring(0,255);
		if (timeout > 120)
            timeout = 120;
        return sendMsgToRobot(CMD_SHOW_MSG, timeout+"", msg);
    }

	/**
     * Sends a message for display on the local (robot) GUI
     * @param msg Message to display (&lt; 256 chars suggested)
	 * @param timeout : timeout duration 
	 * @return A Future representing the running of this operation
     */
    // show a message on the laptop GUI
     public Future showMessageWithConfirmation(String msg, int timeout) {
         System.out.println("Displaying Confirmation");
         if (msg.length() > 255)
            msg = msg.substring(0,255);
		 if (timeout > 120)
            timeout = 120;
	return sendMsgToRobot(CMD_SHOW_MSG_CONFIRM, timeout+"", msg);
    }
    
    /**
     * Obtain a picture from one of the robot's cameras
     * Extremely not implemented at present.
     * @param whichCamera Which camera to use: 0 = left, 1 = fwd, 2 = right
     * @return some image in some format?
     */
    public Image getImage(int whichCamera) {    
        throw new UnsupportedOperationException();
    }
	/**
	 * A private thread to read the robot responses and pass them to the appropriate future
	 */
    private class readerThread extends Thread{
	public void run(){
		while(futures.size() > 0){
			checkArrivedResponse();
		}
		
	}
    }    // may want other access to robot data but not sure what yet.
}
