package com.example.ut_mactb.stocker;


import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class ChartActivity extends AppCompatActivity {

    public static final String PATTERN = "Pattern";
    public static final String PATTERN_NAME = "Pattern Name";
    public static final String PREDICTION = "Prediction";
    public static final String ACCURACY = "Accuracy";

    public static final String HIGH = "HIGH";
    public static final String LOW = "LOW";

    public final String DATE = "Date";
    public final String OPEN = "Open";
    public final String CLOSE = "Close";
    public final String ACTION = "Action";

    private String companyName = "Apple";
    private String patternName = "";

    private WebView webview;
    private ListView listView;
    private TextView avgPredictionTextView;
    //private TextView avgStatusTextView;
    private TextView wtdPredictionTextView;
    private TextView wtdStatusTextView;

    private boolean positiveExists = false;
    private boolean negativeExists = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chart);

        avgPredictionTextView = (TextView) findViewById(R.id.avgPredictionTextView);
        //avgStatusTextView = (TextView) findViewById(R.id.avgStatusTextView);
        wtdPredictionTextView = (TextView) findViewById(R.id.wtdPredictionTextView);
        wtdStatusTextView = (TextView) findViewById(R.id.wtdStatusTextView);

        avgPredictionTextView.setText("Average Prediction");
        //avgStatusTextView.setText(HIGH);
        //if (avgStatusTextView.getText().equals(ChartActivity.HIGH)) {
          //  avgStatusTextView.setTextColor(Color.rgb(0, 153, 51));
        //} else {
          //  avgStatusTextView.setTextColor(Color.RED);
        //}

        wtdPredictionTextView.setText("Weighted Prediction");
        wtdStatusTextView.setText(LOW);
        if (wtdStatusTextView.getText().equals(ChartActivity.HIGH)) {
            wtdStatusTextView.setTextColor(Color.rgb(0, 153, 51));
        } else {
            wtdStatusTextView.setTextColor(Color.RED);
        }

        listView = (ListView) findViewById(R.id.listView);
        InputStream patternInputStream = getResources().openRawResource(R.raw.patternanalysisdata);
        CSVFile patternFile = new CSVFile(patternInputStream);
        List<String[]> patternDetailList = patternFile.read();

        final ArrayList<String> patternList = new ArrayList<>();
        patternList.add(PATTERN);
        final ArrayList<String> patternNameList = new ArrayList<>();
        patternNameList.add(PATTERN);
        final ArrayList<String> patternPredictionList = new ArrayList<>();
        patternPredictionList.add(PREDICTION);
        final ArrayList<String> patternAccuracyList = new ArrayList<>();
        patternAccuracyList.add(ACCURACY);

        patternDetailList.remove(0);
        for (String[] patternDetail : patternDetailList) {
            patternList.add(patternDetail[0]);
            patternNameList.add(patternDetail[1]);
            patternPredictionList.add(patternDetail[2]);
            patternAccuracyList.add(patternDetail[3]);
        }

        //ArrayAdapter<String> adapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_list_item_1, patternNameList);
        listView.setAdapter(new PatternAdapter(getApplicationContext(), patternList, patternNameList, patternPredictionList, patternAccuracyList));

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                if (position > 0) {
                    patternName = patternNameList.get(position);
                    //Toast.makeText(getApplicationContext(), patternPredicitonList.get(position), Toast.LENGTH_SHORT).show();
                    loadGraph(patternList.get(position));
                }
            }
        });
    }

    private void loadGraph(String givenPatternName) {

        positiveExists = false;
        negativeExists = false;
        int resId = getResourceIdByName(givenPatternName);
        InputStream inputStream = getResources().openRawResource(resId);
        CSVFile csvFile = new CSVFile(inputStream);
        List<String[]> stockList = csvFile.read();

        int dateIndex = -1;
        int openIndex = -1;
        int closeIndex = -1;
        int actionIndex = -1;

        if (!stockList.isEmpty()) {
            String[] headersArray = stockList.get(0);
            for (int index = 0; index < headersArray.length; index++) {
                if (headersArray[index].equals(DATE)) {
                    dateIndex = index;
                } else if (headersArray[index].equals(OPEN)) {
                    openIndex = index;
                } else if (headersArray[index].equals(CLOSE)) {
                    closeIndex = index;
                } else if (headersArray[index].equals(ACTION)) {
                    actionIndex = index;
                }
            }
            stockList.remove(0);
        }

        ArrayList<String> dateList = new ArrayList<>();
        ArrayList<String> openList = new ArrayList<>();
        ArrayList<String> closeList = new ArrayList<>();
        ArrayList<String> actionList = new ArrayList<>();

        for (String[] stockData : stockList) {
            dateList.add(stockData[dateIndex]);
            openList.add(stockData[openIndex]);
            closeList.add(stockData[closeIndex]);
            actionList.add(stockData[actionIndex]);
        }

        ArrayList<String> formattedDateList = formatDates(dateList);

        String data = getData(formattedDateList, closeList, actionList);
        if (!positiveExists || !negativeExists) {
            data = reformatData(formattedDateList, closeList, actionList);
        }
        String header = getHeader();
        //Log.i("GP_DATA", data);
        String series = getSeries();

        String xColumn = "X";
        String yColumn = "Amount";

        String xLabel = DATE;
        String yLabel = CLOSE;

        webview = (WebView) findViewById(R.id.webView);
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
                "          title : '" + companyName + ": " + patternName + "'," +
                "          vAxis: {title: '" + yLabel + "'}," +
                "          hAxis: {title: '" + xLabel + "'}," +
                "          seriesType: 'line'," +
                "          series: {" + series + "}" +
                "        };" +
                "" +
                "        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));" +
                "        chart.draw(data, options);" +
                "      }" +
                "</script>" +
                "</head>" +
                "<body>" +
                "<div id='chart_div'></div>" +
                "</body>" +
                "</html>";

        Log.i("GP_TAG", content);
        String encodedHtml = Base64.encodeToString(content.getBytes(), Base64.NO_PADDING);
        WebSettings webSettings = webview.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webview.requestFocusFromTouch();
        webview.loadData(encodedHtml, "text/html", "base64");
    }

    private String getData(ArrayList<String> xValues, ArrayList<String> yValues, ArrayList<String> actionList) {
        String data = "";
        if (xValues.size() == yValues.size()) {
            for (int index = 0; index < xValues.size(); index++) {
                String dataPoint = "";
                if (actionList.get(index).equals("100")) {
                    positiveExists = true;
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", " + yValues.get(index) + ", null]";
                } else if (actionList.get(index).equals("-100")) {
                    negativeExists = true;
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", null, " + yValues.get(index) + "]";
                } else {
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", null, null]";
                }
                data += (dataPoint + ",");
            }
        }
        return data;
    }

    private String reformatData(ArrayList<String> xValues, ArrayList<String> yValues, ArrayList<String> actionList) {
        String newData = "";
        if (!positiveExists) {
            for (int index = 0; index < xValues.size(); index++) {
                String dataPoint = "";
                if (!negativeExists) {
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + "]";
                    newData += (dataPoint + ",");
                } else {
                    if (actionList.get(index).equals("-100")) {
                        dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", " + yValues.get(index) + "]";
                    } else {
                        dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", null]";
                    }
                }
                newData += (dataPoint + ",");

            }
        } else {
            for (int index = 0; index < xValues.size(); index++) {
                String dataPoint = "";
                if (actionList.get(index).equals("100")) {
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", " + yValues.get(index) + "]";
                } else {
                    dataPoint = "[" + xValues.get(index) + ", " + yValues.get(index) + ", null]";
                }
                newData += (dataPoint + ",");
            }
        }
        return newData;
    }

    private ArrayList<String> formatDates(ArrayList<String> dateList) {
        ArrayList<String> formattedDateList = new ArrayList<>();
        Iterator<String> dateIterator = dateList.iterator();
        while (dateIterator.hasNext()) {
            String currentDate = dateIterator.next();
            String regex = "";
            if (currentDate.contains("-")) {
                regex = "-";
            } else {
                regex = "/";
            }
            String[] splitDate = currentDate.split(regex);
            //String formattedCurrentDate = "new Date(" + splitDate[0] + ", " + splitDate[1] + ", " + splitDate[2] + ")";
            String formattedCurrentDate = "'" + splitDate[0] + "/" + splitDate[1] + "/" + splitDate[2] + "'";
            formattedDateList.add(formattedCurrentDate);
        }
        return formattedDateList;
    }

    private String getHeader() {
        String header = "";
        if (positiveExists) {
            if (negativeExists) {
                header = "['Date', 'Closed Price', '" + HIGH + "', '" + LOW + "'],";
            } else {
                header = "['Date', 'Closed Price', '" + HIGH + "'],";
            }

        } else {
            if (negativeExists) {
                header = "['Date', 'Closed Price', '" + LOW + "'],";
            } else {
                header = "['Date', 'Closed Price'],";
            }
        }
        return header;
    }

    private String getSeries() {
        String series = "";
        if (positiveExists) {
            if (negativeExists) {
                series = "1: {type: 'scatter'}, 2: {type: 'scatter'}";
            } else {
                series = "1: {type: 'scatter'}";
            }

        } else {
            if (negativeExists) {
                series = "1: {type: 'scatter'}";
            } else {
                series = "";
            }
        }
        return series;
    }

    private int getResourceIdByName(String aString) {
        String packageName = getPackageName();
        aString = aString.toLowerCase();
        int resId = getResources().getIdentifier(aString, "raw", packageName);
        return resId;
    }
}

