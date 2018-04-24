<template lang="html">
  <div class="FreeTeam">
    <h3>自由队伍</h3>
    <v-card>
      <v-container fluid grid-list-lg>
        <v-layout row wrap>
          <v-flex lg3 md6 xs12 v-for="team in teams" :key="team.id">
            <v-card :color="team.color" class="white--text" router :to="team.url">
              <v-container fluid grid-list-lg>
                <v-layout row>
                  <v-flex xs4>
                    <v-card-media
                      :src="team.logo"
                      height="60px"
                      contain></v-card-media>
                  </v-flex>
                  <v-flex xs8>
                    <v-card-title>
                      {{ team.name }}
                    </v-card-title>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'FreeTeam',
  data: () => ({
    teams: []
  }),
  mounted: function () {
    this.getTeams()
  },
  methods: {
    getTeams: function () {
      this.$axios.get('free-team/list/')
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            this.teams.push({
              url: '/team/free-team/' + response.data[i].id,
              name: response.data[i].name,
              logo: response.data[i].logo,
              color: (i % 3) === 0 ? 'orange lighten-1' : ((i % 3) === 1 ? 'lime lighten-1' : 'indigo ligthten-1')
            })
          }
        })
    }
  }
}
</script>

<style lang="css">
</style>
