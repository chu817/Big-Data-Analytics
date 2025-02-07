//This code is written by HIMANI S KUMAR 22MIA1092 on 5.2.2025
import java.io.*;
import java.util.*;

public class IMDBDataCleaner {
    public static void main(String[] args) {
        String inputFile = "movies.csv";
        String outputFile = "cleaned_movies.csv";
        List<String[]> cleanedData = new ArrayList<>();
        
        try (BufferedReader br = new BufferedReader(new FileReader(inputFile))) {
            String line;
            boolean isFirstLine = true;

            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                if (isFirstLine) {
                    cleanedData.add(values);
                    isFirstLine = false;
                    continue;
                }

                int index = parseInt(values[0]);
                String title = values[1].trim().replaceAll("[^a-zA-Z0-9 ]", "");
                int duration = parseDuration(values[2]);
                int year = parseInt(values[3]);
                int ageRating = parseInt(values[4]);
                double imdbRating = parseDouble(values[5]);
                int votes = parseVotes(values[6]);
                int metacriticScore = parseInt(values[7]);

                cleanedData.add(new String[]{String.valueOf(index), title, String.valueOf(duration), String.valueOf(year), 
                    String.valueOf(ageRating), String.valueOf(imdbRating), String.valueOf(votes), String.valueOf(metacriticScore)});
            }
            
            writeToCSV(outputFile, cleanedData);
            System.out.println("Data cleaning complete! Cleaned data saved to: " + outputFile);
        } catch (IOException e) {
            System.err.println("Error reading the file: " + e.getMessage());
        }
    }

    private static int parseDuration(String duration) {
        if (duration.matches("\\d+h \\d+m")) {
            String[] parts = duration.split("h |m");
            return Integer.parseInt(parts[0]) * 60 + Integer.parseInt(parts[1]);
        }
        return duration.matches("\\d+h") ? Integer.parseInt(duration.replace("h", "")) * 60 : -1;
    }

    private static int parseInt(String value) {
        try {
            return Integer.parseInt(value.replaceAll("[^0-9]", ""));
        } catch (NumberFormatException e) {
            return -1;
        }
    }

    private static double parseDouble(String value) {
        try {
            return Double.parseDouble(value);
        } catch (NumberFormatException e) {
            return -1.0;
        }
    }

    private static int parseVotes(String votes) {
        votes = votes.replace("M", "000000").replace("K", "000");
        return parseInt(votes);
    }

    private static void writeToCSV(String outputFile, List<String[]> data) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile))) {
            for (String[] row : data) {
                bw.write(String.join(",", row));
                bw.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }
    }
}
