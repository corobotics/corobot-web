/********************
* A VirtualRobot for testing the API functionality without using a real robot
* Usable for checking connections and basic sending of data. Actual robot
* functionality should use a real robot
* @author E. Klei Jul 2014
********************/

import java.io.*;
import java.net.*;

public class VirtualRobot {
	private ServerSocket mine;
	private Socket sock;
	private PrintWriter out;
	private BufferedReader in;
	/**
	 * Creates a new VirtualRobot
     */
	public VirtualRobot(){
		try{
			mine = new ServerSocket(15001);
			sock = mine.accept();
			out = new PrintWriter(sock.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
		}catch( IOException e) {
			e.printStackTrace();
		}
	}
    /**
     * Simulates the act of robot movement. Waits, then continues
     * @args The id of the message telling the robot to go to a place
	 */
	public void goPlaces(int msgId){
		try{
			Thread.sleep(1000);
			sendPos(msgId);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	/**
	 * Simulates a robot sending it's position
     * @args the message id to send with
     */
	public void sendPos(int msgId){
		out.println(msgId + " POS 0 0 0" );
	}
    /**
     * Simulates the result of a confirm dialog
     * @args the message id to send with
     */
	public void confirm(int msgId){
		out.println(msgId + " CONFIRM false");
	}
    /**
     * Simulates displaying a message
     */
	public void showMessage(){
		System.out.print("Message");
	}
	/**
	 * Simulates displaying a confirmation
     * @args the id of the command sent
     */
	public void showConfirm(int msgId){
		System.out.print("Confirm");
		confirm(msgId);
	}
    /**
     * Start reading the input to the server
     */
	public void startReading(){

		new readerThread().start();
	}
    /**
     * Runs forever, reading input and calling the appropriate functions
     */
	private class readerThread extends Thread{
		public void run(){
			for(;;){
				try{
					String given = in.readLine();
					int id = Integer.parseInt(given.split(" ")[0]);
					String key = given.split(" ")[1];
					if(key.equals("NAVTOLOC") || key.equals("NAVTOXY") || key.equals("GOTOLOC") || key.equals("GOTOXY") ){
						goPlaces(id);
					}else if(key.equals("SHOW_MSG")){
						showMessage();
					}else if(key.equals("SHOW_MSG_CONFIRM")){
						showConfirm(id);
					}else{
						System.out.print("Unknown command");
					}
				}catch(Exception e){
				}
				finally{
					try{
						sock.close();
					}catch(Exception e){}
				}
			}
		}
	}
}
