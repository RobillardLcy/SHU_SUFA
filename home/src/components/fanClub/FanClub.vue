<template lang="html">
  <div class="FanClub">
    <h1>{{ $route.params.club }}</h1>
  </div>
</template>

<script>
export default {
  name: 'FanClub'
  // TODO: 根据路由中提供的club，从后台数据库中调出各球迷会的页面信息
}
</script>

<style lang="css">
</style>
