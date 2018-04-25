<template lang="html">
  <div class="FreeTeamProfile">
    <v-card>
      <v-container>
        <v-layout row text-xs-center>
          <v-flex xs2>
            <v-card-media
              :src="teamProfile.logo"
              height="60px"
              contain></v-card-media>
          </v-flex>
          <v-flex xs10>
            <div class="headline">{{ teamProfile.name }}</div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
    <br/>
    <div class="headline">队伍成员</div>
    <br/>
    <v-card>
      <v-data-table
        :headers="teamMembersHeaders"
        :items="teamProfile.members"
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
  name: 'FreeTeamProfile',
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
    teamProfile: {
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
    if (this.$route.params.team_id <= 1000) {
      this.$router.push('/team/free-team')
    } else {
      this.teamProfile.id = this.$route.params.team_id
      this.getFreeTeamProfile()
    }
  },
  methods: {
    getFreeTeamProfile: function () {
      let url = 'free-team/profile/' + this.teamProfile.id
      this.$axios.get(url)
        .then(response => {
          this.teamProfile.name = response.data['info'].name
          this.teamProfile.logo = response.data['info'].logo
          this.teamProfile.description = response.data['info'].description
          this.teamProfile.create_at = response.data['info'].create_at
          this.teamProfile.captain.id = response.data['info'].captain_id
          this.teamProfile.captain.name = response.data['info'].captain_name
          this.teamProfile.captain.mobile = response.data['info'].captain_mobile
          for (var i = 0; i < response.data['members'].length; i++) {
            this.teamProfile.members.push({
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
