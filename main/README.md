Project Overview
Hello_World_Project is a simple Java GUI-based application that reads a message and a count from a project.csv file, displays the message and the incremented count in a window, and updates the CSV file with the new count. The project also opens the system terminal and displays the file contents via command-line commands tailored to the detected operating system (Windows or macOS).


Requirements
* Java Development Kit (JDK) version 8 or above


Features
* OS Detection: The program identifies the operating system (Windows or macOS) and runs a corresponding terminal command to display the contents of project.csv.
* CSV File Handling: The program reads data from a CSV file (first entry is a message, second entry is a count), increments the count, and writes the updated data back to the file.
* Simple GUI: The incremented count and message are displayed in a graphical window using Java Swing components.


Project Structure
The project consists of a single Java file Hello_World_Project.java and a project.csv file.
* Hello_World_Project.java: The main class that handles file reading/writing, GUI display, and terminal command execution based on the operating system.
* project.csv: A CSV file in the format of message,count. The message is a string, and the count is an integer.
How the Program Works
1. Operating System Detection:
   * The program detects if the OS is Windows or macOS and executes the appropriate command to open the terminal and display the contents of the project.csv file.
2. Reading CSV File:
   * The program reads the project.csv file, extracting the message and the count.
3. Displaying GUI:
   * A GUI window is displayed using Swing, which shows the message along with the incremented count.
4. Updating the CSV File:
   * After the GUI is displayed, the program writes the new message and updated count back to the project.csv file.