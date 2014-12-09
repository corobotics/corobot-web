/***************
* An object that works with the Robot class to allow programs to run without
* the need to wait for the robot to send back a message. Also allows for
* functions to be called when a Robot finishes a task.
*
* @author E. Klei Jul 2014
***************/
package corobot;
import java.util.*;
import java.util.concurrent.Semaphore;

public class Future{
    private String[] data;
    private CorobotException error;
    private ArrayList<Callback> callbacks;
    private ArrayList<Callback> errors;
    private Semaphore awaitingIO;
    private boolean done;
    
	/**
	 * Creates a future
	 */
    public Future(){
        data = null;
		error = null;
		done = false;
		awaitingIO = new Semaphore(0);
		callbacks = new ArrayList<Callback>();
    }
    
	/**
	 * Makes the object that calls the future wait for the future to be fufilled
     * before continuing
     * @return The future that called this function
     */
    public Future pause() throws CorobotException{
    	try {
			awaitingIO.acquire();
		} catch (InterruptedException e){
			e.printStackTrace();
		}
		if( error != null ){
			throw error;
		}
		awaitingIO.release();
		return this;
	}

	/**
	 * Performs a function after the future is fufilled
     * @args The function that gets called when the future is fufilled
	 * @return The future that called this function
	 */
    public Future then(Callback call){
    	return then(call, null);
    }

    /**
	 * Performs a function after the future is fufilled
     * @args The function that gets called when the future is fufilled
     * @args The function that is called when the robot returns an error
     * @return The future that called this function
     */
    public Future then(Callback call, Callback error){
		if (call != null){
			callbacks.add(call);
		}		
		if (error != null){
			errors.add(error);
		}
		return this;
    }
    /**
     * Returns data sent from the robot in response to 
     * @return The data as an array of strings
     */
    public String[] get(){
		try{
			this.pause();
		}catch(Exception e){}
    	return data;
    }
    /**
     * Checks if the future has been fufilled
     * @return true if it has, otherwise, false
     */
    public boolean is_fufilled(){
    	return done;
    }
    /**
     * Contains the callback
     * @args the callback to call
     */
	protected void safe_call(Callback f){
		safe_call(f, null);
	}
	/**
	 * Contains the callback
     * @args the callback to call
     * @args the data to pass to the callback
     */
	protected void safe_call(Callback f, String[] data){
		try{
			f.call(data);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	/**
	 * Marks that this future has been fufilled
	 * @args the data to be used for the callback
	 */
	protected void fulfilled(String[] data){
		this.data = data;
		Iterator<Callback> i = callbacks.iterator();
		while( i.hasNext() ){
			safe_call(i.next(), this.data);
		}
		awaitingIO.release();
	}
	/**
     * Marks that this future has had an error occur
     * @args The error data to be used for the callback
     */
	protected void error_occured(String[] error){
		StringBuilder builder = new StringBuilder();
		for(String s : error){
			builder.append(s);
		}
		this.error = new CorobotException(builder.toString());
		Iterator<Callback> i = errors.iterator();
		while (i.hasNext()){
			safe_call(i.next(), error);
		}
		awaitingIO.release();
	}

}
