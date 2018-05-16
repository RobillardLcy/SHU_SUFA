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
    <v-card v-show="!collegeProfile.collegeMember">
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
    <v-card v-show="collegeProfile.collegeMember">
      <v-data-table
        :headers="teamMembersProfileHeaders"
        :items="collegeProfile.members"
        item-key="id">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.id }}</td>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.gender }}</td>
          <td>{{ props.item.mobile }}</td>
          <td>{{ props.item.num }}</td>
          <td>{{ props.item.join }}</td>
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
    teamMembersProfileHeaders: [
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
        text: '电话',
        value: 'mobile'
      },
      {
        text: '号码',
        value: 'num'
      },
      {
        text: '入队时间',
        value: 'join'
      }
    ],
    collegeProfile: {
      collegeMember: false,
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
    if (this.$route.params.college_id > 1000) {
      this.$router.push('/team/college-team')
    } else {
      this.collegeProfile.id = this.$route.params.college_id
      this.getCollegeTeamProfile()
    }
  },
  methods: {
    getCollegeTeamProfile: function () {
      let url = 'league/colleges/profile/' + this.collegeProfile.id + '/'
      this.$axios.get(url)
        .then(response => {
          this.collegeProfile.name = response.data['info'].name
          this.collegeProfile.logo = response.data['info'].logo
          this.collegeProfile.description = response.data['info'].description
          this.collegeProfile.create_at = response.data['info'].create_at
          this.collegeProfile.captain.id = response.data['info'].captain_id
          this.collegeProfile.captain.name = response.data['info'].captain_name
          this.collegeProfile.captain.mobile = response.data['info'].captain_mobile
          if ('members' in response.data) {
            if (this.collegeProfile.collegeMember) {
              for (let i = 0; i < response.data['members'].length; i++) {
                this.collegeProfile.members.push({
                  id: response.data['members'][i].member_id,
                  name: response.data['members'][i].member_name,
                  gender: (response.data['members'][i].member_gender === 'male') ? '男' : '女',
                  mobile: response.data['members'][i].member_mobile,
                  number: response.data['members'][i].num,
                  join: response.data['members'][i].join
                })
              }
            } else {
              for (let i = 0; i < response.data['members'].length; i++) {
                this.collegeProfile.members.push({
                  id: response.data['members'][i].member_id,
                  name: response.data['members'][i].member_name,
                  gender: (response.data['members'][i].member_gender === 'male') ? '男' : '女',
                  number: response.data['members'][i].num
                })
              }
            }
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
