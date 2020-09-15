package com.example.dogface.utils;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpMethod;
import org.apache.commons.httpclient.NameValuePair;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.multipart.FilePart;
import org.apache.commons.httpclient.methods.multipart.MultipartRequestEntity;
import org.apache.commons.httpclient.methods.multipart.Part;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;

public class FaceCodeUtil {

    public static String getFaceCode(MultipartFile imageFile) {
        FilePart fp = null;
        try {
            fp = new FilePart("img", multipartFileToFile(imageFile));
        } catch (Exception e) {
            e.printStackTrace();
        }
        Part[] parts = { fp };
        HttpClient client = new HttpClient();
        HttpMethod method = new PostMethod("https://u7i2o7rmvb.execute-api.cn-northwest-1.amazonaws.com.cn/default/dogfacenetapi");
        MultipartRequestEntity mre = new MultipartRequestEntity(parts, method.getParams());
        try {
            client.executeMethod(method);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String res = "";
        try {
            res = method.getResponseBodyAsString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //释放连接
        method.releaseConnection();
        JSONObject jsonObject = JSONObject.parseObject(res);
        JSONArray array = (JSONArray) jsonObject.getJSONObject("body").getJSONArray("predictions").get(0);
        String facecode = "";
        for (int i = 0 ; i < array.size() ; i++) {
            facecode += String.valueOf(array.getFloat(i)) + ",";
        }
        return facecode.substring(0, facecode.length()-1);
    }

    public static double getDistance(String facecode1, String facecode2) {
        String[] codes1 = facecode1.split(",");
        String[] codes2 = facecode2.split(",");
        double d = 0;
        for (int i = 0 ; i < 32 ; i++) {
            d += Math.pow(Double.valueOf(codes1[i])-Double.valueOf(codes2[i]), 2);
        }
        return d;
    }

    public static File multipartFileToFile(MultipartFile file) throws Exception {

        File toFile = null;
        if (file.equals("") || file.getSize() <= 0) {
            file = null;
        } else {
            InputStream ins = null;
            ins = file.getInputStream();
            toFile = new File(file.getOriginalFilename());
            inputStreamToFile(ins, toFile);
            ins.close();
        }
        return toFile;
    }

    //获取流文件
    private static void inputStreamToFile(InputStream ins, File file) {
        try {
            OutputStream os = new FileOutputStream(file);
            int bytesRead = 0;
            byte[] buffer = new byte[8192];
            while ((bytesRead = ins.read(buffer, 0, 8192)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            os.close();
            ins.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
