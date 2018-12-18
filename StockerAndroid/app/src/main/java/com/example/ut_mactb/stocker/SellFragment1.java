package com.example.ut_mactb.stocker;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

public class SellFragment1 extends Fragment {

    private ListView mListView1,mListView2,mListView3,mListView4;
    private CompanyListAdapter adapter;
    private ArrayList<Company> company;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view =inflater.inflate(R.layout.fragment_sell, container, false);

        company = new ArrayList<>();

        company.add(new Company("Apple" , 67));
        company.add(new Company("Microsoft" , 58));


        mListView1 = (ListView)view.findViewById(R.id.listView1);
        mListView2 = (ListView)view.findViewById(R.id.listView2);
        mListView3 = (ListView)view.findViewById(R.id.listView3);
        mListView4 = (ListView)view.findViewById(R.id.listView4);

        adapter = new CompanyListAdapter(getActivity(),company );
        mListView1.setAdapter(adapter);
        mListView2.setAdapter(adapter);
        mListView3.setAdapter(adapter);
        mListView4.setAdapter(adapter);


       ListUtils.setDynamicHeight(mListView1);
       ListUtils.setDynamicHeight(mListView2);


        mListView1.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {


                Toast.makeText(getActivity(), "Clicked", Toast.LENGTH_SHORT).show();
            }
        });



        return view;
    }

    public static class ListUtils {
        public static void setDynamicHeight(ListView mListView) {
            ListAdapter mListAdapter = mListView.getAdapter();
            if (mListAdapter == null) {
                // when adapter is null
                return;
            }
            int height = 0;
            int desiredWidth = View.MeasureSpec.makeMeasureSpec(mListView.getWidth(), View.MeasureSpec.UNSPECIFIED);
            for (int i = 0; i < mListAdapter.getCount(); i++) {
                View listItem = mListAdapter.getView(i, null, mListView);
                listItem.measure(desiredWidth, View.MeasureSpec.UNSPECIFIED);
                height += listItem.getMeasuredHeight();
            }
            ViewGroup.LayoutParams params = mListView.getLayoutParams();
            params.height = height + (mListView.getDividerHeight() * (mListAdapter.getCount() - 1));
            mListView.setLayoutParams(params);
            mListView.requestLayout();
        }
    }
}
