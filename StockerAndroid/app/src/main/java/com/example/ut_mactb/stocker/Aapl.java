package com.example.ut_mactb.stocker;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Aapl extends Activity {

    Button model;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_aapl1);


        model = (Button) findViewById(R.id.button1);

        model.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openActivity1();
            }
        });
    }

        public void openActivity1(){

            Intent intent = new Intent(this, Models.class);
            startActivity(intent);
        }






}
