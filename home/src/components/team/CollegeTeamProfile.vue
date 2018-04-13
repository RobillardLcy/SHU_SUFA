<template lang="html">
  <div class="CollegeTeamProfile">
    <h3>学院队伍详细信息</h3>
    {{ collegeProfile.id }}
    {{ collegeProfile.name }}
    {{ collegeProfile.logo }}
    {{ collegeProfile.description }}
    {{ collegeProfile.create_at }}
    {{ collegeProfile.captain.studentID }}
    {{ collegeProfile.captain.name }}
  </div>
</template>

<script>
export default {
  name: 'CollegeTeamProfile',
  data: () => ({
    collegeProfile: {
      id: null,
      name: null,
      logo: null,
      description: null,
      captain: {
        studentID: null,
        name: null
      },
      create_at: null
    }
  }),
  mounted: function () {
    this.collegeProfile.id = this.$route.params.college_id
    this.getCollegeTeamProfile()
  },
  methods: {
    getCollegeTeamProfile: function () {
      let url = 'colleges/profile/' + this.collegeProfile.id + '/'
      this.$axios.get(url)
        .then(response => {
          this.collegeProfile.name = response.data.name
          this.collegeProfile.logo = response.data.logo
          this.collegeProfile.description = response.data.description
          this.collegeProfile.create_at = response.data.create_at
          this.collegeProfile.captain.studentID = response.data.captain.studentID
          this.collegeProfile.captain.name = response.data.catch.name
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style lang="css">
</style>
