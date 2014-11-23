'use strict'

describe "daemon.radio", ->
  radio = undefined
  $interval = undefined
  callbackfn = undefined
  beforeEach ->
    module "daemon.radio"
    inject (_radio_) -> radio = _radio_
    inject (_$interval_) -> $interval = _$interval_
    callbackfn = jasmine.createSpy('callbackfn')

###
  describe "when initialized", ->

    beforeEach -> radio.init()
    it "should report an initialized radio", ->
      expect(radio.initialized()).toBe(true)
    it "should send", ->
      expect(radio.send('mock', {})).toBe true
    describe "and then closed", ->
      beforeEach -> radio.close()
      it "should not report an initialized radio", ->
        expect(radio.initialized()).toBe(false)
      it "should not accept callbacks", ->
        return_value = radio.onReceive('mock', callbackfn)
        expect(return_value).toBe(false)
        $interval.flush(101)
        expect(callbackfn).not.toHaveBeenCalled()

  describe "when not initialized", ->
    it "should not report an initialized radio", ->
      expect(radio.initialized()).toBe(false)
    it "should not accept callbacks", ->
      return_value = radio.onReceive('mock', callbackfn)
      expect(return_value).toBe(false)
      $interval.flush(101)
      expect(callbackfn).not.toHaveBeenCalled()
    it "should not send", ->
      return_value = radio.send('mock', {})
      expect(return_value).toBe false
###