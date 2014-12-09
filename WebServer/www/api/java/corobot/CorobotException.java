/**
 * An exception having to do with the robot end of the run time
 * @author E. Klei Jul 2014
 */
package corobot;
public class CorobotException extends Exception {
	public CorobotException(){
		super("Something is wrong with the corobot");
	}
	public CorobotException(String error){
		super(error);
	}
}
