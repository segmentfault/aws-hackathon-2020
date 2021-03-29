package com.example.falldetect;

import android.app.Activity;

import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.support.common.FileUtil;

import java.io.IOException;
import java.nio.MappedByteBuffer;

public class Model {

    private static Interpreter interpreter = null;

    private static Model model = new Model();

    private Model(){};

    public static synchronized boolean inference(Activity activity, float[] input) {
        if (interpreter == null) {
            MappedByteBuffer model = null;
            try {
                model = FileUtil.loadMappedFile(activity, "model.tflite");
            } catch (IOException e) {
                e.printStackTrace();
            }
            interpreter = new Interpreter(model
                    , new Interpreter.Options().setNumThreads(4));
        }
        float[] singleInput = new float[30*9];
        float[][] singleOutput = new float[1][2];
        System.arraycopy(input, 30*9, singleInput, 0,
                Math.min(input.length - 30*9, 30*9));
        interpreter.run(singleInput, singleOutput);
        return singleOutput[0][1] > 0.5;
    }

}