<template lang="html">
  <div class="NotFoundPage">
    <h1>404 Page Not Found</h1>
    <p>
      返回<router-link :to="{ name: 'home' }">主页</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage'
}
</script>

<style lang="css">
</style>
