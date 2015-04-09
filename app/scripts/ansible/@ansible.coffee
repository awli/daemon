# This file is capitalized so that it will be loaded before all other files
# with the same module.
angular.module('ansible', [])

.service 'ansible', ->

  HOSTNAME = '10.31.1.61'
  PORT = 12345
  socket = io("http://#{HOSTNAME}:#{PORT}")

  return socket

.service 'robotInfo', ->
  return -> {
    battery: Math.random() * .5 + .25,
    wireless_strength: Math.random() * .5 + .25
  }
