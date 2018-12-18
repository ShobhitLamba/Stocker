package com.example.ut_mactb.stocker;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.ArrayList;


public class PatternAdapter extends BaseAdapter {

    Context context;
    ArrayList<String> patternList;
    ArrayList<String> patternNameList;
    ArrayList<String> patternPredictionList;
    ArrayList<String> patternAccuracyList;

    public PatternAdapter(Context ctx, ArrayList<String> mPatternList, ArrayList<String> mPatternNameList, ArrayList<String> mPatternPredictionList, ArrayList<String> mPatternAccuracyList) {
        this.context = ctx;
        this.patternList = mPatternList;
        this.patternNameList = mPatternNameList;
        this.patternPredictionList = mPatternPredictionList;
        this.patternAccuracyList = mPatternAccuracyList;
    }

    @Override
    public int getCount() {
        return patternList.size();
    }

    @Override
    public Object getItem(int position) {
        return patternList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View currentView;
        if (convertView == null) {
            convertView = View.inflate(context, R.layout.pattern_list_layout, null);
        }
        currentView = convertView;
        TextView patternNameTextView = (TextView) currentView.findViewById(R.id.patternNameTextView);
        TextView patternPredictionTextView = (TextView) currentView.findViewById(R.id.patternPredictionTextView);
        TextView patternAccuracyTextView = (TextView) currentView.findViewById(R.id.patternAccuracyTextView);

        patternNameTextView.setText(patternNameList.get(position));
        if (patternNameTextView.getText().equals(ChartActivity.PATTERN)) {
            patternNameTextView.setTextColor(Color.WHITE);
            patternNameTextView.setTypeface(null, Typeface.BOLD);
            currentView.setBackgroundColor(Color.GRAY);
        } else {
            patternNameTextView.setTextColor(Color.GRAY);
            patternNameTextView.setTypeface(null, Typeface.NORMAL);
            currentView.setBackgroundColor(Color.WHITE);
        }

        patternPredictionTextView.setText(patternPredictionList.get(position));
        if (patternPredictionTextView.getText().equals(ChartActivity.HIGH)) {
            patternPredictionTextView.setTextColor(Color.rgb(0, 153, 51));
        } else if (patternPredictionTextView.getText().equals(ChartActivity.LOW)) {
            patternPredictionTextView.setTextColor(Color.RED);
        } else {
            patternPredictionTextView.setTextColor(Color.WHITE);
            patternPredictionTextView.setTypeface(null, Typeface.BOLD);
        }

        patternAccuracyTextView.setText(patternAccuracyList.get(position));
        if (patternAccuracyTextView.getText().equals(ChartActivity.ACCURACY)) {
            patternAccuracyTextView.setTextColor(Color.WHITE);
            patternAccuracyTextView.setTypeface(null, Typeface.BOLD);
        } else {
            patternAccuracyTextView.setTextColor(Color.GRAY);
            patternAccuracyTextView.setTypeface(null, Typeface.NORMAL);
        }
        return currentView;
    }
}
