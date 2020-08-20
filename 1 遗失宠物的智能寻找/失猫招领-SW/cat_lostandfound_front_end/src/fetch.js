function request(url, params, method = 'POST') {
  // 用于开发的base, /api将被代理到线上的环境
  // const base = '/api'

  // 用于部署到线上环境的base
  const base =
    'http://lostandfound-env.eba-ftezekhq.ap-northeast-1.elasticbeanstalk.com'

  const data = new FormData()
  if (Object.prototype.toString.call(params))
    Object.keys(params).forEach((k) => data.append(k, params[k]))

  return new Promise((resolve) => {
    if (method === 'POST') {
      fetch(base + url, {
        method: method,
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data,
      })
        .then((response) => {
          resolve(response.json())
        })
        .catch((error) => {
          throw new Error(error)
        })
    } else if (method === 'GET') {
      const keys = Object.keys(params)
      const query = []

      if (keys.length > 0)
        Object.keys(params).forEach((k) => query.push(`${k}=${params[k]}`))
      const queryString = '?' + query.join('&')

      fetch(base + url + queryString, {
        method: method,
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
        .then((response) => {
          resolve(response.json())
        })
        .catch((error) => {
          throw new Error(error)
        })
    }
  })
}

export default {
  join(params) {
    return request('/user/regist', {
      email: params.email,
      password: params.password,
    })
  },

  login(params) {
    return request('/user/login', {
      email: params.email,
      password: params.password,
    })
  },

  getPostByFilter(params) {
    return request('/post/search', {
      location: params.location,
      cat_class: params.cat_class,
      type: params.type,
      status: params.status,
      adult: params.adult,
      startTime: params.startTime,
      endTime: params.endTime,
    })
  },

  getPost(post_id) {
    return request(
      '/post/post_id',
      {
        post_id,
      },
      'GET'
    )
  },

  getPostByUser() {
    return request(
      '/post/user_id',
      {
        user_id: JSON.parse(localStorage.getItem('token')),
      },
      'GET'
    )
  },

  addPost() {
    return request('/post/add', {
      user_id: JSON.parse(localStorage.getItem('token')),
    })
  },

  updatePost(params) {
    return request('/post/update', {
      user_id: JSON.parse(localStorage.getItem('token')),
      post_id: params.post_id,
      title: params.title,
      location: params.location,
      cat_class: params.cat_class,
      type: params.type,
      adult: params.adult,
      description: params.description,
      cover_path: params.cover_path,
      lof_time: params.lof_time,
      email_notify: 0,
    })
  },

  deletePost(post_id) {
    return request(
      '/post/delete',
      {
        post_id,
      },
      'GET'
    )
  },

  getPostPhoto(post_id) {
    return request(
      '/photo/get_photos',
      {
        post_id,
      },
      'GET'
    )
  },

  addPostPhoto(params) {
    return request('/photo/add', {
      post_id: params.post_id,
      path: params.path,
      cat_class: params.cat_class,
      photo_index: params.photo_index,
    })
  },

  deletePostPhoto(post_id) {
    return request(
      '/photo/delete_by_post_id',
      {
        post_id,
      },
      'GET'
    )
  },

  AWS_S3_Upload({ post_id, file }) {
    const albumPhotosKey = encodeURIComponent(post_id) + '/'
    const photoKey = albumPhotosKey + file.name

    // eslint-disable-next-line no-undef
    return new AWS.S3.ManagedUpload({
      params: {
        Bucket: 'fzhcats',
        Key: photoKey,
        Body: file,
        ACL: 'public-read',
      },
    }).promise()
  },


  AWS_S3_DeleteAlbum({ post_id }) {
    const albumKey = encodeURIComponent(post_id) + '/'

    // eslint-disable-next-line no-undef
    s3.listObjects({ Prefix: albumKey }, (err, data) => {
      if (err) return console.log(err.message)

      const objects = data.Contents.map((object) => {
        return { Key: object.Key }
      })

      // eslint-disable-next-line no-undef
      s3.deleteObjects({ Delete: { Objects: objects, Quiet: true } }, (err) => {
        if (err) return console.error(err.message)
      })
    })
  },

  AWS_S3_DeletePhoto({ photoKey }) {
    // eslint-disable-next-line no-undef
    s3.deleteObject({ Key: photoKey }, (err) => err && console.error(err))
  },
}
