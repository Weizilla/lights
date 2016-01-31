app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.times = {};

    self.toggle = function() {
        $http.get("/api/toggle").success(function(data) {
            self.getLights();
        });
    };

    self.setLights = function(state) {
        $http.put("/api/lights", {lights: state}).success(function(data) {
            self.getLights();
        })
    };

    self.getLights = function() {
        $http.get("api/lights").success(function(data) {
            self.lights = data["light"];
        });
    };

    self.getTimes = function() {
        $http.get("api/times").success(function(data) {
            for (var m in data) {
                var t = moment(data[m], "H:mm").toDate();
                console.log(data[m]);
                console.log(t);
                self.times[m] = t;
            }
        });
    };

    self.setTime = function(mode) {
        if (mode in self.times && self.times[mode]) {
            var data = {};
            data[mode] = moment(self.times[mode]).format("H:mm");
            $http.put("api/times", data).success(function(data) {
                self.getTimes();
            });
        }
    };

    self.getLights();
    self.getTimes();

    return self;
});