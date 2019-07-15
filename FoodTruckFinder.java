import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class FoodTruckFinder {
	public static void main(String[] args) {
   		try {
			StringBuilder result = new StringBuilder();
			URL url = new URL("http://data.sfgov.org/resource/bbb8-hzi6.xml");
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			String line;
			while ((line = rd.readLine()) != null) {
				result.append(line);
			}
			rd.close();

			System.out.println(result.toString());
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}
}

// to run:
// $ javac FoodTruckFinder.java && java FoodTruckFinder
