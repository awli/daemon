React = require('react')
Router = require('react-router')
RouteHandler = Router.RouteHandler

DNav = require('./DNav')

module.exports = Daemon = React.createClass
  displayName: 'Daemon'

  render: ->
    <div>
      <DNav {...this.props}/>
      <RouteHandler {...this.props}/>
    </div>
