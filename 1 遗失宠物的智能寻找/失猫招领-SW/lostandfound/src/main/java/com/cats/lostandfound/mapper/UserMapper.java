package com.cats.lostandfound.mapper;

import com.cats.lostandfound.entity.User;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

/**
 * mapper的具体表达式
 */
@Mapper //标记mapper文件位置，否则在Application.class启动类上配置mapper包扫描
@Repository
public interface UserMapper {

    /**
     * 查询用户名是否存在，若存在，不允许注册
     * 注解@Param(value) 若value与可变参数相同，注解可省略
     * 注解@Results  列名和字段名相同，注解可省略
     * @param email
     * @return
     */
    @Select(value = "select u.email,u.password from user u where u.email=#{email}")
    @Results
            ({@Result(property = "email",column = "email"),
                    @Result(property = "password",column = "password")})
    User findUserByEmail(@Param("email") String email);

    /**
     * 注册  插入一条user记录
     * @param user
     * @return
     */
    @Insert("insert into user(email, password) values(#{email}, #{password})")
    //加入该注解可以保存对象后，查看对象插入id
    @Options(useGeneratedKeys = true,keyProperty = "user_id")
    void regist(User user);

    /**
     * 登录
     * @param user
     * @return
     */
    @Select("select u.user_id from user u where u.email = #{email} and password = #{password}")
    Long login(User user);
}