/**
 * Exception that will be thrown if robot connection is lost
 * or cannot be established.
 * @author zjb
 */
package corobot;
public class RobotConnectionException extends RuntimeException {
    
    /**
     * Constructor
     * @param msg Exception message
     */
    public RobotConnectionException(String msg) {
        super(msg);
    }
}
