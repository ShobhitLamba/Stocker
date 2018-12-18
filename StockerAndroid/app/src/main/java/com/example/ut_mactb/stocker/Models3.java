package com.example.ut_mactb.stocker;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class Models3 extends Activity{

    Button tech,tsa, pa;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_models3);


        tech = (Button) findViewById(R.id.button2);
        tsa = (Button) findViewById(R.id.button3);
        pa = (Button) findViewById(R.id.button4);

        tech.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                openActivity2();


            }
        });

        tsa.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                openActivity3();

            }
        });


        pa.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                openActivity4();

            }
        });
    }

    public void openActivity2(){

        Intent intent = new Intent(this, Appl_tsa.class);
        startActivity(intent);
    }

    public void openActivity3(){

        Intent intent = new Intent(this, Main2Activity.class);
        startActivity(intent);
    }

    public void openActivity4(){

        Intent intent = new Intent(this, ChartActivity.class);
        startActivity(intent);
    }
}
