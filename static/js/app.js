app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.times = {};

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

    self.getTriggers = function() {
        $http.get("api/triggers").success(function(data) {
            for (var m in data) {
                var t = moment(data[m], "H:mm").toDate();
                console.log(data[m]);
                console.log(t);
                self.times[m] = t;
            }
        });
    };

    self.setTrigger = function(mode) {
        if (mode in self.times && self.times[mode]) {
            var data = {};
            data[mode] = moment(self.times[mode]).format("H:mm");
            $http.put("api/times", data).success(function(data) {
                self.getTimes();
            });
        }
    };

    self.updateState();
    self.getTriggers();

    return self;
});