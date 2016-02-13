app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.triggers = [];
    self.newTrigger = {
        state: true,
        repeatWeekday: false,
        repeatWeekend: false,
        stateName: function() {
            return this.state ? "ON" : "OFF";
        },
        toggleState: function() {
            this.state = ! this.state;
        },
        toggleRepeatWeekday: function() {
            this.repeatWeekday = ! this.repeatWeekday;
        },
        toggleRepeatWeekend: function() {
            this.repeatWeekend = ! this.repeatWeekend;
        },
        asData: function() {
            return {
                state: this.state,
                hour: moment(this.time).hour(),
                minute: moment(this.time).minute(),
                repeat_weekday: this.repeatWeekday,
                repeat_weekend: this.repeatWeekend,
            }
        }
    };

    self.toggle = function() {
        $http.get("/api/toggle").success(function(data) {
            self.updateState();
        });
    };

    self.setState = function(state) {
        $http.put("/api/state", {state: state}).success(function(data) {
            self.updateState();
        })
    };

    self.updateState = function() {
        $http.get("api/state").success(function(data) {
            self.lights = data["state"];
        });
    };

    self.updateTriggers = function() {
        $http.get("api/triggers").success(function(data) {
            self.triggers = data.map(function(data) {
                data.time = moment({hour: data.hour, minute: data.minute}).format("h:mm a");
                data.next_run_time = moment(data.next_run_time * 1000).toDate();
                return data
            });
            self.triggers.sort(function(a, b) {
                return a.next_run_time - b.next_run_time;
            })
        });
    };

    self.addTrigger = function() {
        $http.put("api/triggers", self.newTrigger.asData()).success(function(data) {
            self.updateTriggers();
        });
    };

    self.updateState();
    self.updateTriggers();

    return self;
});
