package com.cats.lostandfound.entity;

/**
 * photo_id:图片id
 * post_id:post的id
 * path:路径，就是那个key
 * photo_index:图片序号，1表示第一张，也就是封面
 * cat_class:猫的种类，0到12
 */
public class Photo {
    private long photo_id;
    private long post_id;
    private String path;
    private int photo_index;
    private int cat_class;

    public long getPhoto_id() {
        return photo_id;
    }

    public void setPhoto_id(long photo_id) {
        this.photo_id = photo_id;
    }

    public long getPost_id() {
        return post_id;
    }

    public void setPost_id(long post_id) {
        this.post_id = post_id;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public int getPhoto_index() {
        return photo_index;
    }

    public void setPhoto_index(int photo_index) {
        this.photo_index = photo_index;
    }

    public int getCat_class() {
        return cat_class;
    }

    public void setCat_class(int cat_class) {
        this.cat_class = cat_class;
    }

    @Override
    public String toString() {
        return "Photo{" +
                "photo_id=" + photo_id +
                ", post_id=" + post_id +
                ", path='" + path + '\'' +
                ", index=" + photo_index +
                ", cat_class=" + cat_class +
                '}';
    }
}
