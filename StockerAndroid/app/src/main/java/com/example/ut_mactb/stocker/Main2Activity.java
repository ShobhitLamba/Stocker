package com.example.ut_mactb.stocker;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;

import java.io.InputStream;

public class Main2Activity extends AppCompatActivity {
    private WebView webview, webview1, webview2, webview3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        webview = findViewById(R.id.webView);
        InputStream ins = getResources().openRawResource(
                getResources().getIdentifier("tsa_wfc_pred",
                        "raw", getPackageName()));
        InputStream ins1 = getResources().openRawResource(
                getResources().getIdentifier("tsa_wfc_real",
                        "raw", getPackageName()));
        //Log.i("ins", ins.toString());
        //Log.i("ins1",ins1.toString());
        ReadData rd = new ReadData();
        String data = rd.readData(ins,ins1);
        String companyName = "Apple INC";
        String content = rd.getWebData(data,companyName);
        //Log.i("Webviewwww",content);
        String encodedHtml = Base64.encodeToString(content.getBytes(), Base64.NO_PADDING);
        WebSettings webSettings = webview.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setUseWideViewPort(true);
        webview.requestFocusFromTouch();
        webview.loadData(encodedHtml, "text/html", "base64");


        webview1 = findViewById(R.id.webView1);
        ins = getResources().openRawResource(
                getResources().getIdentifier("aapl_7_pred",
                        "raw", getPackageName()));
        ins1 = getResources().openRawResource(
                getResources().getIdentifier("aapl_7_real",
                        "raw", getPackageName()));
        rd = new ReadData();
        data = rd.readData(ins,ins1);
        content = rd.getWebData(data,companyName);
        encodedHtml = Base64.encodeToString(content.getBytes(), Base64.NO_PADDING);
        webSettings = webview1.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setUseWideViewPort(true);
        webview1.requestFocusFromTouch();
        webview1.loadData(encodedHtml, "text/html", "base64");



        webview2 = findViewById(R.id.webView2);
        ins = getResources().openRawResource(
                getResources().getIdentifier("aapl_30_pred",
                        "raw", getPackageName()));
        ins1 = getResources().openRawResource(
                getResources().getIdentifier("aapl_30_real",
                        "raw", getPackageName()));
        rd = new ReadData();
        data = rd.readData(ins,ins1);
        //String header = "['Data','Predicted movement','Real movement']";
        content = rd.getWebData(data,companyName);
        Log.i("aapl_30",content);
        encodedHtml = Base64.encodeToString(content.getBytes(), Base64.NO_PADDING);
        webSettings = webview2.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setUseWideViewPort(true);
        webview2.requestFocusFromTouch();
        webview2.loadData(encodedHtml, "text/html", "base64");



        webview3 = findViewById(R.id.webView3);
        ins = getResources().openRawResource(
                getResources().getIdentifier("aapl_60_pred",
                        "raw", getPackageName()));
        ins1 = getResources().openRawResource(
                getResources().getIdentifier("aapl_60_real",
                        "raw", getPackageName()));
        rd = new ReadData();
        data = rd.readData(ins,ins1);
        content = rd.getWebData(data,companyName);
        Log.i("aapl_60",content);
        encodedHtml = Base64.encodeToString(content.getBytes(), Base64.NO_PADDING);
        webSettings = webview3.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setUseWideViewPort(true);
        webview3.requestFocusFromTouch();
        webview3.loadData(encodedHtml, "text/html", "base64");


    }
}

