package com.example.falldetect;

import androidx.appcompat.app.AppCompatActivity;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.TextView;

import java.util.List;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private TextView accX;
    private TextView accY;
    private TextView accZ;
    private TextView gyroX;
    private TextView gyroY;
    private TextView gyroZ;
    private TextView orientX;
    private TextView orientY;
    private TextView orientZ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 获得SensorManager对象
        SensorManager sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        // 注册加速度传感器
        sensorManager.registerListener(this,
                sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),
                SensorManager.SENSOR_DELAY_FASTEST);

        // 注册陀螺仪传感器
        sensorManager.registerListener(this,
                sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE),
                SensorManager.SENSOR_DELAY_FASTEST);

        // 注册方向传感器
        sensorManager.registerListener(this,
                sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION),
                SensorManager.SENSOR_DELAY_FASTEST);

        accX = findViewById(R.id.acc_x);
        accY = findViewById(R.id.acc_y);
        accZ = findViewById(R.id.acc_z);
        gyroX = findViewById(R.id.gyro_x);
        gyroY = findViewById(R.id.gyro_y);
        gyroZ = findViewById(R.id.gyro_z);
        orientX = findViewById(R.id.orient_x);
        orientY = findViewById(R.id.orient_y);
        orientZ = findViewById(R.id.orient_z);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        // 通过getType方法获得当前传回数据的传感器类型
        switch(event.sensor.getType()) {
            case Sensor.TYPE_ACCELEROMETER: // 处理加速度传感器传回的数据
                accX.setText(String.valueOf(event.values[0]));
                accY.setText(String.valueOf(event.values[1]));
                accZ.setText(String.valueOf(event.values[2]));
            break;
            case Sensor.TYPE_GYROSCOPE: // 处理陀螺仪传感器传回的数据
                gyroX.setText(String.valueOf(event.values[0]));
                gyroY.setText(String.valueOf(event.values[1]));
                gyroZ.setText(String.valueOf(event.values[2]));
            break;
            case Sensor.TYPE_ORIENTATION: // 处理方向传感器传回的数据
                orientX.setText(String.valueOf(event.values[0]));
                orientY.setText(String.valueOf(event.values[1]));
                orientZ.setText(String.valueOf(event.values[2]));
            break;
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}
