package com.example.ut_mactb.stocker;

import android.util.Log;

import java.io.FileReader;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import com.fasterxml.jackson.databind.ObjectMapper;


public class ReadData {
    String getWebData(String data, String companyName){
        String xLabel = "Date";
        String yLabel =  "Movement";
        String header = "['Data','Predicted movement','Real movement']";
        String content = "<!DOCTYPE html>" +
                "<html>" +
                "<head>" +
                "   <script src = 'https://www.gstatic.com/charts/loader.js'></script>" +
                "<script type='text/javascript'>" +
                "      google.charts.load('current', {'packages':['corechart']});" +
                "      google.charts.setOnLoadCallback(drawVisualization);" +
                "" +
                "      function drawVisualization() {" +
                "        var data = google.visualization.arrayToDataTable([" + header + data + "]);" +
                "" +
                "        var options = {" +
                "          title : '" + companyName + "'," +
                "          vAxis: {title: '" + yLabel + "'}," +
                "          hAxis: {title: '" + xLabel + "'}," +
                "        };" +
                "" +
                "        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));" +
                "        chart.draw(data, options);" +
                "      }" +
                "</script>" +
                "</head>" +
                "<body>" +
                "<div id='chart_div' ></div>" +
                "</body>" +
                "</html>";
        return content;
    }
    String readData(InputStream file, InputStream file1){
        StringBuilder sb= new StringBuilder();

        try{
            HashMap<String,String> result =
                    new ObjectMapper().readValue(file, HashMap.class);
            HashMap<String,String> result1 =
                    new ObjectMapper().readValue(file1, HashMap.class);

            for(String key: result.keySet()) {
                sb.append(",[\"");
                sb.append(key);
                sb.append("\", ");
                sb.append(Double.parseDouble(result.get(key)));
                sb.append(", ");
                if(result1.containsKey(key)){
                    sb.append(Double.parseDouble(result1.get(key)));
                }
                else{
                    sb.append("null");
                }

                sb.append("]");
                //Log.i(key,result.get(key));
            }
            Log.i("text",sb.toString());
            return sb.toString();
        }
        catch (Exception e) {
            e.printStackTrace();
            Log.i("Errorrr",e.toString());
        }
        return null;
    }
}
