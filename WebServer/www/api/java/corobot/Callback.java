/*******************
 * An interface that allows the user to send functions to futures
 * @author E. Klei Jul 2014
 */
package corobot;

public interface Callback{
	/**
     * The function being enacted. Should be overwritten with user specification
     * @args The data to be sent, can be null
     */
    void call(String[] data);
}

