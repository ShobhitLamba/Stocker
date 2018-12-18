package com.example.ut_mactb.stocker;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Toast;

public class SearchFragment extends Fragment {

    private static final String[] COMPANIES = new String[]{
            "Apple", "Berkshire Hathaway", "Microsoft", "Wells Fargo"};

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_search, container, false);


        String[] companies = getResources().getStringArray(R.array.companies);

        AutoCompleteTextView editText = view.findViewById(R.id.actv);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActivity(),
                android.R.layout.simple_list_item_1,companies);
        editText.setAdapter(adapter);



        editText.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,long arg3) {

                if(arg0.getItemAtPosition(arg2).toString().equals("Apple")){

                    Intent intent = new Intent(getActivity(), Aapl.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Berkshire Hathaway")){
                    Intent intent = new Intent(getActivity(), Brk.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Microsoft")){
                    Intent intent = new Intent(getActivity(), Msft.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Wells Fargo")){
                    Intent intent = new Intent(getActivity(), Wfc.class);
                    startActivity(intent);
                }


                Toast.makeText(getActivity(),(CharSequence)arg0.getItemAtPosition(arg2), Toast.LENGTH_LONG).show();

            }
        });


        return view;
    }
}
