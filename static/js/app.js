app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.triggers = [
        {
            "job_id": 1,
            state: true,
            time: "10:20",
            next_run_time: moment(1455319205*1000).format("dd MMM D h:mm a"),
            repeat_weekday: true,
            repeat_weekend: false
        },
        {
            "job_id": 2,
            state: true,
            time: "10:20",
            next_run_time: 1455319205,
            repeat_weekday: false,
            repeat_weekend: true
        },
        {"job_id": 3,
        state: true,
            time: "10:20",
        next_run_time: 1455319205,
        repeat_weekday: true,
        repeat_weekend: false}
    ];
    self.newTrigger = {
        state: true,
        hour: 10,
        minute: 20,
        repeat_weekday: true,
        repeat_weekend: false,
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
            self.triggers = data;
        });
    };

    self.addTrigger = function() {
        $http.put("api/triggers", self.newTrigger).success(function(data) {
            self.updateTriggers();
        });
    };

    self.updateState();
    //self.updateTriggers();

    return self;
});
