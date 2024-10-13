import java.awt.event.*;
import java.awt.*;
import javax.swing.*;
import java.io.*;
import java.util.Scanner;

public class Hello_World_Project extends JFrame {

	// frame
	static JFrame f;

	// label to display text
	static JLabel l;

	// default constructor
	void text() {
	}

	// main class
	public static void main(String[] args) {
		// Detect the operating system
		String os = System.getProperty("os.name").toLowerCase();
		String currentDir = System.getProperty("user.dir");
		// Print to terminal
		// Conditional statement to check the OS and run the corresponding code
		if (os.contains("win")) {
			// Windows command
			try {
				new ProcessBuilder("cmd.exe", "/c", "start", "cmd.exe", "/k",
						"echo Hello World and the count will be here! && cd " + currentDir + " && type project.csv")
						.start();
			} catch (IOException e) {
				System.out.println("Error opening terminal on Windows: " + e.getMessage());
			}
		} else if (os.contains("mac")) {
			// macOS command
			try {
				String[] command = {
						"osascript",
						"-e",
						"tell application \"Terminal\" to do script \"cd " + currentDir
								+ " && echo $(cat project.csv | tr ',' ' ') && read\""
				};
				new ProcessBuilder(command).start();
			} catch (IOException e) {
				System.out.println("Error opening terminal on macOS: " + e.getMessage());
			}
		} else {
			System.out.println("Unsupported OS.");
		}

		String message = "";
		int number = 0;

		// Read data from the file
		try (Scanner sc = new Scanner(new File("project.csv"))) {
			sc.useDelimiter(",");
			if (sc.hasNext()) {
				message = sc.next();
				if (sc.hasNextInt()) {
					number = sc.nextInt();
				}
			}
		number=number+1;
		} catch (FileNotFoundException e) {
			System.out.println("File not found. Please ensure 'project.csv' exists in the working directory.");
			return;
		}
		// Setup the JFrame
		f = new JFrame("OUTPUT");
		l = new JLabel();
		l.setText(message + " " + number);

		// Create and add panel to frame
		JPanel p = new JPanel();
		p.add(l);
		f.add(p);
		f.setSize(300, 200);
		f.setLocationRelativeTo(null);
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		// update the number
		// Update the file with the new count
		try (FileWriter fw = new FileWriter("project.csv")) {
			fw.write(message + "," + number);
		} catch (IOException e) {
			System.out.println("Error writing to file: " + e.getMessage());
		}
	}
}
