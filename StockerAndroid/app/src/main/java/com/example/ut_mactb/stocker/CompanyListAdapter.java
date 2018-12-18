package com.example.ut_mactb.stocker;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.ArrayList;

public class CompanyListAdapter extends BaseAdapter {

    private Context c;
    private ArrayList<Company> company;

    public CompanyListAdapter(Context c, ArrayList<Company> company) {
        this.c = c;
        this.company = company;
    }

    @Override
    public int getCount() {
        return company.size();
    }

    @Override
    public Object getItem(int position) {
        return company.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        View v = View.inflate(c, R.layout.list_item, null);
        TextView CompanyName = (TextView)v.findViewById(R.id.text1);
        TextView AccuracyValue = (TextView)v.findViewById(R.id.text2);

        CompanyName.setText(company.get(position).getName());
        AccuracyValue.setText(String.valueOf(company.get(position).getAccuracy()) + "%");

        return v;
    }
}
