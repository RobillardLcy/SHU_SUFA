<template lang="html">
  <div class="Activities">
    <h1>{{ $route.params.activity }}</h1>
  </div>
</template>

<script>
export default {
  name: 'Activities'
  // TODO: 根据路由activity，从后台数据库中调出活动信息
}
</script>

<style lang="css">
</style>
