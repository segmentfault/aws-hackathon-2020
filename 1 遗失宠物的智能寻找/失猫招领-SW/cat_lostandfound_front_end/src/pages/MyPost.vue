<template>
  <div>
    <me-list :api="fetchPostByUser"></me-list>
  </div>
</template>

<script>
  import List from '../components/List.vue'

  export default {
    name: 'MyPost',

    components: {
      'me-list': List,
    },

    methods: {
      fetchPostByUser() {
        return this.$request.getPostByUser()
      },
    },
  }
</script>

<style lang="scss" scoped></style>
