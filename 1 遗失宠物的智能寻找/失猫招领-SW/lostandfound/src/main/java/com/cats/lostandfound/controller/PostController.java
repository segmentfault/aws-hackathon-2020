package com.cats.lostandfound.controller;

import com.cats.lostandfound.entity.Filter;
import com.cats.lostandfound.entity.Message;
import com.cats.lostandfound.entity.Post;
import com.cats.lostandfound.service.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/post")
public class PostController {
    @Autowired
    PostService postService;

    /**
     * 当用户新建一个post的时候调用，返回一个Post对象，但仅有post_id和user_id填充了
     * 主要是后面的图片上传时需要post_id参数
     * @param post
     * @return
     */
    @PostMapping(value = "/add")
    public Message<Post> addPost(Post post){
        return postService.addPost(post);
    }

    /**
     * 当用户修改或者点击发表的时候调用这个，除了timestamp都要填充
     * @param post
     * @return
     */
    @PostMapping(value = "/update")
    public Message<Post> updatePost(Post post){
        return postService.updatePost(post);
    }

    /**
     * 当用户取消发表或者删除post时调用，只需填充post_id
     * @param post_id
     * @return
     */
    @GetMapping(value = "/delete")
    public Message<Post> deletePost(long post_id){
        return postService.deletePost(post_id);
    }

    /**
     * 用户用过滤器筛选posts，如果某一选项是全部，就不填充，使之为null
     * @param filter
     * @return
     */
    @PostMapping(value = "/search")
    public Message<List<Post>> findPostByFilters(Filter filter){
        return postService.findPostsByFilters(filter);
    }

    /**
     * 用户打开自己的主页时能看到自己发布的历史posts，这时通过user_id获取当前用户的所有posts
     * @param user_id
     * @return
     */
    @GetMapping(value = "/user_id")
    public Message<List<Post>> findPostByUserId(long user_id){
        return postService.findPostsByUserId(user_id);
    }

    /**
     * 通过post_id获取单个post，注意同时还需要通过photo的API根据post_id获取所有图片的路径
     * @param post_id
     * @return
     */
    @GetMapping(value = "/post_id")
    public Message<Post> findPostByPostId(long post_id){
        return postService.findPostsByPostId(post_id);
    }
}
