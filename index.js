const matrix = require("@matrix-io/matrix-lite");
const mqtt = require('mqtt')
const client  = mqtt.connect('mqtt://158.97.91.177',8883)

client.on('connect', function () {
  client.subscribe('presence', function (err) {
    if (!err) {
      client.publish('presence', 'Hello mqtt')
    }
  })
})

client.on('message', function (topic, message) {
  // message is Buffer
  console.log(message.toString())
  client.end()
})
