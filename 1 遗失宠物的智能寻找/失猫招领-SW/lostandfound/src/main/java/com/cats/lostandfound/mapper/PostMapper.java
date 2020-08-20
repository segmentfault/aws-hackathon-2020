package com.cats.lostandfound.mapper;

import com.cats.lostandfound.entity.Filter;
import com.cats.lostandfound.entity.Post;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper //标记mapper文件位置，否则在Application.class启动类上配置mapper包扫描
@Repository
public interface PostMapper {

    @Insert("insert into post(user_id, location, title, description, cat_class, adult, type, status, cover_path, timestamp, lof_time, email_notify) " +
            "values(#{user_id}, #{location}, #{title}, #{description},#{cat_class}, #{adult}, #{type},#{status},#{cover_path},#{timestamp},#{lof_time},#{email_notify})")
    @Options(useGeneratedKeys = true,keyProperty = "post_id")
    void post(Post post);

    @Select(value = "select * from post where user_id=#{user_id} order by timestamp desc")
    @Results(id="postMap", value={
            @Result(property = "post_id",column = "post_id"),
            @Result(property = "user_id",column = "user_id"),
            @Result(property = "location",column = "location"),
            @Result(property = "title",column = "title"),
            @Result(property = "description",column = "description"),
            @Result(property = "cat_class",column = "cat_class"),
            @Result(property = "adult",column = "adult"),
            @Result(property = "type",column = "type"),
            @Result(property = "status",column = "status"),
            @Result(property = "cover_path",column = "cover_path"),
            @Result(property = "timestamp",column = "timestamp"),
            @Result(property = "lof_time",column = "lof_time"),
            @Result(property = "email_notify",column = "email_notify")
    })
    List<Post> findPostsByUserId(@Param("user_id") long user_id);

    @Select(value = "select * from post where post_id=#{post_id} order by timestamp desc")
    @ResultMap("postMap")
    Post findPostByPostId(@Param("post_id") long post_id);

    @Update("update post set location=#{location}, title=#{title}, " +
            "description = #{description}, cat_class = #{cat_class}, " +
            "type = #{type}, status = #{status}, cover_path = #{cover_path}, " +
            "timestamp = #{timestamp}, " + "lof_time = #{lof_time}, " +
            "email_notify = #{email_notify}, " + "adult = #{adult} " +
            " where post_id = #{post_id} ")
    void updatePost(@Param("post_id")long post_id, @Param("location")String location, @Param("title")String title,
                    @Param("description")String description, @Param("cat_class")int cat_class,
                    @Param("type")int type, @Param("status")int status, @Param("cover_path") String cover_path,
                    @Param("timestamp") long timestamp, @Param("lof_time") long lof_time,
                    @Param("email_notify") int email_notify, @Param("adult") int adult);

    @Delete("delete from post where post_id=#{post_id}")
    void deleteByPostId(@Param("post_id") long post_id);

    @Select({"<script>",
            " select * from post ",
            " where 1=1 ",
            "<when test='location!=null'>",
            " and location = #{location} ",
            "</when>",
            "<when test='cat_class!=-1'>",
            " and cat_class = #{cat_class} ",
            "</when>",
            "<when test='type!=-1'>",
            " and type = #{type} ",
            "</when>",
            "<when test='status!=-1'>",
            " and status = #{status} ",
            "</when>",
            "<when test='adult!=-1'>",
            " and adult = #{adult} ",
            "</when>",
            "<when test='startTime!=-1'>",
            " and lof_time &gt; #{startTime} ",
            "</when>",
            "<when test='endTime!=-1'>",
            " and lof_time &lt;= #{endTime} ",
            "</when>",
            " order by timestamp desc ",
            "</script>"})
    @ResultMap("postMap")
    List<Post> findPostsByFilters(Filter filter);

}