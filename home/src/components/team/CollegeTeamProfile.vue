<template lang="html">
  <div class="CollegeTeamProfile">
    <v-card>
      <v-container>
        <v-layout row text-xs-center>
          <v-flex xs2>
            <v-card-media
              :src="collegeProfile.logo"
              height="60px"
              contain></v-card-media>
          </v-flex>
          <v-flex xs10>
            <div class="headline">{{ collegeProfile.name }}</div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
    <br/>
    <div class="headline">学院成员</div>
    <br/>
    <v-card>
      <v-data-table
        :headers="teamMembersHeaders"
        :items="collegeProfile.members"
        item-key="id">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.id }}</td>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.gender }}</td>
          <td>{{ props.item.num }}</td>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'CollegeTeamProfile',
  data: () => ({
    teamMembersHeaders: [
      {
        text: '学号',
        value: 'id'
      },
      {
        text: '姓名',
        value: 'name'
      },
      {
        text: '性别',
        value: 'gender'
      },
      {
        text: '号码',
        value: 'num'
      }
    ],
    collegeProfile: {
      id: null,
      name: null,
      logo: null,
      description: null,
      captain: {
        studentID: null,
        name: null
      },
      create_at: null,
      members: []
    }
  }),
  mounted: function () {
    this.collegeProfile.id = this.$route.params.college_id
    this.getCollegeTeamProfile()
  },
  methods: {
    getCollegeTeamProfile: function () {
      let url = 'colleges/profile/' + this.collegeProfile.id
      this.$axios.get(url)
        .then(response => {
          this.collegeProfile.name = response.data['info'].name
          this.collegeProfile.logo = response.data['info'].logo
          this.collegeProfile.description = response.data['info'].description
          this.collegeProfile.create_at = response.data['info'].create_at
          this.collegeProfile.captain.id = response.data['info'].captain_id
          this.collegeProfile.captain.name = response.data['info'].captain_name
          this.collegeProfile.captain.mobile = response.data['info'].captain_mobile
          for (var i = 0; i < response.data['members'].length; i++) {
            this.collegeProfile.members.push({
              id: response.data['members'][i].id,
              name: response.data['members'][i].name,
              gender: (response.data['members'][i].gender === 'male') ? '男' : '女',
              number: response.data['members'][i].num
            })
          }
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
