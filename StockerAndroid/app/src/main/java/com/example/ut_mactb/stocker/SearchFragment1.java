package com.example.ut_mactb.stocker;


import android.content.Intent;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;

import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;

import android.os.Bundle;
import android.os.Environment;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;

import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.MultiAutoCompleteTextView;
import android.widget.Toast;
import java.io.IOException;
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


public class SearchFragment1 extends Fragment {
    AutoCompleteTextView text;
    MultiAutoCompleteTextView text1;
    String[] languages={"Apple Inc. ( AAPL ) ","Berkshire Hathaway ( BRK.A )","Microsoft ( MSFT )","Wells Fargo (WFC)"};

    @Override
    @Nullable
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_search1, container, false);

        text=(AutoCompleteTextView)view.findViewById(R.id.autoCompleteTextView1);
        text1=(MultiAutoCompleteTextView)view.findViewById(R.id.multiAutoCompleteTextView1);

        ArrayAdapter adapter = new
                ArrayAdapter(getActivity(),android.R.layout.simple_list_item_1,languages);

        text.setAdapter(adapter);
        text.setThreshold(1);

        text1.setAdapter(adapter);
        text1.setTokenizer(new MultiAutoCompleteTextView.CommaTokenizer());

        text.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,long arg3) {

                if(arg0.getItemAtPosition(arg2).toString().equals("Apple Inc. ( AAPL )")){

                    Intent intent = new Intent(getActivity(), Aapl.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Berkshire Hathaway  ( BRK.A )")){
                    Intent intent = new Intent(getActivity(), Brk.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Microsoft (MSFT)")){
                    Intent intent = new Intent(getActivity(), Msft.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Wells Fargo (WFC)")){
                    Intent intent = new Intent(getActivity(), Wfc.class);
                    startActivity(intent);
                }


                Toast.makeText(getActivity(),(CharSequence)arg0.getItemAtPosition(arg2), Toast.LENGTH_LONG).show();

            }
        });

        text1.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,long arg3) {

                if(arg0.getItemAtPosition(arg2).toString().equals("Apple Inc. ( AAPL )")){

                    Intent intent = new Intent(getActivity(), Aapl.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Berkshire Hathaway  ( BRK.A )")){
                    Intent intent = new Intent(getActivity(), Brk.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Microsoft (MSFT)")){
                    Intent intent = new Intent(getActivity(), Msft.class);
                    startActivity(intent);
                }
                else if(arg0.getItemAtPosition(arg2).toString().equals("Wells Fargo (WFC)")){
                    Intent intent = new Intent(getActivity(), Wfc.class);
                    startActivity(intent);
                }


                Toast.makeText(getActivity(),(CharSequence)arg0.getItemAtPosition(arg2), Toast.LENGTH_LONG).show();

            }
        });

        return view;
    }
}

