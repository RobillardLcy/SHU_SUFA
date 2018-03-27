<template lang="html">
  <div class="MessageBox">
    <v-dialog >
      <v-card max-width=500>
        <v-card-title class="headline">{{ title }}</v-card-title>
        <v-card-text>{{ content }}</v-card-text>
        <v-card-actions>
          <v-btn color="red" flat @click.native="closeDialog">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'MessageBox',
  data: () => ({
  }),
  props: {
    title: {
      type: String,
      default () {
        return '提醒'
      }
    },
    content: {
      type: String,
      default () {
        return '错误！'
      }
    }
  },
  methods: {
    closeDialog: function () {
      this.$emit('closeDialog')
    }
  }
}
</script>

<style lang="css">
</style>
