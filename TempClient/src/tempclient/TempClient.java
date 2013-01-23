/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package tempclient;

import java.io.IOException;
import java.util.Random;
import org.apache.http.HttpHost;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.HttpContext;

/**
 *
 * @author Balaji
 */
public class TempClient {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException, InterruptedException {
        // TODO code application logic here
        HttpClient httpclient = new DefaultHttpClient();
        try {
            for (int k = 0; k < 200; k++)
            {
                Thread.sleep(1000);
                Random coordinate = new Random();
                String i = String.valueOf(coordinate.nextInt(255));
                String j = String.valueOf(coordinate.nextInt(255));
                HttpGet httpget = new HttpGet("http://129.21.30.80:8080/acceptInput?robotname=" + "Testrobot&" + "x=" + i + "&y=" + j);

                System.out.println("Sent coordinates of the robot Testrobot is x : " + i + " and y :" + j);
                // Create a response handler
                ResponseHandler<String> responseHandler = new BasicResponseHandler();

                String responseBody = httpclient.execute(httpget, responseHandler);
                System.out.println("----------------------------------------");
                System.out.println(responseBody);
                System.out.println("----------------------------------------");
            }

        } finally {
            // When HttpClient instance is no longer needed,
            // shut down the connection manager to ensure
            // immediate deallocation of all system resources
            httpclient.getConnectionManager().shutdown();
        }

    }
}
